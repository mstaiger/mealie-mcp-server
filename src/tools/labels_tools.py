import logging
import traceback
from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from mealie import MealieFetcher

logger = logging.getLogger("mealie-mcp")


def register_labels_tools(mcp: FastMCP, mealie: MealieFetcher) -> None:
    """Register label-related MCP tools."""

    @mcp.tool()
    def get_labels(
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List labels (used to group shopping-list items and annotate foods).

        Args:
            page: Page number to retrieve
            per_page: Number of items per page
            search: Optional search term to filter labels by name
        """
        try:
            logger.info({"message": "Fetching labels", "page": page, "per_page": per_page})
            return mealie.get_labels(page=page, per_page=per_page, search=search)
        except Exception as e:
            error_msg = f"Error fetching labels: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def create_label(name: str, color: Optional[str] = None) -> Dict[str, Any]:
        """Create a new label.

        Args:
            name: Label name (e.g., "Produce", "Dairy")
            color: Optional hex color string (e.g., "#ff0000"). Defaults to Mealie's "#959595".
        """
        try:
            logger.info({"message": "Creating label", "name": name})
            return mealie.create_label(name=name, color=color)
        except Exception as e:
            error_msg = f"Error creating label '{name}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_label(label_id: str) -> Dict[str, Any]:
        """Get a specific label by ID."""
        try:
            logger.info({"message": "Fetching label", "label_id": label_id})
            return mealie.get_label(label_id)
        except Exception as e:
            error_msg = f"Error fetching label '{label_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def update_label(
        label_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a label's name and/or color.

        Args:
            label_id: UUID of the label to update
            name: New label name
            color: New hex color string (e.g., "#ff0000")
        """
        try:
            logger.info({"message": "Updating label", "label_id": label_id})
            return mealie.update_label(label_id, name=name, color=color)
        except Exception as e:
            error_msg = f"Error updating label '{label_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def delete_label(label_id: str) -> Dict[str, Any]:
        """Delete a specific label."""
        try:
            logger.info({"message": "Deleting label", "label_id": label_id})
            return mealie.delete_label(label_id)
        except Exception as e:
            error_msg = f"Error deleting label '{label_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)
