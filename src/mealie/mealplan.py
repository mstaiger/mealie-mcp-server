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
