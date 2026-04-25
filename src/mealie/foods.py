import logging
from typing import Any, Dict, List, Optional

from utils import format_api_params

logger = logging.getLogger("mealie-mcp")


class FoodsMixin:
    """Mixin class for ingredient food-related API endpoints"""

    def get_foods(
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
        """Get all ingredient foods.

        Args:
            page: Page number to retrieve
            per_page: Number of items per page
            order_by: Field to order results by
            order_direction: Direction to order results ('asc' or 'desc')
            search: Search term to filter foods
            query_filter: Advanced query filter
            order_by_null_position: How to handle nulls in ordering ('first' or 'last')
            pagination_seed: Seed for consistent pagination

        Returns:
            JSON response containing food items and pagination information
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

        logger.info({"message": "Retrieving foods", "parameters": params})
        return self._handle_request("GET", "/api/foods", params=params)

    def get_food(self, food_id: str) -> Dict[str, Any]:
        """Get a specific food by ID.

        Args:
            food_id: The UUID of the food

        Returns:
            JSON response containing the food details
        """
        if not food_id:
            raise ValueError("Food ID cannot be empty")

        logger.info({"message": "Retrieving food", "food_id": food_id})
        return self._handle_request("GET", f"/api/foods/{food_id}")

    def create_food(
        self,
        name: str,
        plural_name: Optional[str] = None,
        description: Optional[str] = None,
        label_id: Optional[str] = None,
        aliases: Optional[List[str]] = None,
        extras: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new ingredient food.

        Args:
            name: Name of the food (required)
            plural_name: Plural form of the food name
            description: Free-text description
            label_id: UUID of a MultiPurposeLabel to associate with the food
            aliases: Alternative names for this food (each becomes an alias object)
            extras: Arbitrary extra metadata for the food

        Returns:
            JSON response containing the created food
        """
        if not name:
            raise ValueError("Food name cannot be empty")

        payload: Dict[str, Any] = {"name": name}
        if plural_name is not None:
            payload["pluralName"] = plural_name
        if description is not None:
            payload["description"] = description
        if label_id is not None:
            payload["labelId"] = label_id
        if aliases is not None:
            payload["aliases"] = [{"name": alias} for alias in aliases]
        if extras is not None:
            payload["extras"] = extras

        logger.info({"message": "Creating food", "name": name})
        return self._handle_request("POST", "/api/foods", json=payload)

    def update_food(self, food_id: str, food_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a specific food.

        Args:
            food_id: The UUID of the food to update
            food_data: Dictionary containing the food properties to update
                (camelCase keys matching the Mealie API, e.g. 'name',
                'pluralName', 'description', 'labelId', 'aliases', 'extras')

        Returns:
            JSON response containing the updated food
        """
        if not food_id:
            raise ValueError("Food ID cannot be empty")
        if not food_data:
            raise ValueError("Food data cannot be empty")

        # Mealie's PUT is a full replace: the body's id field is bound
        # straight into the SQL UPDATE, so a missing id becomes NULL and
        # violates the NOT NULL primary key. Merge onto the existing food.
        existing = self.get_food(food_id)
        merged: Dict[str, Any] = {**existing, **food_data, "id": food_id}

        logger.info({"message": "Updating food", "food_id": food_id})
        return self._handle_request("PUT", f"/api/foods/{food_id}", json=merged)

    def delete_food(self, food_id: str) -> Dict[str, Any]:
        """Delete a specific food.

        Args:
            food_id: The UUID of the food to delete

        Returns:
            JSON response confirming deletion
        """
        if not food_id:
            raise ValueError("Food ID cannot be empty")

        logger.info({"message": "Deleting food", "food_id": food_id})
        return self._handle_request("DELETE", f"/api/foods/{food_id}")

    def merge_foods(self, from_food_id: str, to_food_id: str) -> Dict[str, Any]:
        """Merge one food into another. The source food is deleted and its
        references are reassigned to the target food.

        Args:
            from_food_id: UUID of the food to merge from (will be deleted)
            to_food_id: UUID of the food to merge into (will be retained)

        Returns:
            JSON response confirming the merge
        """
        if not from_food_id:
            raise ValueError("from_food_id cannot be empty")
        if not to_food_id:
            raise ValueError("to_food_id cannot be empty")

        payload = {"fromFood": from_food_id, "toFood": to_food_id}
        logger.info(
            {
                "message": "Merging foods",
                "from_food_id": from_food_id,
                "to_food_id": to_food_id,
            }
        )
        return self._handle_request("PUT", "/api/foods/merge", json=payload)
