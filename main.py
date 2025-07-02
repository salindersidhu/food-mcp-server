import httpx
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("MealBot")

# MealDB API Setup 
MEALDB_BASE_URL = "https://www.themealdb.com/api/json/v1/1/"


@mcp.tool(title="Meal Fetcher")
async def fetch_meal_by_name(name: str) -> dict:
    """Fetch meals by their name."""
    async with httpx.AsyncClient() as client:
        url = f"{MEALDB_BASE_URL}search.php?s={name}"
        response = await client.get(url)
        return response.json()


if __name__ == "__main__":
    # Start the server
    mcp.run()
