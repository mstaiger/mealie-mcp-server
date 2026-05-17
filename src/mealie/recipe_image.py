import logging
import os
from typing import Any, Dict, Optional

logger = logging.getLogger("mealie-mcp")


class RecipeImageMixin:
    """Recipe image and asset upload operations."""

    def _get_recipe_image_url(self, slug: str) -> Optional[str]:
        """Look up a recipe's viewable image URL by slug.

        Returns the full URL or None if the recipe has no image or lookup fails.
        """
        try:
            recipe = self.get_recipe(slug)
            recipe_id = recipe.get("id")
            if recipe_id:
                base = str(self._client.base_url).rstrip("/")
                return f"{base}/api/media/recipes/{recipe_id}/images/original.webp"
        except Exception:
            logger.debug({"message": "Could not resolve image URL", "slug": slug})
        return None

    def scrape_recipe_image_from_url(self, slug: str, image_url: str) -> Dict[str, Any]:
        """Scrape and set a recipe's image from a URL (JSON payload)

        Args:
            slug: The slug identifier of the recipe
            image_url: URL of the image to scrape

        Returns:
            JSON response confirming the image was set
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")
        if not image_url:
            raise ValueError("Image URL cannot be empty")

        payload = {"url": image_url}

        logger.info({"message": "Scraping recipe image from URL", "slug": slug, "url": image_url})
        result = self._handle_request("POST", f"/api/recipes/{slug}/image", json=payload)

        if isinstance(result, dict):
            image_view_url = self._get_recipe_image_url(slug)
            if image_view_url:
                result["image_url"] = image_view_url

        return result

    def upload_recipe_image(self, slug: str, image_data: bytes, filename: str) -> Dict[str, Any]:
        """Upload a recipe image file (multipart upload)

        Args:
            slug: The slug identifier of the recipe
            image_data: Binary image data
            filename: Name of the image file

        Returns:
            JSON response confirming the image was uploaded
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")
        if not image_data:
            raise ValueError("Image data cannot be empty")
        if not filename:
            raise ValueError("Filename cannot be empty")

        _, ext = os.path.splitext(filename)
        extension = ext.lstrip(".").lower()
        if not extension:
            raise ValueError(f"Cannot determine image extension from filename: {filename!r}")

        files = {"image": (filename, image_data)}
        data = {"extension": extension}

        logger.info(
            {
                "message": "Uploading recipe image",
                "slug": slug,
                "filename": filename,
                "extension": extension,
            }
        )
        result = self._handle_request(
            "PUT", f"/api/recipes/{slug}/image", files=files, data=data
        )

        if isinstance(result, dict):
            image_view_url = self._get_recipe_image_url(slug)
            if image_view_url:
                result["image_url"] = image_view_url

        return result

    def upload_recipe_asset(self, slug: str, asset_data: bytes, filename: str) -> Dict[str, Any]:
        """Upload a recipe asset file (multipart upload)

        Args:
            slug: The slug identifier of the recipe
            asset_data: Binary asset data
            filename: Name of the asset file

        Returns:
            JSON response containing the uploaded asset details
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")
        if not asset_data:
            raise ValueError("Asset data cannot be empty")
        if not filename:
            raise ValueError("Filename cannot be empty")

        files = {"file": (filename, asset_data)}

        logger.info({"message": "Uploading recipe asset", "slug": slug, "filename": filename})
        return self._handle_request("POST", f"/api/recipes/{slug}/assets", files=files)
