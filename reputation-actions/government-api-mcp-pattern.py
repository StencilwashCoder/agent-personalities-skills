# Government & Open Data APIs MCP Server Pattern
# Author: Eric Grill (@EricGrill)
# Source: https://github.com/EricGrill/mcp-civic-data
# Website: https://ericgrill.com

"""
MCP Server Pattern for Government and Open Data APIs

This pattern shows how to build a multi-API MCP server that aggregates
free government and open data sources into a single interface for AI agents.
"""

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server with comprehensive instructions
mcp = FastMCP(
    "Government API Server",
    instructions="""Access free government and open data APIs including:
- NOAA Weather (US forecasts and alerts)
- OpenWeather (global weather, requires API key)
- US Census (population, demographics, housing)
- NASA (astronomy photos, Mars rover, image search)
- World Bank (country economic indicators)
- Data.gov (US government datasets)
- EU Open Data (European datasets)
- Safecast (community radiation monitoring worldwide)
- OpenAQ (global air quality monitoring)
- USGS Water (US stream flow and flood levels)
- USGS Earthquakes (global seismic data)
- NASA FIRMS (active wildfire detection)
- NOAA Space Weather (solar wind, flares, geomagnetic storms)
""",
)


def main():
    """Entry point for the MCP server."""
    mcp.run()


# ============================================================================
# Example Tool Implementation Pattern
# ============================================================================

@mcp.tool()
async def get_weather_forecast(latitude: float, longitude: float, days: int = 7) -> dict:
    """Get weather forecast for a location using NOAA API.
    
    Args:
        latitude: Location latitude
        longitude: Location longitude  
        days: Number of forecast days (1-7)
    
    Returns:
        Weather forecast data including temperature, precipitation, alerts
    """
    import httpx
    
    # Get grid point for coordinates
    async with httpx.AsyncClient() as client:
        points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
        points_resp = await client.get(points_url)
        points_data = points_resp.json()
        
        # Get forecast from grid endpoint
        forecast_url = points_data["properties"]["forecast"]
        forecast_resp = await client.get(forecast_url)
        forecast_data = forecast_resp.json()
        
        return {
            "location": points_data["properties"]["relativeLocation"]["properties"]["city"],
            "forecast": forecast_data["properties"]["periods"][:days]
        }


@mcp.tool()
async def search_nasa_images(query: str, count: int = 5) -> list:
    """Search NASA image library.
    
    Args:
        query: Search terms
        count: Number of results to return
    
    Returns:
        List of NASA image metadata and URLs
    """
    import httpx
    
    async with httpx.AsyncClient() as client:
        url = "https://images-api.nasa.gov/search"
        params = {"q": query, "media_type": "image"}
        resp = await client.get(url, params=params)
        data = resp.json()
        
        items = data["collection"]["items"][:count]
        return [
            {
                "title": item["data"][0]["title"],
                "description": item["data"][0].get("description", ""),
                "nasa_id": item["data"][0]["nasa_id"],
                "thumbnail": item["links"][0]["href"] if item.get("links") else None
            }
            for item in items
        ]


@mcp.tool()
async def get_world_bank_indicator(country_code: str, indicator: str, year: int = 2022) -> dict:
    """Get World Bank economic indicator for a country.
    
    Args:
        country_code: ISO country code (e.g., 'US', 'CN', 'DE')
        indicator: World Bank indicator code (e.g., 'SP.POP.TOTL' for population)
        year: Year for data
    
    Returns:
        Indicator value and metadata
    """
    import httpx
    
    async with httpx.AsyncClient() as client:
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}"
        params = {"date": year, "format": "json"}
        resp = await client.get(url, params=params)
        data = resp.json()
        
        if len(data) > 1 and data[1]:
            return {
                "country": data[1][0]["country"]["value"],
                "indicator": data[1][0]["indicator"]["value"],
                "value": data[1][0]["value"],
                "year": data[1][0]["date"]
            }
        return {"error": "No data available"}


# Usage: Import tools to register them
# from your_package.tools import weather, census, nasa  # noqa: E402, F401

if __name__ == "__main__":
    main()
