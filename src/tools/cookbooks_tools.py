import logging
import traceback
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from mealie import MealieFetcher

logger = logging.getLogger("mealie-mcp")


def register_cookbooks_tools(mcp: FastMCP, mealie: MealieFetcher) -> None:
    """Register cookbook-related MCP tools."""

    @mcp.tool()
    def get_cookbooks(
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List cookbooks (saved recipe searches) for the current household."""
        try:
            logger.info({"message": "Fetching cookbooks", "page": page, "per_page": per_page})
            return mealie.get_cookbooks(page=page, per_page=per_page, search=search)
        except Exception as e:
            error_msg = f"Error fetching cookbooks: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def create_cookbook(
        name: str,
        description: Optional[str] = None,
        slug: Optional[str] = None,
        position: Optional[int] = None,
        public: Optional[bool] = None,
        query_filter_string: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new cookbook.

        Args:
            name: Cookbook display name
            description: Free-text description
            slug: Custom slug (server generates from name if omitted)
            position: Display-order position (1-based)
            public: Whether the cookbook is publicly discoverable
            query_filter_string: Recipe filter expression in Mealie's query DSL,
                e.g. ``tags.slug = "quick"`` or ``categories.name = "Breakfast"``
        """
        try:
            logger.info({"message": "Creating cookbook", "name": name})
            return mealie.create_cookbook(
                name=name,
                description=description,
                slug=slug,
                position=position,
                public=public,
                query_filter_string=query_filter_string,
            )
        except Exception as e:
            error_msg = f"Error creating cookbook '{name}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_cookbook(cookbook_id_or_slug: str) -> Dict[str, Any]:
        """Get a specific cookbook by ID or slug.

        The Mealie endpoint accepts either; pass whichever you have.
        """
        try:
            logger.info({"message": "Fetching cookbook", "id_or_slug": cookbook_id_or_slug})
            return mealie.get_cookbook(cookbook_id_or_slug)
        except Exception as e:
            error_msg = f"Error fetching cookbook '{cookbook_id_or_slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def update_cookbook(
        cookbook_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        slug: Optional[str] = None,
        position: Optional[int] = None,
        public: Optional[bool] = None,
        query_filter_string: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a cookbook. Only provide fields you want to change."""
        try:
            logger.info({"message": "Updating cookbook", "cookbook_id": cookbook_id})
            return mealie.update_cookbook(
                cookbook_id,
                name=name,
                description=description,
                slug=slug,
                position=position,
                public=public,
                query_filter_string=query_filter_string,
            )
        except Exception as e:
            error_msg = f"Error updating cookbook '{cookbook_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def delete_cookbook(cookbook_id: str) -> Dict[str, Any]:
        """Delete a cookbook."""
        try:
            logger.info({"message": "Deleting cookbook", "cookbook_id": cookbook_id})
            return mealie.delete_cookbook(cookbook_id)
        except Exception as e:
            error_msg = f"Error deleting cookbook '{cookbook_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def update_cookbooks_bulk(cookbooks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Bulk-update cookbooks (primarily used to reorder them).

        Args:
            cookbooks: List of full cookbook dicts. Each must include
                id, groupId, householdId, name. A common pattern is to
                fetch via get_cookbooks, modify each entry's ``position``,
                and pass the full list back.
        """
        try:
            logger.info({"message": "Bulk-updating cookbooks", "count": len(cookbooks)})
            return mealie.update_cookbooks_bulk(cookbooks)
        except Exception as e:
            error_msg = f"Error bulk-updating cookbooks: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)
