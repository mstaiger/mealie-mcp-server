import logging
import traceback
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from mealie import MealieFetcher

logger = logging.getLogger("mealie-mcp")


def register_user_tools(mcp: FastMCP, mealie: MealieFetcher) -> None:
    """Register user-self-service MCP tools (profile, favorites, ratings)."""

    @mcp.tool()
    def get_current_user() -> Dict[str, Any]:
        """Get the profile of the currently authenticated user."""
        try:
            logger.info({"message": "Fetching current user"})
            return mealie.get_current_user()
        except Exception as e:
            error_msg = f"Error fetching current user: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_my_favorites() -> List[Dict[str, Any]]:
        """List the current user's favorite recipes."""
        try:
            logger.info({"message": "Fetching favorites"})
            return mealie.get_my_favorites()
        except Exception as e:
            error_msg = f"Error fetching favorites: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def add_favorite_recipe(
        recipe_slug: str, user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add a recipe to favorites.

        Args:
            recipe_slug: Slug of the recipe to favorite
            user_id: Target user's UUID (defaults to current user)
        """
        try:
            logger.info({"message": "Adding favorite", "slug": recipe_slug, "user_id": user_id})
            return mealie.add_favorite_recipe(recipe_slug, user_id=user_id)
        except Exception as e:
            error_msg = f"Error adding favorite '{recipe_slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def remove_favorite_recipe(
        recipe_slug: str, user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Remove a recipe from favorites."""
        try:
            logger.info({"message": "Removing favorite", "slug": recipe_slug, "user_id": user_id})
            return mealie.remove_favorite_recipe(recipe_slug, user_id=user_id)
        except Exception as e:
            error_msg = f"Error removing favorite '{recipe_slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_my_ratings() -> List[Dict[str, Any]]:
        """List the current user's recipe ratings."""
        try:
            logger.info({"message": "Fetching ratings"})
            return mealie.get_my_ratings()
        except Exception as e:
            error_msg = f"Error fetching ratings: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def get_my_rating_for_recipe(recipe_id: str) -> Dict[str, Any]:
        """Get the current user's rating for a specific recipe (by recipe UUID)."""
        try:
            logger.info({"message": "Fetching rating for recipe", "recipe_id": recipe_id})
            return mealie.get_my_rating_for_recipe(recipe_id)
        except Exception as e:
            error_msg = f"Error fetching rating for recipe '{recipe_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def rate_recipe(
        recipe_slug: str,
        rating: Optional[float] = None,
        is_favorite: Optional[bool] = None,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Set a numeric rating and/or favorite flag on a recipe.

        Args:
            recipe_slug: Slug of the recipe to rate
            rating: 0–5 (or None to clear)
            is_favorite: Favorite flag
            user_id: Target user's UUID (defaults to current user)
        """
        try:
            logger.info(
                {
                    "message": "Rating recipe",
                    "slug": recipe_slug,
                    "rating": rating,
                    "is_favorite": is_favorite,
                }
            )
            return mealie.rate_recipe(
                recipe_slug, rating=rating, is_favorite=is_favorite, user_id=user_id
            )
        except Exception as e:
            error_msg = f"Error rating recipe '{recipe_slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)
