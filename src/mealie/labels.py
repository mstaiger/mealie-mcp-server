import logging
from typing import Any, Dict, Optional

from utils import format_api_params

logger = logging.getLogger("mealie-mcp")


class LabelsMixin:
    """Mixin class for multi-purpose label API endpoints (/api/groups/labels/*).

    Labels are used by shopping list items (for grouping on the list) and by
    foods (as their display/category label).
    """

    def get_labels(
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
        """Get all labels.

        Returns:
            JSON response containing label items and pagination information
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

        logger.info({"message": "Retrieving labels", "parameters": params})
        return self._handle_request("GET", "/api/groups/labels", params=params)

    def create_label(self, name: str, color: Optional[str] = None) -> Dict[str, Any]:
        """Create a new label.

        Args:
            name: Label name (required)
            color: Optional hex color string, e.g. "#ff0000". Mealie defaults
                to "#959595" if omitted.
        """
        if not name:
            raise ValueError("Label name cannot be empty")

        payload: Dict[str, Any] = {"name": name}
        if color is not None:
            payload["color"] = color

        logger.info({"message": "Creating label", "name": name})
        return self._handle_request("POST", "/api/groups/labels", json=payload)

    def get_label(self, label_id: str) -> Dict[str, Any]:
        """Get a specific label by ID."""
        if not label_id:
            raise ValueError("Label ID cannot be empty")

        logger.info({"message": "Retrieving label", "label_id": label_id})
        return self._handle_request("GET", f"/api/groups/labels/{label_id}")

    def update_label(
        self,
        label_id: str,
        name: Optional[str] = None,
        color: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a label.

        MultiPurposeLabelUpdate requires id + groupId in the body, so this
        fetches the current record and overlays the given fields to avoid
        forcing callers to supply groupId.
        """
        if not label_id:
            raise ValueError("Label ID cannot be empty")
        if name is None and color is None:
            raise ValueError("At least one field (name, color) must be provided")

        existing = self.get_label(label_id)
        payload = {
            "id": existing["id"],
            "groupId": existing["groupId"],
            "name": name if name is not None else existing["name"],
            "color": color if color is not None else existing.get("color", "#959595"),
        }

        logger.info({"message": "Updating label", "label_id": label_id})
        return self._handle_request("PUT", f"/api/groups/labels/{label_id}", json=payload)

    def delete_label(self, label_id: str) -> Dict[str, Any]:
        """Delete a label."""
        if not label_id:
            raise ValueError("Label ID cannot be empty")

        logger.info({"message": "Deleting label", "label_id": label_id})
        return self._handle_request("DELETE", f"/api/groups/labels/{label_id}")
