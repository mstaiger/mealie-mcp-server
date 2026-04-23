import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("mealie-mcp")


class UserMixin:
    """Mixin class for user-related API endpoints."""

    def get_current_user(self) -> Dict[str, Any]:
        """Get information about the currently logged in user."""
        logger.info({"message": "Retrieving current user information"})
        return self._handle_request("GET", "/api/users/self")

    def get_my_favorites(self) -> List[Dict[str, Any]]:
        """Get the current user's favorite recipes."""
        logger.info({"message": "Retrieving current user's favorites"})
        return self._handle_request("GET", "/api/users/self/favorites")

    def get_user_favorites(self, user_id: str) -> List[Dict[str, Any]]:
        """Get a specific user's favorites (by user UUID)."""
        if not user_id:
            raise ValueError("user_id cannot be empty")

        logger.info({"message": "Retrieving user favorites", "user_id": user_id})
        return self._handle_request("GET", f"/api/users/{user_id}/favorites")

    def add_favorite_recipe(self, recipe_slug: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Add a recipe to favorites.

        Args:
            recipe_slug: Slug of the recipe to favorite
            user_id: Target user's UUID. If omitted, resolves to the current user.
        """
        if not recipe_slug:
            raise ValueError("recipe_slug cannot be empty")

        if user_id is None:
            user_id = self.get_current_user()["id"]

        logger.info(
            {"message": "Adding favorite recipe", "user_id": user_id, "slug": recipe_slug}
        )
        return self._handle_request(
            "POST", f"/api/users/{user_id}/favorites/{recipe_slug}"
        )

    def remove_favorite_recipe(
        self, recipe_slug: str, user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Remove a recipe from favorites."""
        if not recipe_slug:
            raise ValueError("recipe_slug cannot be empty")

        if user_id is None:
            user_id = self.get_current_user()["id"]

        logger.info(
            {"message": "Removing favorite recipe", "user_id": user_id, "slug": recipe_slug}
        )
        return self._handle_request(
            "DELETE", f"/api/users/{user_id}/favorites/{recipe_slug}"
        )

    def get_my_ratings(self) -> List[Dict[str, Any]]:
        """Get the current user's recipe ratings."""
        logger.info({"message": "Retrieving current user's ratings"})
        return self._handle_request("GET", "/api/users/self/ratings")

    def get_my_rating_for_recipe(self, recipe_id: str) -> Dict[str, Any]:
        """Get the current user's rating for a specific recipe.

        Args:
            recipe_id: Recipe UUID (not slug).
        """
        if not recipe_id:
            raise ValueError("recipe_id cannot be empty")

        logger.info({"message": "Retrieving user's rating for recipe", "recipe_id": recipe_id})
        return self._handle_request("GET", f"/api/users/self/ratings/{recipe_id}")

    def get_user_ratings(self, user_id: str) -> List[Dict[str, Any]]:
        """Get a specific user's ratings (by user UUID)."""
        if not user_id:
            raise ValueError("user_id cannot be empty")

        logger.info({"message": "Retrieving user ratings", "user_id": user_id})
        return self._handle_request("GET", f"/api/users/{user_id}/ratings")

    def rate_recipe(
        self,
        recipe_slug: str,
        rating: Optional[float] = None,
        is_favorite: Optional[bool] = None,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Set a rating and/or favorite flag on a recipe.

        Args:
            recipe_slug: Slug of the recipe to rate
            rating: Numeric rating (Mealie expects 0–5; pass None to clear)
            is_favorite: Optional favorite flag
            user_id: Target user's UUID. Defaults to current user.
        """
        if not recipe_slug:
            raise ValueError("recipe_slug cannot be empty")
        if rating is None and is_favorite is None:
            raise ValueError("At least one of rating or is_favorite must be provided")

        if user_id is None:
            user_id = self.get_current_user()["id"]

        payload: Dict[str, Any] = {}
        if rating is not None:
            payload["rating"] = rating
        if is_favorite is not None:
            payload["isFavorite"] = is_favorite

        logger.info(
            {
                "message": "Rating recipe",
                "user_id": user_id,
                "slug": recipe_slug,
                "rating": rating,
                "is_favorite": is_favorite,
            }
        )
        return self._handle_request(
            "POST", f"/api/users/{user_id}/ratings/{recipe_slug}", json=payload
        )
