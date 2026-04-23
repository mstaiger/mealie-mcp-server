import logging
from typing import Any, Dict, List, Optional

from utils import format_api_params

logger = logging.getLogger("mealie-mcp")


class CookbooksMixin:
    """Mixin class for cookbook API endpoints (/api/households/cookbooks/*).

    A cookbook is a saved search/filter over recipes — identified by a
    ``queryFilterString`` (Mealie's recipe query syntax). Cookbooks also
    carry a display ``position`` used to order them in the UI; the bulk
    PUT is primarily for reordering.
    """

    def get_cookbooks(
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
        """Get all cookbooks for the current household."""
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

        logger.info({"message": "Retrieving cookbooks", "parameters": params})
        return self._handle_request("GET", "/api/households/cookbooks", params=params)

    def create_cookbook(
        self,
        name: str,
        description: Optional[str] = None,
        slug: Optional[str] = None,
        position: Optional[int] = None,
        public: Optional[bool] = None,
        query_filter_string: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new cookbook.

        Args:
            name: Cookbook display name (required)
            description: Free-text description
            slug: Custom slug; server generates one from name if omitted
            position: Display-order position (1-based, defaults to 1)
            public: Whether the cookbook is publicly discoverable (default False)
            query_filter_string: Recipe filter expression in Mealie's query DSL
                (e.g. ``"tags.slug = 'quick'"``). Stored verbatim.
        """
        if not name:
            raise ValueError("Cookbook name cannot be empty")

        payload: Dict[str, Any] = {"name": name}
        if description is not None:
            payload["description"] = description
        if slug is not None:
            payload["slug"] = slug
        if position is not None:
            payload["position"] = position
        if public is not None:
            payload["public"] = public
        if query_filter_string is not None:
            payload["queryFilterString"] = query_filter_string

        logger.info({"message": "Creating cookbook", "name": name})
        return self._handle_request("POST", "/api/households/cookbooks", json=payload)

    def get_cookbook(self, cookbook_id_or_slug: str) -> Dict[str, Any]:
        """Get a specific cookbook by ID or slug.

        The Mealie endpoint accepts either a UUID or a slug string.
        """
        if not cookbook_id_or_slug:
            raise ValueError("Cookbook id or slug cannot be empty")

        logger.info({"message": "Retrieving cookbook", "id_or_slug": cookbook_id_or_slug})
        return self._handle_request("GET", f"/api/households/cookbooks/{cookbook_id_or_slug}")

    def update_cookbook(
        self,
        cookbook_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        slug: Optional[str] = None,
        position: Optional[int] = None,
        public: Optional[bool] = None,
        query_filter_string: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a cookbook.

        UpdateCookBook requires id + groupId + householdId in the payload, so
        this fetches the current record first and overlays the given fields.
        """
        if not cookbook_id:
            raise ValueError("Cookbook ID cannot be empty")

        updates: Dict[str, Any] = {}
        if name is not None:
            updates["name"] = name
        if description is not None:
            updates["description"] = description
        if slug is not None:
            updates["slug"] = slug
        if position is not None:
            updates["position"] = position
        if public is not None:
            updates["public"] = public
        if query_filter_string is not None:
            updates["queryFilterString"] = query_filter_string

        if not updates:
            raise ValueError("At least one field must be provided to update")

        existing = self.get_cookbook(cookbook_id)
        payload = {
            "id": existing["id"],
            "groupId": existing["groupId"],
            "householdId": existing["householdId"],
            "name": existing["name"],
            "description": existing.get("description", ""),
            "slug": existing.get("slug"),
            "position": existing.get("position", 1),
            "public": existing.get("public", False),
            "queryFilterString": existing.get("queryFilterString", ""),
        }
        payload.update(updates)

        logger.info({"message": "Updating cookbook", "cookbook_id": cookbook_id})
        return self._handle_request(
            "PUT", f"/api/households/cookbooks/{cookbook_id}", json=payload
        )

    def delete_cookbook(self, cookbook_id: str) -> Dict[str, Any]:
        """Delete a specific cookbook."""
        if not cookbook_id:
            raise ValueError("Cookbook ID cannot be empty")

        logger.info({"message": "Deleting cookbook", "cookbook_id": cookbook_id})
        return self._handle_request("DELETE", f"/api/households/cookbooks/{cookbook_id}")

    def update_cookbooks_bulk(self, cookbooks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Bulk update cookbooks (typically used for reordering via ``position``).

        Args:
            cookbooks: List of full cookbook dicts matching UpdateCookBook
                (must include id, groupId, householdId, name). Callers that
                only want to reorder can fetch via get_cookbooks, mutate
                ``position``, and pass the full list back.
        """
        if not cookbooks:
            raise ValueError("cookbooks list cannot be empty")

        logger.info({"message": "Bulk-updating cookbooks", "count": len(cookbooks)})
        return self._handle_request("PUT", "/api/households/cookbooks", json=cookbooks)
