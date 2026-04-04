#!/usr/bin/env node
/**
 * Multi-Agent Orchestration Pattern (TypeScript)
 * 
 * A pattern for coordinating multiple specialized AI agents that collaborate
 * on complex tasks. Each agent has a specific role, and a coordinator
 * delegates work and synthesizes results.
 * 
 * This pattern is used in systems like AutoGen, CrewAI, and OpenAI's multi-agent SDK.
 * 
 * Author: Eric Grill (https://ericgrill.com)
 * Related: https://github.com/ericgrill
 */

import { EventEmitter } from "events";

// ============================================================================
// TYPES
// ============================================================================

interface AgentConfig {
  name: string;
  role: string;
  systemPrompt: string;
  tools?: string[];
  llmConfig?: {
    model: string;
    temperature?: number;
  };
}

interface Task {
  id: string;
  description: string;
  assignedTo?: string;
  dependencies?: string[];
  status: "pending" | "in_progress" | "completed" | "failed";
  result?: any;
  error?: string;
}

interface Message {
  from: string;
  to: string;
  type: "task" | "result" | "delegation" | "broadcast";
  content: any;
  timestamp: Date;
}

// ============================================================================
// BASE AGENT CLASS
// ============================================================================

/**
 * Base class for all agents in the system.
 * Agents can receive tasks, execute them, and communicate with other agents.
 */
abstract class BaseAgent extends EventEmitter {
  public readonly name: string;
  public readonly role: string;
  protected systemPrompt: string;
  protected messageHistory: Message[] = [];
  protected isBusy: boolean = false;

  constructor(config: AgentConfig) {
    super();
    this.name = config.name;
    this.role = config.role;
    this.systemPrompt = config.systemPrompt;
  }

  /**
   * Receive a message from another agent or the orchestrator.
   */
  async receiveMessage(message: Message): Promise<void> {
    this.messageHistory.push(message);
    
    if (message.type === "task") {
      await this.handleTask(message);
    } else if (message.type === "delegation") {
      await this.handleDelegation(message);
    }
  }

  /**
   * Execute a task. Subclasses must implement this.
   */
  protected abstract executeTask(task: Task): Promise<any>;

  /**
   * Send a message to another agent.
   */
  protected sendMessage(to: string, type: Message["type"], content: any): void {
    const message: Message = {
      from: this.name,
      to,
      type,
      content,
      timestamp: new Date(),
    };
    this.emit("message", message);
  }

  private async handleTask(message: Message): Promise<void> {
    if (this.isBusy) {
      this.sendMessage(message.from, "result", {
        error: "Agent is busy",
        taskId: message.content.id,
      });
      return;
    }

    this.isBusy = true;
    const task: Task = message.content;
    
    try {
      console.log(`[${this.name}] Starting task: ${task.description}`);
      const result = await this.executeTask(task);
      
      this.sendMessage(message.from, "result", {
        taskId: task.id,
        status: "completed",
        result,
        agent: this.name,
      });
    } catch (error) {
      this.sendMessage(message.from, "result", {
        taskId: task.id,
        status: "failed",
        error: error instanceof Error ? error.message : String(error),
        agent: this.name,
      });
    } finally {
      this.isBusy = false;
    }
  }

  private async handleDelegation(message: Message): Promise<void> {
    // Handle being asked to coordinate sub-tasks
    const subTasks: Task[] = message.content.subTasks;
    console.log(`[${this.name}] Received delegation with ${subTasks.length} sub-tasks`);
    
    // Execute each sub-task sequentially or in parallel
    const results = await Promise.all(
      subTasks.map((task) => this.executeTask(task))
    );
    
    this.sendMessage(message.from, "result", {
      delegationId: message.content.delegationId,
      results,
      agent: this.name,
    });
  }
}

// ============================================================================
// SPECIALIZED AGENT IMPLEMENTATIONS
// ============================================================================

/**
 * Research Agent: Gathers information and performs analysis.
 */
