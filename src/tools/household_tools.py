import logging
import traceback
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from mealie import MealieFetcher

logger = logging.getLogger("mealie-mcp")


def register_household_tools(mcp: FastMCP, mealie: MealieFetcher) -> None:
    """Register household-context MCP tools."""

    @mcp.tool()
    def get_current_household() -> Dict[str, Any]:
        """Get information about the current authenticated user's household."""
        try:
            logger.info({"message": "Fetching current household"})
            return mealie.get_current_household()
        except Exception as e:
            error_msg = f"Error fetching current household: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_household_recipe(recipe_slug: str) -> Dict[str, Any]:
        """Get a recipe scoped to the current household (enforces private-household rules)."""
        try:
            logger.info({"message": "Fetching household recipe", "slug": recipe_slug})
            return mealie.get_household_recipe(recipe_slug)
        except Exception as e:
            error_msg = f"Error fetching household recipe '{recipe_slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_household_members() -> List[Dict[str, Any]]:
        """List members of the current household."""
        try:
            logger.info({"message": "Fetching household members"})
            return mealie.get_household_members()
        except Exception as e:
            error_msg = f"Error fetching household members: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_household_preferences() -> Dict[str, Any]:
        """Get the current household's preferences."""
        try:
            logger.info({"message": "Fetching household preferences"})
            return mealie.get_household_preferences()
        except Exception as e:
            error_msg = f"Error fetching household preferences: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def update_household_preferences(
        private_household: Optional[bool] = None,
        lock_recipe_edits_from_other_households: Optional[bool] = None,
        first_day_of_week: Optional[int] = None,
        recipe_public: Optional[bool] = None,
        recipe_show_nutrition: Optional[bool] = None,
        recipe_show_assets: Optional[bool] = None,
        recipe_landscape_view: Optional[bool] = None,
        recipe_disable_comments: Optional[bool] = None,
        recipe_disable_amount: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Update household preferences. Only provided fields are changed.

        Args:
            private_household: Whether the household is private
            lock_recipe_edits_from_other_households: Prevent cross-household edits
            first_day_of_week: 0=Sunday, 1=Monday, etc.
            recipe_public: Whether recipes are publicly visible by default
            recipe_show_nutrition: Show nutrition info on recipe cards
            recipe_show_assets: Show assets (attached files) on recipe pages
            recipe_landscape_view: Landscape card orientation
            recipe_disable_comments: Disable recipe comments site-wide
            recipe_disable_amount: Hide ingredient amounts by default
        """
        try:
            logger.info({"message": "Updating household preferences"})
            return mealie.update_household_preferences(
                private_household=private_household,
                lock_recipe_edits_from_other_households=lock_recipe_edits_from_other_households,
                first_day_of_week=first_day_of_week,
                recipe_public=recipe_public,
                recipe_show_nutrition=recipe_show_nutrition,
                recipe_show_assets=recipe_show_assets,
                recipe_landscape_view=recipe_landscape_view,
                recipe_disable_comments=recipe_disable_comments,
                recipe_disable_amount=recipe_disable_amount,
            )
        except Exception as e:
            error_msg = f"Error updating household preferences: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def set_household_permissions(
        user_id: str,
        can_manage_household: Optional[bool] = None,
        can_manage: Optional[bool] = None,
        can_invite: Optional[bool] = None,
        can_organize: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Set permission flags for a household member.

        Note: Mealie's API treats omitted flags as False. To toggle a single
        flag without clobbering others, first inspect the member via
        get_household_members and re-send all flags you want to keep.
        """
        try:
            logger.info({"message": "Setting household permissions", "user_id": user_id})
            return mealie.set_household_permissions(
                user_id,
                can_manage_household=can_manage_household,
                can_manage=can_manage,
                can_invite=can_invite,
                can_organize=can_organize,
            )
        except Exception as e:
            error_msg = f"Error setting permissions for user '{user_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_household_statistics() -> Dict[str, Any]:
        """Get counts (recipes, users, cookbooks, ...) for the current household."""
        try:
            logger.info({"message": "Fetching household statistics"})
            return mealie.get_household_statistics()
        except Exception as e:
            error_msg = f"Error fetching household statistics: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_household_invitations() -> List[Dict[str, Any]]:
        """List outstanding invite tokens for the current household."""
        try:
            logger.info({"message": "Fetching household invitations"})
            return mealie.get_household_invitations()
        except Exception as e:
            error_msg = f"Error fetching household invitations: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def create_household_invitation(
        uses: int = 1,
        group_id: Optional[str] = None,
        household_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create an invitation token.

        Args:
            uses: Number of times the token can be redeemed (default 1)
            group_id: Optional override for target group (defaults to current)
            household_id: Optional override for target household (defaults to current)
        """
        try:
            logger.info({"message": "Creating household invitation", "uses": uses})
            return mealie.create_household_invitation(
                uses=uses, group_id=group_id, household_id=household_id
            )
        except Exception as e:
            error_msg = f"Error creating household invitation: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def send_household_invitation_email(email: str, token: str) -> Dict[str, Any]:
        """Email an existing invite token to a recipient.

        Args:
            email: Destination email address
            token: Invite token string from create_household_invitation
        """
        try:
            logger.info({"message": "Emailing household invitation", "email": email})
            return mealie.send_household_invitation_email(email=email, token=token)
        except Exception as e:
            error_msg = f"Error emailing household invitation: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)
