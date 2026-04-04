# Bitcoin OP_RETURN Data Operations with MCP
# Author: Eric Grill (@EricGrill)
# Source: https://github.com/EricGrill/mcp-bitcoin-cli
# Website: https://ericgrill.com

"""
MCP server for Bitcoin OP_RETURN data operations.

This server exposes tools for working with Bitcoin OP_RETURN data,
including low-level primitives, Bitcoin Core interface, token operations,
document storage, and timestamping.
"""

import hashlib
from typing import Optional
from mcp.server.fastmcp import FastMCP

from mcp_bitcoin_cli.config import Config, ConnectionMethod, load_config
from mcp_bitcoin_cli.envelope import EnvelopeType, decode_envelope, encode_envelope
from mcp_bitcoin_cli.node.cli import BitcoinCLI
from mcp_bitcoin_cli.node.interface import NodeInterface
from mcp_bitcoin_cli.node.rpc import BitcoinRPC
from mcp_bitcoin_cli.primitives import decode_op_return_script, encode_op_return_script
from mcp_bitcoin_cli.protocols.brc20 import BRC20Deploy, BRC20Mint, BRC20Transfer


def create_server(config: Optional[Config] = None) -> FastMCP:
    """Create and configure the MCP server with all tools."""
    if config is None:
        config = Config()

    mcp = FastMCP("mcp-bitcoin-cli")
    mcp._config = config
    mcp._node: Optional[NodeInterface] = None

    def get_node() -> NodeInterface:
        """Get or create the node interface."""
        if mcp._node is None:
            if config.connection_method == ConnectionMethod.CLI:
                mcp._node = BitcoinCLI(config)
            else:
                mcp._node = BitcoinRPC(config)
        return mcp._node

    # =========================================================================
    # Low-Level Primitives (offline-capable)
    # =========================================================================

    @mcp.tool()
    def encode_op_return(data: str, encoding: str = "utf-8") -> dict:
        """Encode arbitrary data into OP_RETURN script format.
        
        Args:
            data: Data to encode (string)
            encoding: Encoding for the data ('utf-8', 'hex'). Default: 'utf-8'
        
        Returns:
            Dictionary with 'script_hex' containing the OP_RETURN script.
        """
        if encoding == "hex":
            try:
                data_bytes = bytes.fromhex(data)
            except ValueError as e:
                return {"error": f"Invalid hex string: {e}"}
        else:
            data_bytes = data.encode(encoding)

        script = encode_op_return_script(data_bytes)
        return {"script_hex": script.hex()}

    @mcp.tool()
    def decode_op_return(script_hex: str) -> dict:
        """Parse OP_RETURN data from script hex.
        
        Args:
            script_hex: OP_RETURN script as hex string
        
        Returns:
            Dictionary with 'data_hex' and 'data_utf8' (if decodable).
        """
        try:
            script = bytes.fromhex(script_hex)
        except ValueError as e:
            return {"error": f"Invalid hex string: {e}"}

        data = decode_op_return_script(script)
        result = {"data_hex": data.hex()}

        try:
            result["data_utf8"] = data.decode("utf-8")
        except UnicodeDecodeError:
            result["data_utf8"] = None

        return result

    @mcp.tool()
    def build_op_return_transaction(
        data: str,
        encoding: str = "utf-8",
        use_envelope: bool = True,
        envelope_type: str = "raw",
    ) -> dict:
        """Construct OP_RETURN output data for a transaction.
        
        This prepares the data for inclusion in a transaction but does not
        create or broadcast the transaction itself.
        
        Args:
            data: Data to embed
            encoding: Data encoding ('utf-8' or 'hex')
            use_envelope: Whether to wrap in BTCD envelope format
            envelope_type: Envelope protocol type ('raw', 'doc', 'brc20')
        
        Returns:
            Dictionary with prepared transaction output data
        """
        if encoding == "hex":
            data_bytes = bytes.fromhex(data)
        else:
            data_bytes = data.encode(encoding)

        if use_envelope:
            etype = EnvelopeType(envelope_type)
            data_bytes = encode_envelope(data_bytes, etype)

        script = encode_op_return_script(data_bytes)

        return {
            "script_hex": script.hex(),
            "script_asm": f"OP_RETURN {script[1:].hex()}",
            "data_size_bytes": len(data_bytes),
            "envelope_used": use_envelope,
            "envelope_type": envelope_type if use_envelope else None,
        }

    return mcp


# Example usage
if __name__ == "__main__":
    server = create_server()
    # Run with: mcp.run()
