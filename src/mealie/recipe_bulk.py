import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("mealie-mcp")


class RecipeBulkMixin:
    """Bulk recipe operations (batch update, tag, categorize, delete)."""

    def _resolve_recipe_ids(self, recipe_slugs: List[str]) -> List[str]:
        """Resolve recipe slugs to UUIDs.

        Mealie's bulk-actions endpoints accept the field name `recipes` but
        match against recipe.id (UUID), not slug — passing slugs returns 200
        with zero rows updated.
        """
        ids: List[str] = []
        for slug in recipe_slugs:
            recipe = self._handle_request("GET", f"/api/recipes/{slug}")
            recipe_id = recipe.get("id") if isinstance(recipe, dict) else None
            if not recipe_id:
                raise ValueError(f"Could not resolve recipe id for slug '{slug}'")
            ids.append(recipe_id)
        return ids

    def bulk_categorize_recipes(
        self, recipe_slugs: List[str], categories: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Attach categories to many recipes at once.

        Tries the dedicated bulk-actions/categorize endpoint first; falls back
        to PATCH /api/recipes if the endpoint is unavailable.

        Args:
            recipe_slugs: List of recipe slugs to update
            categories: Full CategoryBase dicts (each with id + name + slug)
        """
        if not recipe_slugs:
            raise ValueError("recipe_slugs cannot be empty")
        if not categories:
            raise ValueError("categories cannot be empty")

        recipe_ids = self._resolve_recipe_ids(recipe_slugs)
        payload = {"recipes": recipe_ids, "categories": categories}
        logger.info(
            {"message": "Bulk-categorizing recipes", "count": len(recipe_ids)}
        )
        try:
            result = self._handle_request(
                "POST", "/api/recipes/bulk-actions/categorize", json=payload
            )
            if isinstance(result, list):
                return result
            return [result] if isinstance(result, dict) else []
        except Exception as e:
            logger.info(
                {
                    "message": "bulk-actions/categorize endpoint failed, falling back to PATCH",
                    "error": str(e),
                }
            )
            patches = [
                {"id": rid, "recipeCategory": categories} for rid in recipe_ids
            ]
            return self.patch_recipes_batch(patches)

    def bulk_tag_recipes(
        self, recipe_slugs: List[str], tags: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Attach tags to many recipes at once.

        Tries the dedicated bulk-actions/tag endpoint first; falls back to
        PATCH /api/recipes if the endpoint is unavailable (removed in some
        Mealie versions).

        Args:
            recipe_slugs: List of recipe slugs to update
            tags: Full TagBase dicts (each with id + name + slug)
        """
        if not recipe_slugs:
            raise ValueError("recipe_slugs cannot be empty")
        if not tags:
            raise ValueError("tags cannot be empty")

        recipe_ids = self._resolve_recipe_ids(recipe_slugs)
        payload = {"recipes": recipe_ids, "tags": tags}
        logger.info({"message": "Bulk-tagging recipes", "count": len(recipe_ids)})
        try:
            result = self._handle_request(
                "POST", "/api/recipes/bulk-actions/tag", json=payload
            )
            if isinstance(result, list):
                return result
            return [result] if isinstance(result, dict) else []
        except Exception as e:
            logger.info(
                {
                    "message": "bulk-actions/tag endpoint failed, falling back to PATCH",
                    "error": str(e),
                }
            )
            patches = [{"id": rid, "tags": tags} for rid in recipe_ids]
            return self.patch_recipes_batch(patches)

    def bulk_update_recipe_settings(
        self,
        recipe_slugs: List[str],
        public: Optional[bool] = None,
        show_nutrition: Optional[bool] = None,
        show_assets: Optional[bool] = None,
        landscape_view: Optional[bool] = None,
        disable_comments: Optional[bool] = None,
        disable_amount: Optional[bool] = None,
        locked: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Apply the same settings (public, locked, etc.) across many recipes.

        Omitted fields are left at their server defaults (Mealie's
        RecipeSettings schema uses defaults for unspecified keys).
        """
        if not recipe_slugs:
            raise ValueError("recipe_slugs cannot be empty")

        settings: Dict[str, Any] = {}
        if public is not None:
            settings["public"] = public
        if show_nutrition is not None:
            settings["showNutrition"] = show_nutrition
        if show_assets is not None:
            settings["showAssets"] = show_assets
        if landscape_view is not None:
            settings["landscapeView"] = landscape_view
        if disable_comments is not None:
            settings["disableComments"] = disable_comments
        if disable_amount is not None:
            settings["disableAmount"] = disable_amount
        if locked is not None:
            settings["locked"] = locked

        if not settings:
            raise ValueError("At least one setting must be provided")

        recipe_ids = self._resolve_recipe_ids(recipe_slugs)
        payload = {"recipes": recipe_ids, "settings": settings}
        logger.info(
            {
                "message": "Bulk-updating recipe settings",
                "count": len(recipe_ids),
                "fields": list(settings),
            }
        )
        return self._handle_request(
            "POST", "/api/recipes/bulk-actions/settings", json=payload
        )

    def bulk_delete_recipes(self, recipe_slugs: List[str]) -> Dict[str, Any]:
        """Delete many recipes at once by slug."""
        if not recipe_slugs:
            raise ValueError("recipe_slugs cannot be empty")

        recipe_ids = self._resolve_recipe_ids(recipe_slugs)
        payload = {"recipes": recipe_ids}
        logger.info({"message": "Bulk-deleting recipes", "count": len(recipe_ids)})
        return self._handle_request(
            "POST", "/api/recipes/bulk-actions/delete", json=payload
        )

    def update_recipes_batch(
        self, recipes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Full-replace many recipes in a single call (PUT /api/recipes).

        Args:
            recipes: List of complete recipe dicts (Recipe-Input shape). Each
                should include the full recipe body; partial payloads will
                zero out missing fields. Use ``patch_recipes_batch`` for
                partial updates.
        """
        if not recipes:
            raise ValueError("recipes cannot be empty")

        logger.info({"message": "Batch-replacing recipes", "count": len(recipes)})
        result = self._handle_request("PUT", "/api/recipes", json=recipes)
        if isinstance(result, list):
            return result
        return [result] if isinstance(result, dict) else []

    def patch_recipes_batch(
        self, recipes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Partial-update many recipes in a single call (PATCH /api/recipes).

        Each entry must carry enough identifying info (slug and/or id) plus
        the fields to change. Unspecified fields are left alone.
        """
        if not recipes:
            raise ValueError("recipes cannot be empty")

        logger.info({"message": "Batch-patching recipes", "count": len(recipes)})
        result = self._handle_request("PATCH", "/api/recipes", json=recipes)
        if isinstance(result, list):
            return result
        return [result] if isinstance(result, dict) else []
