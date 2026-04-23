import logging
import traceback
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from mealie import MealieFetcher

logger = logging.getLogger("mealie-mcp")


def register_group_tools(mcp: FastMCP, mealie: MealieFetcher) -> None:
    """Register group-context MCP tools."""

    @mcp.tool()
    def get_current_group() -> Dict[str, Any]:
        """Get the current authenticated user's group."""
        try:
            logger.info({"message": "Fetching current group"})
            return mealie.get_current_group()
        except Exception as e:
            error_msg = f"Error fetching current group: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_group_preferences() -> Dict[str, Any]:
        """Get group-level preferences."""
        try:
            logger.info({"message": "Fetching group preferences"})
            return mealie.get_group_preferences()
        except Exception as e:
            error_msg = f"Error fetching group preferences: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def update_group_preferences(private_group: Optional[bool] = None) -> Dict[str, Any]:
        """Update group-level preferences.

        Args:
            private_group: Whether the group is private (hidden from /explore)
        """
        try:
            logger.info({"message": "Updating group preferences"})
            return mealie.update_group_preferences(private_group=private_group)
        except Exception as e:
            error_msg = f"Error updating group preferences: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_group_members() -> List[Dict[str, Any]]:
        """List members of the current group."""
        try:
            logger.info({"message": "Fetching group members"})
            return mealie.get_group_members()
        except Exception as e:
            error_msg = f"Error fetching group members: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_group_member(username_or_id: str) -> Dict[str, Any]:
        """Get a specific group member by username or UUID."""
        try:
            logger.info({"message": "Fetching group member", "username_or_id": username_or_id})
            return mealie.get_group_member(username_or_id)
        except Exception as e:
            error_msg = f"Error fetching group member '{username_or_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_group_households() -> List[Dict[str, Any]]:
        """List households in the current group."""
        try:
            logger.info({"message": "Fetching group households"})
            return mealie.get_group_households()
        except Exception as e:
            error_msg = f"Error fetching group households: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_group_household(household_slug: str) -> Dict[str, Any]:
        """Get a group-scoped household by slug."""
        try:
            logger.info({"message": "Fetching group household", "slug": household_slug})
            return mealie.get_group_household(household_slug)
        except Exception as e:
            error_msg = f"Error fetching group household '{household_slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_group_storage() -> Dict[str, Any]:
        """Get the group's storage-usage summary."""
        try:
            logger.info({"message": "Fetching group storage"})
            return mealie.get_group_storage()
        except Exception as e:
            error_msg = f"Error fetching group storage: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_group_reports(report_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """List group-level reports (backup/restore/bulk-import job logs).

        Args:
            report_type: Optional filter by ReportCategory (e.g., "backup", "restore").
        """
        try:
            logger.info({"message": "Fetching group reports", "report_type": report_type})
            return mealie.get_group_reports(report_type=report_type)
        except Exception as e:
            error_msg = f"Error fetching group reports: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_group_report(report_id: str) -> Dict[str, Any]:
        """Get a specific group report by UUID."""
        try:
            logger.info({"message": "Fetching group report", "report_id": report_id})
            return mealie.get_group_report(report_id)
        except Exception as e:
            error_msg = f"Error fetching group report '{report_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def delete_group_report(report_id: str) -> Dict[str, Any]:
        """Delete a group report by UUID."""
        try:
            logger.info({"message": "Deleting group report", "report_id": report_id})
            return mealie.delete_group_report(report_id)
        except Exception as e:
            error_msg = f"Error deleting group report '{report_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)
