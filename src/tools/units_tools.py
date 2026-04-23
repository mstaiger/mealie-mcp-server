import logging
import traceback
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from mealie import MealieFetcher

logger = logging.getLogger("mealie-mcp")


def register_units_tools(mcp: FastMCP, mealie: MealieFetcher) -> None:
    """Register all unit-related tools with the MCP server."""

    @mcp.tool()
    def get_units(
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get all ingredient units with pagination and optional search.

        Args:
            page: Page number to retrieve
            per_page: Number of items per page
            search: Search term to filter units by name

        Returns:
            Dict[str, Any]: Units with pagination information
        """
        try:
            logger.info(
                {
                    "message": "Fetching units",
                    "page": page,
                    "per_page": per_page,
                    "search": search,
                }
            )
            return mealie.get_units(page=page, per_page=per_page, search=search)
        except Exception as e:
            error_msg = f"Error fetching units: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_unit(unit_id: str) -> Dict[str, Any]:
        """Get a specific unit by ID.

        Args:
            unit_id: The UUID of the unit

        Returns:
            Dict[str, Any]: The unit details
        """
        try:
            logger.info({"message": "Fetching unit", "unit_id": unit_id})
            return mealie.get_unit(unit_id)
        except Exception as e:
            error_msg = f"Error fetching unit '{unit_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def create_unit(
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
            name: Name of the unit (e.g., "teaspoon", "gram")
            plural_name: Plural form of the unit name (e.g., "teaspoons")
            description: Free-text description of the unit
            abbreviation: Short form of the unit (e.g., "tsp")
            plural_abbreviation: Plural short form of the unit (e.g., "tsps")
            use_abbreviation: Whether the abbreviation should be rendered in the UI
            fraction: Whether the unit supports fractional amounts (e.g., 1/2 cup)
            aliases: Alternative names for this unit
            extras: Arbitrary extra metadata for the unit

        Returns:
            Dict[str, Any]: The created unit details
        """
        try:
            logger.info({"message": "Creating unit", "name": name})
            return mealie.create_unit(
                name=name,
                plural_name=plural_name,
                description=description,
                abbreviation=abbreviation,
                plural_abbreviation=plural_abbreviation,
                use_abbreviation=use_abbreviation,
                fraction=fraction,
                aliases=aliases,
                extras=extras,
            )
        except Exception as e:
            error_msg = f"Error creating unit '{name}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def update_unit(
        unit_id: str,
        name: Optional[str] = None,
        plural_name: Optional[str] = None,
        description: Optional[str] = None,
        abbreviation: Optional[str] = None,
        plural_abbreviation: Optional[str] = None,
        use_abbreviation: Optional[bool] = None,
        fraction: Optional[bool] = None,
        aliases: Optional[List[str]] = None,
        extras: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Update a unit's details. Only provided fields are sent.

        Args:
            unit_id: The UUID of the unit to update
            name: New name for the unit
            plural_name: New plural form of the unit name
            description: New free-text description
            abbreviation: New short form of the unit
            plural_abbreviation: New plural short form of the unit
            use_abbreviation: Whether the abbreviation should be rendered in the UI
            fraction: Whether the unit supports fractional amounts
            aliases: Replacement list of alternative names for this unit
            extras: Replacement extra metadata dict for the unit

        Returns:
            Dict[str, Any]: The updated unit details
        """
        try:
            logger.info({"message": "Updating unit", "unit_id": unit_id})

            unit_data: Dict[str, Any] = {}
            if name is not None:
                unit_data["name"] = name
            if plural_name is not None:
                unit_data["pluralName"] = plural_name
            if description is not None:
                unit_data["description"] = description
            if abbreviation is not None:
                unit_data["abbreviation"] = abbreviation
            if plural_abbreviation is not None:
                unit_data["pluralAbbreviation"] = plural_abbreviation
            if use_abbreviation is not None:
                unit_data["useAbbreviation"] = use_abbreviation
            if fraction is not None:
                unit_data["fraction"] = fraction
            if aliases is not None:
                unit_data["aliases"] = [{"name": alias} for alias in aliases]
            if extras is not None:
                unit_data["extras"] = extras

            if not unit_data:
                raise ValueError("At least one field must be provided to update")

            return mealie.update_unit(unit_id, unit_data)
        except Exception as e:
            error_msg = f"Error updating unit '{unit_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def delete_unit(unit_id: str) -> Dict[str, Any]:
        """Delete a specific unit.

        Args:
            unit_id: The UUID of the unit to delete

        Returns:
            Dict[str, Any]: Confirmation of deletion
        """
        try:
            logger.info({"message": "Deleting unit", "unit_id": unit_id})
            return mealie.delete_unit(unit_id)
        except Exception as e:
            error_msg = f"Error deleting unit '{unit_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def merge_units(from_unit_id: str, to_unit_id: str) -> Dict[str, Any]:
        """Merge one unit into another. The source unit is deleted and all
        of its references (e.g. in recipe ingredients) are reassigned to
        the target unit.

        Args:
            from_unit_id: UUID of the unit to merge from (will be deleted)
            to_unit_id: UUID of the unit to merge into (will be retained)

        Returns:
            Dict[str, Any]: Confirmation of the merge
        """
        try:
            logger.info(
                {
                    "message": "Merging units",
                    "from_unit_id": from_unit_id,
                    "to_unit_id": to_unit_id,
                }
            )
            return mealie.merge_units(from_unit_id, to_unit_id)
        except Exception as e:
            error_msg = (
                f"Error merging unit '{from_unit_id}' into '{to_unit_id}': {str(e)}"
            )
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)
