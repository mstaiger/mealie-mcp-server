import logging
import traceback
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from mealie import MealieFetcher

logger = logging.getLogger("mealie-mcp")


def register_foods_tools(mcp: FastMCP, mealie: MealieFetcher) -> None:
    """Register all food-related tools with the MCP server."""

    @mcp.tool()
    def get_foods(
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get all ingredient foods with pagination and optional search.

        Args:
            page: Page number to retrieve
            per_page: Number of items per page
            search: Search term to filter foods by name

        Returns:
            Dict[str, Any]: Foods with pagination information
        """
        try:
            logger.info(
                {
                    "message": "Fetching foods",
                    "page": page,
                    "per_page": per_page,
                    "search": search,
                }
            )
            return mealie.get_foods(page=page, per_page=per_page, search=search)
        except Exception as e:
            error_msg = f"Error fetching foods: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_food(food_id: str) -> Dict[str, Any]:
        """Get a specific food by ID.

        Args:
            food_id: The UUID of the food

        Returns:
            Dict[str, Any]: The food details
        """
        try:
            logger.info({"message": "Fetching food", "food_id": food_id})
            return mealie.get_food(food_id)
        except Exception as e:
            error_msg = f"Error fetching food '{food_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def create_food(
        name: str,
        plural_name: Optional[str] = None,
        description: Optional[str] = None,
        label_id: Optional[str] = None,
        aliases: Optional[List[str]] = None,
        extras: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new ingredient food.

        Args:
            name: Name of the food (e.g., "Tomato", "Olive Oil")
            plural_name: Plural form of the food name (e.g., "Tomatoes")
            description: Free-text description of the food
            label_id: UUID of a MultiPurposeLabel to associate with the food
            aliases: Alternative names for this food
            extras: Arbitrary extra metadata for the food

        Returns:
            Dict[str, Any]: The created food details
        """
        try:
            logger.info({"message": "Creating food", "name": name})
            return mealie.create_food(
                name=name,
                plural_name=plural_name,
                description=description,
                label_id=label_id,
                aliases=aliases,
                extras=extras,
            )
        except Exception as e:
            error_msg = f"Error creating food '{name}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def update_food(
        food_id: str,
        name: Optional[str] = None,
        plural_name: Optional[str] = None,
        description: Optional[str] = None,
        label_id: Optional[str] = None,
        aliases: Optional[List[str]] = None,
        extras: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Update a food's details. Only provided fields are sent.

        Args:
            food_id: The UUID of the food to update
            name: New name for the food
            plural_name: New plural form of the food name
            description: New free-text description
            label_id: UUID of a MultiPurposeLabel to associate (set to empty string to clear)
            aliases: Replacement list of alternative names for this food
            extras: Replacement extra metadata dict for the food

        Returns:
            Dict[str, Any]: The updated food details
        """
        try:
            logger.info({"message": "Updating food", "food_id": food_id})

            food_data: Dict[str, Any] = {}
            if name is not None:
                food_data["name"] = name
            if plural_name is not None:
                food_data["pluralName"] = plural_name
            if description is not None:
                food_data["description"] = description
            if label_id is not None:
                food_data["labelId"] = label_id
            if aliases is not None:
                food_data["aliases"] = [{"name": alias} for alias in aliases]
            if extras is not None:
                food_data["extras"] = extras

            if not food_data:
                raise ValueError("At least one field must be provided to update")

            return mealie.update_food(food_id, food_data)
        except Exception as e:
            error_msg = f"Error updating food '{food_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def delete_food(food_id: str) -> Dict[str, Any]:
        """Delete a specific food.

        Args:
            food_id: The UUID of the food to delete

        Returns:
            Dict[str, Any]: Confirmation of deletion
        """
        try:
            logger.info({"message": "Deleting food", "food_id": food_id})
            return mealie.delete_food(food_id)
        except Exception as e:
            error_msg = f"Error deleting food '{food_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def merge_foods(from_food_id: str, to_food_id: str) -> Dict[str, Any]:
        """Merge one food into another. The source food is deleted and all
        of its references (e.g. in recipe ingredients) are reassigned to
        the target food.

        Args:
            from_food_id: UUID of the food to merge from (will be deleted)
            to_food_id: UUID of the food to merge into (will be retained)

        Returns:
            Dict[str, Any]: Confirmation of the merge
        """
        try:
            logger.info(
                {
                    "message": "Merging foods",
                    "from_food_id": from_food_id,
                    "to_food_id": to_food_id,
                }
            )
            return mealie.merge_foods(from_food_id, to_food_id)
        except Exception as e:
            error_msg = (
                f"Error merging food '{from_food_id}' into '{to_food_id}': {str(e)}"
            )
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)
