#!/usr/bin/env python3
"""
Multi-Agent SSH Orchestration Pattern
=====================================
A pattern for coordinating AI agents across multiple servers via SSH.
Useful for distributed task execution, monitoring, and management.

Author: Eric Grill
Website: https://ericgrill.com
GitHub: https://github.com/ericgrill

Features:
- Execute commands on multiple servers concurrently
- Collect and aggregate results
- Error handling and retry logic
- Agent registration and heartbeat monitoring

Dependencies:
    pip install paramiko concurrent-futures

License: MIT
"""

import paramiko
import json
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Callable
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Status of a remote agent."""
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    ERROR = "error"


@dataclass
class ServerConfig:
    """Configuration for a remote server."""
    host: str
    port: int = 22
    username: str = ""
    key_path: str = "~/.ssh/id_rsa"
    password: Optional[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class TaskResult:
    """Result of a task execution."""
    host: str
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: float
    timestamp: float
    error: Optional[str] = None


@dataclass
class AgentInfo:
    """Information about a remote agent."""
    host: str
    status: str
    last_seen: float
    capabilities: List[str]
    load_avg: float = 0.0


class SSHConnectionPool:
    """Manages SSH connections with connection pooling."""
    
    def __init__(self, max_connections: int = 10):
        self._pool: Dict[str, paramiko.SSHClient] = {}
        self._lock = threading.Lock()
        self._max_connections = max_connections
    
    def get_connection(self, config: ServerConfig) -> paramiko.SSHClient:
        """Get or create an SSH connection."""
        key = f"{config.username}@{config.host}:{config.port}"
        
        with self._lock:
            if key in self._pool:
                # Verify connection is still alive
                try:
                    transport = self._pool[key].get_transport()
                    if transport and transport.is_active():
                        return self._pool[key]
                except Exception:
                    pass
            
            # Create new connection
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            connect_kwargs = {
                "hostname": config.host,
                "port": config.port,
                "username": config.username,
                "timeout": 30,
            }
            
            if config.password:
                connect_kwargs["password"] = config.password
            else:
                connect_kwargs["key_filename"] = config.key_path
            
            client.connect(**connect_kwargs)
            self._pool[key] = client
            logger.info(f"New SSH connection to {config.host}")
            return client
    
    def close_all(self):
        """Close all connections in the pool."""
        with self._lock:
            for client in self._pool.values():
                try:
                    client.close()
                except Exception as e:
                    logger.warning(f"Error closing connection: {e}")
            self._pool.clear()


class AgentOrchestrator:
    """Orchestrates multiple agents across SSH-connected servers."""
    
    def __init__(self, max_workers: int = 10):
        self.servers: Dict[str, ServerConfig] = {}
        self.agents: Dict[str, AgentInfo] = {}
        self.connection_pool = SSHConnectionPool(max_connections=max_workers)
        self.max_workers = max_workers
        self._heartbeat_thread: Optional[threading.Thread] = None
        self._stop_heartbeat = threading.Event()
    
    def register_server(self, config: ServerConfig) -> None:
        """Register a server for agent deployment."""
        self.servers[config.host] = config
        self.agents[config.host] = AgentInfo(
            host=config.host,
            status=AgentStatus.OFFLINE.value,
            last_seen=0,
            capabilities=[]
        )
        logger.info(f"Registered server: {config.host}")
    
    def execute_on_server(
        self, 
        config: ServerConfig, 
        command: str,
        timeout: int = 60
    ) -> TaskResult:
        """Execute a command on a single server."""
        start_time = time.time()
        
        try:
            client = self.connection_pool.get_connection(config)
            
            stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
            exit_code = stdout.channel.recv_exit_status()
            
            stdout_data = stdout.read().decode('utf-8', errors='replace')
            stderr_data = stderr.read().decode('utf-8', errors='replace')
            
            duration_ms = (time.time() - start_time) * 1000
            
            # Update agent info
            self.agents[config.host].last_seen = time.time()
            self.agents[config.host].status = AgentStatus.ONLINE.value
            
            return TaskResult(
                host=config.host,
                success=exit_code == 0,
                stdout=stdout_data,
                stderr=stderr_data,
                exit_code=exit_code,
                duration_ms=duration_ms,
                timestamp=time.time()
            )
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.agents[config.host].status = AgentStatus.ERROR.value
            
            return TaskResult(
                host=config.host,
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                duration_ms=duration_ms,
                timestamp=time.time(),
                error=str(e)
            )
    
    def execute_on_all(
        self, 
        command: str,
        filter_tags: Optional[List[str]] = None,
        timeout: int = 60
    ) -> List[TaskResult]:
        """
        Execute a command on all registered servers concurrently.
        
        Args:
            command: The shell command to execute
            filter_tags: Only execute on servers with these tags
            timeout: Command timeout in seconds
        """
        targets = list(self.servers.values())
        
        if filter_tags:
            targets = [
                s for s in targets 
                if any(tag in s.tags for tag in filter_tags)
            ]
        
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(
                    self.execute_on_server, config, command, timeout
                ): config.host
                for config in targets
            }
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                    logger.info(f"Completed on {result.host}: success={result.success}")
                except Exception as e:
                    host = futures[future]
                    logger.error(f"Failed to execute on {host}: {e}")
                    results.append(TaskResult(
                        host=host,
                        success=False,
                        stdout="",
                        stderr=str(e),
                        exit_code=-1,
                        duration_ms=0,
                        timestamp=time.time(),
                        error=str(e)
                    ))
        
        return results
    
    def execute_with_aggregation(
        self,
        command: str,
        aggregator: Callable[[List[TaskResult]], Dict],
        filter_tags: Optional[List[str]] = None
    ) -> Dict:
        """
        Execute on all servers and aggregate results.
        
        Example aggregator:
            def count_success(results):
                return {
                    'total': len(results),
                    'successful': sum(1 for r in results if r.success),
                    'failed': sum(1 for r in results if not r.success)
                }
        """
        results = self.execute_on_all(command, filter_tags)
        return aggregator(results)
    
    def start_heartbeat(self, interval: int = 30):
        """Start background heartbeat monitoring."""
        def heartbeat_loop():
            while not self._stop_heartbeat.wait(interval):
                self._check_all_agents()
        
        self._heartbeat_thread = threading.Thread(
            target=heartbeat_loop, 
            daemon=True
        )
        self._heartbeat_thread.start()
        logger.info(f"Started heartbeat monitoring (interval: {interval}s)")
    
    def stop_heartbeat(self):
        """Stop heartbeat monitoring."""
        self._stop_heartbeat.set()
        if self._heartbeat_thread:
            self._heartbeat_thread.join(timeout=5)
    
    def _check_all_agents(self):
        """Check connectivity to all registered agents."""
        results = self.execute_on_all("uptime", timeout=10)
        for result in results:
            agent = self.agents.get(result.host)
            if agent:
                if result.success:
                    agent.status = AgentStatus.ONLINE.value
                    agent.last_seen = time.time()
                else:
                    agent.status = AgentStatus.OFFLINE.value
    
    def get_agent_status(self) -> Dict[str, Dict]:
        """Get current status of all agents."""
        return {
            host: asdict(info) 
            for host, info in self.agents.items()
        }
    
    def close(self):
        """Clean up resources."""
        self.stop_heartbeat()
        self.connection_pool.close_all()


# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE USAGE
# ═══════════════════════════════════════════════════════════════════════════════

def example_aggregator(results: List[TaskResult]) -> Dict:
    """Example result aggregator."""
    return {
        "total_servers": len(results),
        "successful": sum(1 for r in results if r.success),
        "failed": sum(1 for r in results if not r.success),
        "avg_response_time_ms": sum(r.duration_ms for r in results) / len(results),
        "hosts": [r.host for r in results if r.success]
    }


def main():
    """Example usage of the AgentOrchestrator."""
    orchestrator = AgentOrchestrator(max_workers=5)
    
    # Register some servers
    servers = [
        ServerConfig(
            host="server1.example.com",
            username="admin",
            key_path="~/.ssh/id_rsa",
            tags=["web", "production"]
        ),
        ServerConfig(
            host="server2.example.com",
            username="admin",
            key_path="~/.ssh/id_rsa",
            tags=["db", "production"]
        ),
        ServerConfig(
            host="staging.example.com",
            username="deploy",
            password="staging-pass",  # Use keys in production!
            tags=["staging"]
        ),
    ]
    
    for server in servers:
        orchestrator.register_server(server)
    
    try:
        # Execute on all servers
        print("═" * 60)
        print("Running system check on all servers...")
        print("═" * 60)
        
        results = orchestrator.execute_on_all(
            command="df -h / | tail -1 | awk '{print $5}'",
            filter_tags=["production"]  # Only production servers
        )
        
        for result in results:
            print(f"\n📍 {result.host}")
            print(f"   Status: {'✅' if result.success else '❌'}")
            print(f"   Output: {result.stdout.strip()}")
            if result.stderr:
                print(f"   Error: {result.stderr.strip()}")
        
        # Aggregate results
        print("\n" + "═" * 60)
        print("Aggregated Results:")
        print("═" * 60)
        
        aggregated = orchestrator.execute_with_aggregation(
            command="uptime",
            aggregator=example_aggregator
        )
        print(json.dumps(aggregated, indent=2))
        
        # Start monitoring
        orchestrator.start_heartbeat(interval=30)
        
        # Show agent status
        print("\n" + "═" * 60)
        print("Agent Status:")
        print("═" * 60)
        status = orchestrator.get_agent_status()
        print(json.dumps(status, indent=2))
        
        # Keep running for a bit to show heartbeat
        time.sleep(5)
        
    finally:
        orchestrator.close()
        print("\n✅ Orchestrator shut down")


if __name__ == "__main__":
    main()
