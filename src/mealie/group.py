import logging
from typing import Any, Dict, List, Optional

from utils import format_api_params

logger = logging.getLogger("mealie-mcp")


class GroupMixin:
    """Mixin for group-scoped API endpoints (/api/groups/*).

    Excludes labels (own mixin), migrations, and seeders (out of scope).
    """

    def get_current_group(self) -> Dict[str, Any]:
        """Get the current authenticated user's group."""
        logger.info({"message": "Retrieving current group"})
        return self._handle_request("GET", "/api/groups/self")

    def get_group_preferences(self) -> Dict[str, Any]:
        """Get group-level preferences (private-group flag, etc.)."""
        logger.info({"message": "Retrieving group preferences"})
        return self._handle_request("GET", "/api/groups/preferences")

    def update_group_preferences(
        self, private_group: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Update group-level preferences.

        Args:
            private_group: Whether the group is private (hidden from /explore)
        """
        payload: Dict[str, Any] = {}
        if private_group is not None:
            payload["privateGroup"] = private_group

        if not payload:
            raise ValueError("At least one preference field must be provided")

        logger.info({"message": "Updating group preferences", "fields": list(payload)})
        return self._handle_request("PUT", "/api/groups/preferences", json=payload)

    def get_group_members(self) -> List[Dict[str, Any]]:
        """List members of the current group."""
        logger.info({"message": "Retrieving group members"})
        return self._handle_request("GET", "/api/groups/members")

    def get_group_member(self, username_or_id: str) -> Dict[str, Any]:
        """Get a specific group member by username or UUID."""
        if not username_or_id:
            raise ValueError("username_or_id cannot be empty")

        logger.info({"message": "Retrieving group member", "username_or_id": username_or_id})
        return self._handle_request("GET", f"/api/groups/members/{username_or_id}")

    def get_group_households(self) -> List[Dict[str, Any]]:
        """List households in the current group."""
        logger.info({"message": "Retrieving group households"})
        return self._handle_request("GET", "/api/groups/households")

    def get_group_household(self, household_slug: str) -> Dict[str, Any]:
        """Get a group-scoped household by slug."""
        if not household_slug:
            raise ValueError("household_slug cannot be empty")

        logger.info({"message": "Retrieving group household", "slug": household_slug})
        return self._handle_request("GET", f"/api/groups/households/{household_slug}")

    def get_group_storage(self) -> Dict[str, Any]:
        """Get the group's storage-usage summary."""
        logger.info({"message": "Retrieving group storage"})
        return self._handle_request("GET", "/api/groups/storage")

    def get_group_reports(self, report_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """List group-level reports (backup/restore/bulk-import job logs).

        Args:
            report_type: Optional filter; one of the ReportCategory values
                Mealie recognizes (e.g., "backup", "restore", "bulk_import").
        """
        params = format_api_params({"report_type": report_type})
        logger.info({"message": "Retrieving group reports", "params": params})
        return self._handle_request("GET", "/api/groups/reports", params=params)

    def get_group_report(self, report_id: str) -> Dict[str, Any]:
        """Get a specific group report by UUID."""
        if not report_id:
            raise ValueError("report_id cannot be empty")

        logger.info({"message": "Retrieving group report", "report_id": report_id})
        return self._handle_request("GET", f"/api/groups/reports/{report_id}")

    def delete_group_report(self, report_id: str) -> Dict[str, Any]:
        """Delete a group report by UUID."""
        if not report_id:
            raise ValueError("report_id cannot be empty")

        logger.info({"message": "Deleting group report", "report_id": report_id})
        return self._handle_request("DELETE", f"/api/groups/reports/{report_id}")
