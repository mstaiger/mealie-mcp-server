import logging
from typing import Any, Dict, List, Optional

from utils import format_api_params

logger = logging.getLogger("mealie-mcp")


class MealplanMixin:
    """Mixin class for mealplan-related API endpoints"""

    def get_mealplans(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get all mealplans for the current household with pagination.

        Args:
            start_date: Start date for filtering meal plans (ISO format YYYY-MM-DD)
            end_date: End date for filtering meal plans (ISO format YYYY-MM-DD)
            page: Page number to retrieve
            per_page: Number of items per page

        Returns:
            JSON response containing mealplan items and pagination information

        Raises:
            MealieApiError: If the API request fails
        """
        param_dict = {
            "startDate": start_date,
            "endDate": end_date,
            "page": page,
            "perPage": per_page,
        }

        params = format_api_params(param_dict)

        logger.info({"message": "Retrieving mealplans", "parameters": params})
        response = self._handle_request(
            "GET", "/api/households/mealplans", params=params
        )
        return response

    def create_mealplan(
        self,
        date: str,
        recipe_id: Optional[str] = None,
        title: Optional[str] = None,
        entry_type: str = "breakfast",
    ) -> Dict[str, Any]:
        """Create a new mealplan entry.

        Args:
            date: Date for the mealplan in ISO format (YYYY-MM-DD)
            recipe_id: UUID of the recipe to add to the mealplan (optional)
            title: Title for the mealplan entry if not using a recipe (optional)
            entry_type: Type of mealplan entry (breakfast, lunch, dinner, etc.)

        Returns:
            JSON response containing the created mealplan entry

        Raises:
            ValueError: If neither recipe_id nor title is provided
            MealieApiError: If the API request fails
        """
        if not recipe_id and not title:
            raise ValueError("Either recipe_id or title must be provided")
        if not date:
            raise ValueError("Date cannot be empty")

        # Build the request payload
        payload = {
            "date": date,
            "entryType": entry_type,
        }

        if recipe_id:
            payload["recipeId"] = recipe_id
        if title:
            payload["title"] = title

        logger.info(
            {
                "message": "Creating mealplan entry",
                "date": date,
                "entry_type": entry_type,
            }
        )
        return self._handle_request("POST", "/api/households/mealplans", json=payload)

    def get_todays_mealplan(self) -> List[Dict[str, Any]]:
        """Get the mealplan entries for today.

        Returns:
            List of today's mealplan entries

        Raises:
            MealieApiError: If the API request fails
        """
        logger.info({"message": "Retrieving today's mealplan"})
        return self._handle_request("GET", "/api/households/mealplans/today")

    def get_mealplan(self, mealplan_id: int) -> Dict[str, Any]:
        """Get a single mealplan entry by its integer ID."""
        if mealplan_id is None:
            raise ValueError("mealplan_id cannot be empty")

        logger.info({"message": "Retrieving mealplan entry", "mealplan_id": mealplan_id})
        return self._handle_request("GET", f"/api/households/mealplans/{mealplan_id}")

    def update_mealplan(
        self,
        mealplan_id: int,
        date: Optional[str] = None,
        entry_type: Optional[str] = None,
        title: Optional[str] = None,
        text: Optional[str] = None,
        recipe_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a mealplan entry.

        UpdatePlanEntry requires id + groupId + userId in the payload, so this
        fetches the current record and overlays the given fields.
        """
        if mealplan_id is None:
            raise ValueError("mealplan_id cannot be empty")

        updates: Dict[str, Any] = {}
        if date is not None:
            updates["date"] = date
        if entry_type is not None:
            updates["entryType"] = entry_type
        if title is not None:
            updates["title"] = title
        if text is not None:
            updates["text"] = text
        if recipe_id is not None:
            updates["recipeId"] = recipe_id

        if not updates:
            raise ValueError("At least one field must be provided to update")

        existing = self.get_mealplan(mealplan_id)
        payload = {
            "id": existing["id"],
            "groupId": existing["groupId"],
            "userId": existing["userId"],
            "date": existing["date"],
            "entryType": existing.get("entryType", "breakfast"),
            "title": existing.get("title", ""),
            "text": existing.get("text", ""),
            "recipeId": existing.get("recipeId"),
        }
        payload.update(updates)

        logger.info({"message": "Updating mealplan entry", "mealplan_id": mealplan_id})
        return self._handle_request(
            "PUT", f"/api/households/mealplans/{mealplan_id}", json=payload
        )

    def delete_mealplan(self, mealplan_id: int) -> Dict[str, Any]:
        """Delete a mealplan entry by its integer ID."""
        if mealplan_id is None:
            raise ValueError("mealplan_id cannot be empty")

        logger.info({"message": "Deleting mealplan entry", "mealplan_id": mealplan_id})
        return self._handle_request("DELETE", f"/api/households/mealplans/{mealplan_id}")

    def create_random_mealplan(
        self,
        date: str,
        entry_type: str = "dinner",
    ) -> Dict[str, Any]:
        """Create a random mealplan entry.

        Respects any household mealplan rules; with no rules configured, picks
        any random recipe.

        Args:
            date: Target date in ISO format (YYYY-MM-DD)
            entry_type: breakfast | lunch | dinner | side (default: dinner)
        """
        if not date:
            raise ValueError("date cannot be empty")

        payload = {"date": date, "entryType": entry_type}
        logger.info(
            {"message": "Creating random mealplan entry", "date": date, "entry_type": entry_type}
        )
        return self._handle_request(
            "POST", "/api/households/mealplans/random", json=payload
        )

    def get_mealplan_rules(
        self,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        order_by: Optional[str] = None,
        order_direction: Optional[str] = None,
        query_filter: Optional[str] = None,
        pagination_seed: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List mealplan rules for the current household.

        Rules constrain ``create_random_mealplan`` by matching day + entry_type
        against a ``queryFilterString`` (Mealie recipe query DSL).
        """
        param_dict = {
            "page": page,
            "perPage": per_page,
            "orderBy": order_by,
            "orderDirection": order_direction,
            "queryFilter": query_filter,
            "paginationSeed": pagination_seed,
        }
        params = format_api_params(param_dict)

        logger.info({"message": "Retrieving mealplan rules", "parameters": params})
        return self._handle_request(
            "GET", "/api/households/mealplans/rules", params=params
        )

    def create_mealplan_rule(
        self,
        day: str = "unset",
        entry_type: str = "unset",
        query_filter_string: str = "",
    ) -> Dict[str, Any]:
        """Create a mealplan rule.

        Args:
            day: One of monday..sunday or ``unset`` (matches any day)
            entry_type: breakfast | lunch | dinner | side | unset
            query_filter_string: Recipe filter expression (Mealie DSL)
        """
        payload = {
            "day": day,
            "entryType": entry_type,
            "queryFilterString": query_filter_string,
        }
        logger.info(
            {"message": "Creating mealplan rule", "day": day, "entry_type": entry_type}
        )
        return self._handle_request(
            "POST", "/api/households/mealplans/rules", json=payload
        )

    def get_mealplan_rule(self, rule_id: str) -> Dict[str, Any]:
        """Get a mealplan rule by UUID."""
        if not rule_id:
            raise ValueError("rule_id cannot be empty")

        logger.info({"message": "Retrieving mealplan rule", "rule_id": rule_id})
        return self._handle_request("GET", f"/api/households/mealplans/rules/{rule_id}")

    def update_mealplan_rule(
        self,
        rule_id: str,
        day: Optional[str] = None,
        entry_type: Optional[str] = None,
        query_filter_string: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a mealplan rule. Only provided fields are changed.

        PlanRulesOut requires id + groupId + householdId; fetch-merge-update.
        """
        if not rule_id:
            raise ValueError("rule_id cannot be empty")

        updates: Dict[str, Any] = {}
        if day is not None:
            updates["day"] = day
        if entry_type is not None:
            updates["entryType"] = entry_type
        if query_filter_string is not None:
            updates["queryFilterString"] = query_filter_string

        if not updates:
            raise ValueError("At least one field must be provided to update")

        existing = self.get_mealplan_rule(rule_id)
        payload = {
            "id": existing["id"],
            "groupId": existing["groupId"],
            "householdId": existing["householdId"],
            "day": existing.get("day", "unset"),
            "entryType": existing.get("entryType", "unset"),
            "queryFilterString": existing.get("queryFilterString", ""),
        }
        payload.update(updates)

        logger.info({"message": "Updating mealplan rule", "rule_id": rule_id})
        return self._handle_request(
            "PUT", f"/api/households/mealplans/rules/{rule_id}", json=payload
        )

    def delete_mealplan_rule(self, rule_id: str) -> Dict[str, Any]:
        """Delete a mealplan rule by UUID."""
        if not rule_id:
            raise ValueError("rule_id cannot be empty")

        logger.info({"message": "Deleting mealplan rule", "rule_id": rule_id})
        return self._handle_request(
            "DELETE", f"/api/households/mealplans/rules/{rule_id}"
        )
