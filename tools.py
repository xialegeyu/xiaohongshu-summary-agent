import os
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, SseConnectionParams, StreamableHTTPConnectionParams
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp import StdioServerParameters


xhs_mcp_server = McpToolset(
    # Use StreamableHTTPConnectionParams for HTTP connection
    connection_params=StreamableHTTPConnectionParams(
        # Provide the URL of the running server
        url=os.getenv("XHS_MCP_SERVER_URL"),
        headers={"Authorization": os.getenv("XHS_TOKEN")}
    ),
    # get_feed_detail: get post details using feed_id and xsec_token
    # search_feeds: search posts using keyword
    tool_filter=['get_feed_detail', 'search_feeds']
)

