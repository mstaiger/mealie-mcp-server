import logging
from typing import Any, Dict, List, Optional

from utils import format_api_params

logger = logging.getLogger("mealie-mcp")


class UnitsMixin:
    """Mixin class for ingredient unit-related API endpoints"""

    def get_units(
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
        """Get all ingredient units.

        Args:
            page: Page number to retrieve
            per_page: Number of items per page
            order_by: Field to order results by
            order_direction: Direction to order results ('asc' or 'desc')
            search: Search term to filter units
            query_filter: Advanced query filter
            order_by_null_position: How to handle nulls in ordering ('first' or 'last')
            pagination_seed: Seed for consistent pagination

        Returns:
            JSON response containing unit items and pagination information
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

        logger.info({"message": "Retrieving units", "parameters": params})
        return self._handle_request("GET", "/api/units", params=params)

    def get_unit(self, unit_id: str) -> Dict[str, Any]:
        """Get a specific unit by ID.

        Args:
            unit_id: The UUID of the unit

        Returns:
            JSON response containing the unit details
        """
        if not unit_id:
            raise ValueError("Unit ID cannot be empty")

        logger.info({"message": "Retrieving unit", "unit_id": unit_id})
        return self._handle_request("GET", f"/api/units/{unit_id}")

    def create_unit(
        self,
        name: str,
        plural_name: Optional[str] = None,
        description: Optional[str] = None,
        abbreviation: Optional[str] = None,
        plural_abbreviation: Optional[str] = None,
        use_abbreviation: Optional[bool] = None,
        fraction: Optional[bool] = None,
        aliases: Optional[List[str]] = None,
        extras: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new ingredient unit.

        Args:
            name: Name of the unit (required, e.g. "teaspoon")
            plural_name: Plural form of the unit name (e.g. "teaspoons")
            description: Free-text description of the unit
            abbreviation: Short form of the unit (e.g. "tsp")
            plural_abbreviation: Plural short form (e.g. "tsps")
            use_abbreviation: Whether the abbreviation should be rendered in the UI
            fraction: Whether the unit supports fractional amounts (e.g. 1/2)
            aliases: Alternative names for this unit (each becomes an alias object)
            extras: Arbitrary extra metadata for the unit

        Returns:
            JSON response containing the created unit
        """
        if not name:
            raise ValueError("Unit name cannot be empty")

        payload: Dict[str, Any] = {"name": name}
        if plural_name is not None:
            payload["pluralName"] = plural_name
        if description is not None:
            payload["description"] = description
        if abbreviation is not None:
            payload["abbreviation"] = abbreviation
        if plural_abbreviation is not None:
            payload["pluralAbbreviation"] = plural_abbreviation
        if use_abbreviation is not None:
            payload["useAbbreviation"] = use_abbreviation
        if fraction is not None:
            payload["fraction"] = fraction
        if aliases is not None:
            payload["aliases"] = [{"name": alias} for alias in aliases]
        if extras is not None:
            payload["extras"] = extras

        logger.info({"message": "Creating unit", "name": name})
        return self._handle_request("POST", "/api/units", json=payload)

    def update_unit(self, unit_id: str, unit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a specific unit.

        Args:
            unit_id: The UUID of the unit to update
            unit_data: Dictionary containing the unit properties to update
                (camelCase keys matching the Mealie API, e.g. 'name',
                'pluralName', 'description', 'abbreviation',
                'pluralAbbreviation', 'useAbbreviation', 'fraction',
                'aliases', 'extras')

        Returns:
            JSON response containing the updated unit
        """
        if not unit_id:
            raise ValueError("Unit ID cannot be empty")
        if not unit_data:
            raise ValueError("Unit data cannot be empty")

        logger.info({"message": "Updating unit", "unit_id": unit_id})
        return self._handle_request("PUT", f"/api/units/{unit_id}", json=unit_data)

    def delete_unit(self, unit_id: str) -> Dict[str, Any]:
        """Delete a specific unit.

        Args:
            unit_id: The UUID of the unit to delete

        Returns:
            JSON response confirming deletion
        """
        if not unit_id:
            raise ValueError("Unit ID cannot be empty")

        logger.info({"message": "Deleting unit", "unit_id": unit_id})
        return self._handle_request("DELETE", f"/api/units/{unit_id}")

    def merge_units(self, from_unit_id: str, to_unit_id: str) -> Dict[str, Any]:
        """Merge one unit into another. The source unit is deleted and its
        references are reassigned to the target unit.

        Args:
            from_unit_id: UUID of the unit to merge from (will be deleted)
            to_unit_id: UUID of the unit to merge into (will be retained)

        Returns:
            JSON response confirming the merge
        """
        if not from_unit_id:
            raise ValueError("from_unit_id cannot be empty")
        if not to_unit_id:
            raise ValueError("to_unit_id cannot be empty")

        payload = {"fromUnit": from_unit_id, "toUnit": to_unit_id}
        logger.info(
            {
                "message": "Merging units",
                "from_unit_id": from_unit_id,
                "to_unit_id": to_unit_id,
            }
        )
        return self._handle_request("PUT", "/api/units/merge", json=payload)
