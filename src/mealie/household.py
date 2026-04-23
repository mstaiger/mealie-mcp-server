import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("mealie-mcp")

_PREFERENCES_FIELD_MAP = {
    "private_household": "privateHousehold",
    "lock_recipe_edits_from_other_households": "lockRecipeEditsFromOtherHouseholds",
    "first_day_of_week": "firstDayOfWeek",
    "recipe_public": "recipePublic",
    "recipe_show_nutrition": "recipeShowNutrition",
    "recipe_show_assets": "recipeShowAssets",
    "recipe_landscape_view": "recipeLandscapeView",
    "recipe_disable_comments": "recipeDisableComments",
    "recipe_disable_amount": "recipeDisableAmount",
}


class HouseholdMixin:
    """Mixin for household self-service endpoints (/api/households/*).

    Excludes cookbooks, shopping lists, mealplans, webhooks, events,
    recipe-actions, and invitations (handled elsewhere or out of scope).
    """

    def get_current_household(self) -> Dict[str, Any]:
        """Get the current authenticated user's household."""
        logger.info({"message": "Retrieving current household"})
        return self._handle_request("GET", "/api/households/self")

    def get_household_recipe(self, recipe_slug: str) -> Dict[str, Any]:
        """Get a recipe scoped to the current household by slug."""
        if not recipe_slug:
            raise ValueError("recipe_slug cannot be empty")

        logger.info({"message": "Retrieving household recipe", "slug": recipe_slug})
        return self._handle_request("GET", f"/api/households/self/recipes/{recipe_slug}")

    def get_household_members(self) -> List[Dict[str, Any]]:
        """List the current household's members."""
        logger.info({"message": "Retrieving household members"})
        return self._handle_request("GET", "/api/households/members")

    def get_household_preferences(self) -> Dict[str, Any]:
        """Get the current household's preferences."""
        logger.info({"message": "Retrieving household preferences"})
        return self._handle_request("GET", "/api/households/preferences")

    def update_household_preferences(
        self,
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

        Mealie accepts a partial body for this PUT — no fetch-merge needed.
        """
        local_values = {k: v for k, v in locals().items() if k != "self"}
        payload: Dict[str, Any] = {}
        for py_key, api_key in _PREFERENCES_FIELD_MAP.items():
            if local_values.get(py_key) is not None:
                payload[api_key] = local_values[py_key]

        if not payload:
            raise ValueError("At least one preference field must be provided to update")

        logger.info({"message": "Updating household preferences", "fields": list(payload)})
        return self._handle_request("PUT", "/api/households/preferences", json=payload)

    def set_household_permissions(
        self,
        user_id: str,
        can_manage_household: Optional[bool] = None,
        can_manage: Optional[bool] = None,
        can_invite: Optional[bool] = None,
        can_organize: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Set permission flags for a household member.

        Mealie's SetPermissions schema requires userId; all flags default
        to False on the server, so any flag you omit is treated as False.
        """
        if not user_id:
            raise ValueError("user_id cannot be empty")

        payload: Dict[str, Any] = {"userId": user_id}
        if can_manage_household is not None:
            payload["canManageHousehold"] = can_manage_household
        if can_manage is not None:
            payload["canManage"] = can_manage
        if can_invite is not None:
            payload["canInvite"] = can_invite
        if can_organize is not None:
            payload["canOrganize"] = can_organize

        logger.info({"message": "Setting household permissions", "user_id": user_id})
        return self._handle_request("PUT", "/api/households/permissions", json=payload)

    def get_household_statistics(self) -> Dict[str, Any]:
        """Get counts of recipes, users, cookbooks, etc. for the household."""
        logger.info({"message": "Retrieving household statistics"})
        return self._handle_request("GET", "/api/households/statistics")

    def get_household_invitations(self) -> List[Dict[str, Any]]:
        """List outstanding invite tokens for the current household."""
        logger.info({"message": "Retrieving household invitations"})
        return self._handle_request("GET", "/api/households/invitations")

    def create_household_invitation(
        self,
        uses: int = 1,
        group_id: Optional[str] = None,
        household_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create an invitation token.

        Args:
            uses: Number of times the token can be redeemed (default 1)
            group_id: Optional override for target group; omitted → current group
            household_id: Optional override for target household
        """
        if uses is None or uses < 1:
            raise ValueError("uses must be a positive integer")

        payload: Dict[str, Any] = {"uses": uses}
        if group_id is not None:
            payload["groupId"] = group_id
        if household_id is not None:
            payload["householdId"] = household_id

        logger.info({"message": "Creating household invitation", "uses": uses})
        return self._handle_request(
            "POST", "/api/households/invitations", json=payload
        )

    def send_household_invitation_email(
        self, email: str, token: str
    ) -> Dict[str, Any]:
        """Email an existing invite token to a recipient.

        Args:
            email: Destination email address
            token: Invite token string (from create_household_invitation)
        """
        if not email:
            raise ValueError("email cannot be empty")
        if not token:
            raise ValueError("token cannot be empty")

        payload = {"email": email, "token": token}
        logger.info({"message": "Emailing household invitation", "email": email})
        return self._handle_request(
            "POST", "/api/households/invitations/email", json=payload
        )
