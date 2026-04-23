import logging
from typing import Any, Dict, List, Optional

from utils import format_api_params

logger = logging.getLogger("mealie-mcp")


class ToolsOrganizerMixin:
    """Mixin class for recipe-tool organizer API endpoints (/api/organizers/tools/*)."""

    def get_recipe_tools(
        self,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        order_by: Optional[str] = None,
        order_direction: Optional[str] = None,
        search: Optional[str] = None,
        query_filter: Optional[str] = None,
        order_by_null_position: Optional[str] = None,
        pagination_seed: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get all recipe tools (kitchen equipment).

        Returns:
            JSON response containing tool items and pagination information
        """
        param_dict = {
            "page": page,
            "perPage": per_page,
            "orderBy": order_by,
            "orderDirection": order_direction,
            "search": search,
            "queryFilter": query_filter,
            "orderByNullPosition": order_by_null_position,
            "paginationSeed": pagination_seed,
        }
        params = format_api_params(param_dict)

        logger.info({"message": "Retrieving recipe tools", "parameters": params})
        return self._handle_request("GET", "/api/organizers/tools", params=params)

    def create_recipe_tool(
        self,
        name: str,
        households_with_tool: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Create a new recipe tool.

        Args:
            name: Name of the tool (required)
            households_with_tool: Optional list of household IDs that own this tool
        """
        if not name:
            raise ValueError("Tool name cannot be empty")

        payload: Dict[str, Any] = {"name": name}
        if households_with_tool is not None:
            payload["householdsWithTool"] = households_with_tool

        logger.info({"message": "Creating recipe tool", "name": name})
        return self._handle_request("POST", "/api/organizers/tools", json=payload)

    def get_recipe_tool(self, tool_id: str) -> Dict[str, Any]:
        """Get a specific recipe tool by ID."""
        if not tool_id:
            raise ValueError("Tool ID cannot be empty")

        logger.info({"message": "Retrieving recipe tool", "tool_id": tool_id})
        return self._handle_request("GET", f"/api/organizers/tools/{tool_id}")

    def get_recipe_tool_by_slug(self, tool_slug: str) -> Dict[str, Any]:
        """Get a specific recipe tool by its slug."""
        if not tool_slug:
            raise ValueError("Tool slug cannot be empty")

        logger.info({"message": "Retrieving recipe tool by slug", "tool_slug": tool_slug})
        return self._handle_request("GET", f"/api/organizers/tools/slug/{tool_slug}")

    def update_recipe_tool(self, tool_id: str, tool_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a recipe tool.

        Args:
            tool_id: UUID of the tool to update
            tool_data: camelCase dict matching RecipeToolCreate
                (e.g. 'name', 'householdsWithTool')
        """
        if not tool_id:
            raise ValueError("Tool ID cannot be empty")
        if not tool_data:
            raise ValueError("Tool data cannot be empty")

        logger.info({"message": "Updating recipe tool", "tool_id": tool_id})
        return self._handle_request("PUT", f"/api/organizers/tools/{tool_id}", json=tool_data)

    def delete_recipe_tool(self, tool_id: str) -> Dict[str, Any]:
        """Delete a recipe tool."""
        if not tool_id:
            raise ValueError("Tool ID cannot be empty")

        logger.info({"message": "Deleting recipe tool", "tool_id": tool_id})
        return self._handle_request("DELETE", f"/api/organizers/tools/{tool_id}")
