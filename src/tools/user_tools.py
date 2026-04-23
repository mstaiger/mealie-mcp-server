import logging
import os
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

    @mcp.tool()
    def change_password(new_password: str, current_password: str = "") -> Dict[str, Any]:
        """Change the current user's password (minimum 8 characters).

        Args:
            new_password: New password, minimum 8 characters
            current_password: Current password (required when one is set;
                safe to leave empty for OAuth-only accounts)
        """
        try:
            logger.info({"message": "Changing password"})
            return mealie.change_password(
                new_password=new_password, current_password=current_password
            )
        except Exception as e:
            error_msg = f"Error changing password: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def forgot_password(email: str) -> Dict[str, Any]:
        """Send a password-reset email to the given address."""
        try:
            logger.info({"message": "Initiating password reset", "email": email})
            return mealie.forgot_password(email)
        except Exception as e:
            error_msg = f"Error initiating password reset: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def reset_password(
        token: str, email: str, password: str, password_confirm: str
    ) -> Dict[str, Any]:
        """Complete a password reset using the token from the reset email."""
        try:
            logger.info({"message": "Completing password reset", "email": email})
            return mealie.reset_password(
                token=token,
                email=email,
                password=password,
                password_confirm=password_confirm,
            )
        except Exception as e:
            error_msg = f"Error completing password reset: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def create_api_token(name: str, integration_id: str = "generic") -> Dict[str, Any]:
        """Create a long-lived API token for the current user.

        Args:
            name: Human-friendly name for the token
            integration_id: Free-form tag identifying the consumer (default "generic")

        Returns:
            The token value is returned ONLY in this response — save it now.
            Later GETs will not expose it.
        """
        try:
            logger.info({"message": "Creating API token", "name": name})
            return mealie.create_api_token(name=name, integration_id=integration_id)
        except Exception as e:
            error_msg = f"Error creating API token '{name}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def delete_api_token(token_id: int) -> Dict[str, Any]:
        """Revoke a long-lived API token by its integer ID."""
        try:
            logger.info({"message": "Deleting API token", "token_id": token_id})
            return mealie.delete_api_token(token_id)
        except Exception as e:
            error_msg = f"Error deleting API token '{token_id}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def upload_profile_image(
        image_path: str,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Upload a user profile image from a filesystem path.

        Args:
            image_path: Path to an image file on disk.
            user_id: Target user's UUID (defaults to current user).
        """
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()
            filename = os.path.basename(image_path)
            logger.info(
                {"message": "Uploading profile image", "path": image_path, "user_id": user_id}
            )
            return mealie.upload_profile_image(
                image_data=image_data, filename=filename, user_id=user_id
            )
        except Exception as e:
            error_msg = f"Error uploading profile image '{image_path}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)
