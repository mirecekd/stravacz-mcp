"""
Entry point pro HTTP streaming verzi Stravacz MCP serveru

Spouští HTTP streaming MCP server na portu 8809.
"""

from src.stravacz_mcp_server.server_http import main

if __name__ == "__main__":
    main()
