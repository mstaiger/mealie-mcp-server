import logging
import traceback
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from mealie import MealieFetcher

logger = logging.getLogger("mealie-mcp")


def register_tools_organizer_tools(mcp: FastMCP, mealie: MealieFetcher) -> None:
    """Register recipe-tool (organizer) MCP tools."""

    @mcp.tool()
    def get_recipe_tools(
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List recipe tools (kitchen equipment) with pagination.

        Args:
            page: Page number to retrieve
            per_page: Number of items per page
            search: Optional search term to filter tools by name
        """
        try:
            logger.info({"message": "Fetching recipe tools", "page": page, "per_page": per_page})
            return mealie.get_recipe_tools(page=page, per_page=per_page, search=search)
        except Exception as e:
            error_msg = f"Error fetching recipe tools: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def create_recipe_tool(
        name: str,
        households_with_tool: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Create a new recipe tool.

        Args:
            name: Tool name (e.g., "Dutch Oven", "Stand Mixer")
            households_with_tool: Optional list of household IDs that own this tool
        """
        try:
            logger.info({"message": "Creating recipe tool", "name": name})
            return mealie.create_recipe_tool(name=name, households_with_tool=households_with_tool)
        except Exception as e:
            error_msg = f"Error creating recipe tool '{name}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_recipe_tool(tool_id: str) -> Dict[str, Any]:
        """Get a specific recipe tool by ID."""
        try:
            logger.info({"message": "Fetching recipe tool", "tool_id": tool_id})
            return mealie.get_recipe_tool(tool_id)
        except Exception as e:
            error_msg = f"Error fetching recipe tool '{tool_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_recipe_tool_by_slug(tool_slug: str) -> Dict[str, Any]:
        """Get a recipe tool by its slug (e.g., 'dutch-oven')."""
        try:
            logger.info({"message": "Fetching recipe tool by slug", "tool_slug": tool_slug})
            return mealie.get_recipe_tool_by_slug(tool_slug)
        except Exception as e:
            error_msg = f"Error fetching recipe tool by slug '{tool_slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def update_recipe_tool(
        tool_id: str,
        name: Optional[str] = None,
        households_with_tool: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Update a recipe tool's details."""
        try:
            logger.info({"message": "Updating recipe tool", "tool_id": tool_id})

            tool_data: Dict[str, Any] = {}
            if name is not None:
                tool_data["name"] = name
            if households_with_tool is not None:
                tool_data["householdsWithTool"] = households_with_tool

            if not tool_data:
                raise ValueError("At least one field must be provided to update")

            return mealie.update_recipe_tool(tool_id, tool_data)
        except Exception as e:
            error_msg = f"Error updating recipe tool '{tool_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def delete_recipe_tool(tool_id: str) -> Dict[str, Any]:
        """Delete a specific recipe tool."""
        try:
            logger.info({"message": "Deleting recipe tool", "tool_id": tool_id})
            return mealie.delete_recipe_tool(tool_id)
        except Exception as e:
            error_msg = f"Error deleting recipe tool '{tool_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)