class ResearchAgent extends BaseAgent {
  protected async executeTask(task: Task): Promise<any> {
    // Simulate research work
    await this.delay(1000);
    
    return {
      findings: `Research completed for: ${task.description}`,
      sources: ["Source A", "Source B", "Source C"],
      summary: "Key insights discovered...",
    };
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

/**
 * Code Agent: Writes and reviews code.
 */
class CodeAgent extends BaseAgent {
  protected async executeTask(task: Task): Promise<any> {
    // Simulate coding work
    await this.delay(1500);
    
    return {
      code: `// Generated code for: ${task.description}`,
      language: "typescript",
      tests: ["test1", "test2"],
      documentation: "API documentation...",
    };
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

/**
 * Review Agent: Quality assurance and critique.
 */
class ReviewAgent extends BaseAgent {
  protected async executeTask(task: Task): Promise<any> {
    // Simulate review work
    await this.delay(800);
    
    return {
      score: 8.5,
      feedback: ["Improve error handling", "Add more comments"],
      approved: true,
      suggestions: ["Consider using TypeScript strict mode"],
    };
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

// ============================================================================
// ORCHESTRATOR
// ============================================================================

/**
 * The Orchestrator coordinates multiple agents to accomplish complex goals.
 * It handles task decomposition, agent selection, and result synthesis.
 */
class Orchestrator extends EventEmitter {
  private agents: Map<string, BaseAgent> = new Map();
  private tasks: Map<string, Task> = new Map();
  private results: Map<string, any> = new Map();

  /**
   * Register an agent with the orchestrator.
   */
  registerAgent(agent: BaseAgent): void {
    this.agents.set(agent.name, agent);
    
    // Listen for messages from the agent
    agent.on("message", (message: Message) => {
      this.handleAgentMessage(message);
    });
    
    console.log(`[Orchestrator] Registered agent: ${agent.name} (${agent.role})`);
  }

  /**
   * Execute a complex goal by breaking it into tasks and delegating to agents.
   */
  async executeGoal(goal: string, context?: any): Promise<any> {
    console.log(`\n[Orchestrator] Starting goal: ${goal}`);
    
    // Step 1: Plan - Break goal into tasks
    const tasks = await this.planTasks(goal, context);
    console.log(`[Orchestrator] Planned ${tasks.length} tasks`);
    
    // Step 2: Execute - Delegate tasks to appropriate agents
    const executionPlan = this.createExecutionPlan(tasks);
    const results = await this.executePlan(executionPlan);
    
    // Step 3: Synthesize - Combine results into final output
    const finalResult = await this.synthesizeResults(goal, results);
    
    console.log(`[Orchestrator] Goal completed\n`);
    return finalResult;
  }

  private async planTasks(goal: string, context?: any): Promise<Task[]> {
    // In a real system, use an LLM to plan tasks
    // Here we use a simple rule-based approach for demonstration
    
    const tasks: Task[] = [];
    
    if (goal.toLowerCase().includes("research")) {
      tasks.push({
        id: "research-1",
        description: `Research: ${goal}`,
        status: "pending",
      });
    }
    
    if (goal.toLowerCase().includes("code") || goal.toLowerCase().includes("implement")) {
      tasks.push({
        id: "code-1",
        description: `Implement: ${goal}`,
        status: "pending",
        dependencies: tasks.length > 0 ? [tasks[tasks.length - 1].id] : undefined,
      });
      
      tasks.push({
        id: "review-1",
        description: `Review implementation of: ${goal}`,
        status: "pending",
        dependencies: ["code-1"],
      });
    }
    
    // Store tasks
    tasks.forEach((t) => this.tasks.set(t.id, t));
    
    return tasks;
  }

  private createExecutionPlan(tasks: Task[]): Map<string, Task[]> {
    // Group tasks by agent assignment
    const plan = new Map<string, Task[]>();
    
    for (const task of tasks) {
      const agentName = this.selectAgentForTask(task);
      if (!plan.has(agentName)) {
        plan.set(agentName, []);
      }
      plan.get(agentName)!.push(task);
    }
    
    return plan;
  }

  private selectAgentForTask(task: Task): string {
    // Simple role-based assignment
    if (task.description.toLowerCase().includes("research")) {
      return "researcher";
    } else if (task.description.toLowerCase().includes("review")) {
      return "reviewer";
    } else if (task.description.toLowerCase().includes("implement") || 
               task.description.toLowerCase().includes("code")) {
      return "coder";
    }
    return Array.from(this.agents.keys())[0];
  }

  private async executePlan(plan: Map<string, Task[]>): Promise<Map<string, any>> {
    const results = new Map<string, any>();
    
    // Execute tasks for each agent
    const promises: Promise<void>[] = [];
    
    for (const [agentName, tasks] of plan) {
      const agent = this.agents.get(agentName);
      if (!agent) continue;
      
      for (const task of tasks) {
        task.status = "in_progress";
        task.assignedTo = agentName;
        
        const promise = this.executeTaskWithAgent(agent, task).then((result) => {
          results.set(task.id, result);
          this.results.set(task.id, result);
        });
        
        promises.push(promise);
      }
    }
    
    await Promise.all(promises);
    return results;
  }

  private executeTaskWithAgent(agent: BaseAgent, task: Task): Promise<any> {
    return new Promise((resolve, reject) => {
      const message: Message = {
        from: "orchestrator",
        to: agent.name,
        type: "task",
        content: task,
        timestamp: new Date(),
      };
      
      // Set up one-time listener for result
      const onResult = (msg: Message) => {
        if (msg.type === "result" && msg.content.taskId === task.id) {
          agent.off("message", onResult);
          if (msg.content.error) {
            reject(new Error(msg.content.error));
          } else {
            resolve(msg.content.result);
          }
        }
      };
      
      agent.on("message", onResult);
      agent.receiveMessage(message);
    });
  }

  private async synthesizeResults(goal: string, results: Map<string, any>): Promise<any> {
    // In a real system, use an LLM to synthesize
    return {
      goal,
      completed: true,
      taskResults: Object.fromEntries(results),
      summary: `Successfully completed ${results.size} tasks`,
    };
  }

  private handleAgentMessage(message: Message): void {
    // Handle agent-to-agent communication if needed
    if (message.to !== "orchestrator") {
      const targetAgent = this.agents.get(message.to);
      if (targetAgent) {
        targetAgent.receiveMessage(message);
      }
    }
  }
}

// ============================================================================
// USAGE EXAMPLE
// ============================================================================

async function main() {
  // Create the orchestrator
  const orchestrator = new Orchestrator();
  
  // Create and register specialized agents
  orchestrator.registerAgent(new ResearchAgent({
    name: "researcher",
    role: "research",
    systemPrompt: "You are a research specialist. Gather comprehensive information and provide summaries.",
  }));
  
  orchestrator.registerAgent(new CodeAgent({
    name: "coder",
    role: "developer",
    systemPrompt: "You are a senior developer. Write clean, well-tested code with documentation.",
  }));
  
  orchestrator.registerAgent(new ReviewAgent({
    name: "reviewer",
    role: "qa",
    systemPrompt: "You are a code reviewer. Check for bugs, style issues, and best practices.",
  }));
  
  // Execute a complex goal
  const result = await orchestrator.executeGoal(
    "Research and implement a rate limiter",
    { language: "typescript", requirements: ["token bucket algorithm"] }
  );
  
  console.log("Final Result:", JSON.stringify(result, null, 2));
}

// Run if executed directly
if (require.main === module) {
  main().catch(console.error);
}

export { Orchestrator, BaseAgent, ResearchAgent, CodeAgent, ReviewAgent };
export type { AgentConfig, Task, Message };


/**
 * Key Patterns:
 * 
 * 1. Role-Based Agents: Each agent has a specific specialization
 * 2. Message Passing: Async communication between agents
 * 3. Task Decomposition: Break complex goals into manageable tasks
 * 4. Dynamic Planning: Determine execution order based on dependencies
 * 5. Result Synthesis: Combine individual outputs into coherent result
 * 
 * Extensions:
 * - Add LLM-based planning for dynamic task generation
 * - Implement retry logic and error recovery
 * - Add human-in-the-loop for approval checkpoints
 * - Implement agent bidding for task assignment
 * - Add streaming results for real-time updates
 * 
 * More at https://ericgrill.com
 */