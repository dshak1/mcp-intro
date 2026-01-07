"""
A simple Weather MCP Server
This server provides weather-related tools and resources
"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

# Create the MCP server instance
server = Server("weather-server")

# TODO: YOU WILL IMPLEMENT THIS!
# This decorator registers a function as an MCP tool
@server.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available tools this server provides.
    
    QUESTION FOR YOU: What should this return?
    Think about the schema! What information does the client need?
    """
    return [
        Tool(
            name="get_weather",
            description="Get current weather for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city to get weather for"
                    }
                    # CHALLENGE: Want to add more? Try adding "units" (celsius/fahrenheit)!
                },
                "required": ["city"]  # City is required!
            }
        )
    ]


# TODO: YOU WILL IMPLEMENT THIS!
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle tool calls from the client.
    
    QUESTION FOR YOU: What should happen when the client calls 'get_weather'?
    """
    if name == "get_weather":
        # Extract the city from arguments
        city = arguments.get("city", "Unknown")
        
        # For now, return fake weather data
        # Later you could call a real weather API!
        weather_report = f"Weather in {city}: 72°F (22°C), Sunny with clear skies ☀️"
        
        return [TextContent(
            type="text",
            text=weather_report
        )]
    else:
        raise ValueError(f"Unknown tool: {name}")


# Main entry point
async def main():
    """Run the server using stdio transport"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
