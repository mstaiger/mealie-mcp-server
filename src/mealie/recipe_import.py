import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("mealie-mcp")


class RecipeImportMixin:
    """Recipe import and ingredient parsing operations."""

    def parse_ingredient(self, ingredient: str) -> Dict[str, Any]:
        """Parse a single ingredient string into structured quantity/unit/food fields.

        Args:
            ingredient: The ingredient string to parse (e.g. "2 cups all-purpose flour")

        Returns:
            JSON response with parsed ingredient fields (quantity, unit, food, etc.)
        """
        if not ingredient:
            raise ValueError("Ingredient string cannot be empty")

        logger.info({"message": "Parsing ingredient", "ingredient": ingredient})
        return self._handle_request(
            "POST", "/api/parser/ingredient", json={"ingredient": ingredient}
        )

    def parse_ingredients(self, ingredients: List[str]) -> List[Dict[str, Any]]:
        """Parse multiple ingredient strings into structured quantity/unit/food fields.

        Args:
            ingredients: List of ingredient strings to parse

        Returns:
            JSON response with list of parsed ingredient objects
        """
        if not ingredients:
            raise ValueError("Ingredients list cannot be empty")

        logger.info({"message": "Parsing ingredients", "count": len(ingredients)})
        return self._handle_request(
            "POST",
            "/api/parser/ingredients",
            json={"ingredients": ingredients},
        )

    def import_recipe_from_url(self, url: str, include_tags: bool = False) -> str:
        """Scrape a recipe from a URL and save it to the database.

        Args:
            url: The source URL to scrape
            include_tags: If True, attempt to import tags from the scraped page

        Returns:
            The slug of the newly created recipe (Mealie returns it as a bare JSON string).
        """
        if not url:
            raise ValueError("url cannot be empty")

        payload = {"url": url, "includeTags": include_tags}
        logger.info({"message": "Importing recipe from URL", "url": url})
        return self._handle_request("POST", "/api/recipes/create/url", json=payload)

    def import_recipes_from_urls(
        self, imports: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Scrape multiple recipes from URLs (async bulk import).

        Args:
            imports: List of dicts matching CreateRecipeBulk. Each must have
                a ``url`` key; may optionally include ``categories`` and
                ``tags`` (lists of RecipeCategory / RecipeTag objects).

        Returns:
            JSON response from Mealie acknowledging the bulk import (202 Accepted).
        """
        if not imports:
            raise ValueError("imports list cannot be empty")

        payload = {"imports": imports}
        logger.info({"message": "Bulk-importing recipes from URLs", "count": len(imports)})
        return self._handle_request("POST", "/api/recipes/create/url/bulk", json=payload)

    def test_recipe_scrape(self, url: str, use_openai: bool = False) -> Dict[str, Any]:
        """Dry-run a recipe scrape to preview results without saving.

        Args:
            url: The source URL to scrape
            use_openai: If True, use Mealie's OpenAI-assisted scraping (if configured)

        Returns:
            JSON response with the scraped-but-not-saved recipe structure.
        """
        if not url:
            raise ValueError("url cannot be empty")

        payload = {"url": url, "useOpenAI": use_openai}
        logger.info({"message": "Testing recipe scrape", "url": url, "use_openai": use_openai})
        return self._handle_request(
            "POST", "/api/recipes/test-scrape-url", json=payload
        )

    def import_recipe_from_html_or_json(
        self, data: str, include_tags: bool = False
    ) -> Dict[str, Any]:
        """Create a recipe from raw HTML or a schema.org/Recipe JSON string.

        Args:
            data: Raw HTML source of a recipe page, OR a JSON-encoded
                schema.org/Recipe object (as a string, not a dict).
            include_tags: If True, attempt to import tags.
        """
        if not data:
            raise ValueError("data cannot be empty")

        payload = {"data": data, "includeTags": include_tags}
        logger.info(
            {"message": "Importing recipe from HTML/JSON", "size": len(data)}
        )
        return self._handle_request(
            "POST", "/api/recipes/create/html-or-json", json=payload
        )

    def import_recipe_from_zip(
        self, archive_data: bytes, filename: str
    ) -> Dict[str, Any]:
        """Create a recipe from a Mealie ZIP archive (multipart upload).

        Args:
            archive_data: Binary contents of the ZIP
            filename: Original filename (used as the multipart field name)
        """
        if not archive_data:
            raise ValueError("archive_data cannot be empty")
        if not filename:
            raise ValueError("filename cannot be empty")

        files = {"archive": (filename, archive_data)}
        logger.info(
            {
                "message": "Importing recipe from ZIP",
                "filename": filename,
                "size": len(archive_data),
            }
        )
        return self._handle_request(
            "POST", "/api/recipes/create/zip", files=files
        )

    def import_recipe_from_image(
        self,
        images: List[Dict[str, Any]],
        translate_language: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a recipe from one or more images via Mealie's OpenAI OCR flow.

        Args:
            images: List of dicts each with ``filename`` (str) and ``data`` (bytes).
            translate_language: Optional language code for translated output (e.g. "en").
        """
        if not images:
            raise ValueError("images cannot be empty")

        files = [
            ("images", (img["filename"], img["data"]))
            for img in images
        ]
        params = {}
        if translate_language is not None:
            params["translateLanguage"] = translate_language

        logger.info(
            {
                "message": "Importing recipe from image",
                "count": len(images),
                "translate": translate_language,
            }
        )
        return self._handle_request(
            "POST",
            "/api/recipes/create/image",
            files=files,
            params=params or None,
        )
