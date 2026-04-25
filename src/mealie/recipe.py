import logging
import os
from typing import Any, Dict, List, Optional

from utils import format_api_params

logger = logging.getLogger("mealie-mcp")


class RecipeMixin:
    """Mixin class for recipe-related API endpoints"""

    def get_recipes(
        self,
        search: Optional[str] = None,
        order_by: Optional[str] = None,
        order_by_null_position: Optional[str] = None,
        order_direction: Optional[str] = "desc",
        query_filter: Optional[str] = None,
        pagination_seed: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        categories: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        tools: Optional[List[str]] = None,
        require_all_tags: Optional[bool] = None,
        require_all_categories: Optional[bool] = None,
        require_all_tools: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Provides paginated list of recipes

        Args:
            search: Search term to filter recipes by name, description, etc.
            order_by: Field to order results by
            order_by_null_position: How to handle nulls in ordering ('first' or 'last')
            order_direction: Direction to order results ('asc' or 'desc')
            query_filter: Advanced query filter
            pagination_seed: Seed for consistent pagination
            page: Page number to retrieve
            per_page: Number of items per page
            categories: List of category slugs (NOT names) to filter by
            tags: List of tag slugs or UUIDs (NOT display names) to filter by
            tools: List of tool slugs to filter by
            require_all_tags: If True, recipe must have ALL specified tags (AND logic). Default False (OR logic)
            require_all_categories: If True, recipe must have ALL specified categories (AND logic)
            require_all_tools: If True, recipe must have ALL specified tools (AND logic)

        Returns:
            JSON response containing recipe items and pagination information
        """

        param_dict = {
            "search": search,
            "orderBy": order_by,
            "orderByNullPosition": order_by_null_position,
            "orderDirection": order_direction,
            "queryFilter": query_filter,
            "paginationSeed": pagination_seed,
            "page": page,
            "perPage": per_page,
            "categories": categories,
            "tags": tags,
            "tools": tools,
            "requireAllTags": require_all_tags,
            "requireAllCategories": require_all_categories,
            "requireAllTools": require_all_tools,
        }

        params = format_api_params(param_dict)

        logger.info({"message": "Retrieving recipes", "parameters": params})
        return self._handle_request("GET", "/api/recipes", params=params)

    def get_recipe(self, slug: str) -> Dict[str, Any]:
        """Retrieve a specific recipe by its slug

        Args:
            slug: The slug identifier of the recipe to retrieve

        Returns:
            JSON response containing all recipe details
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")

        logger.info({"message": "Retrieving recipe", "slug": slug})
        return self._handle_request("GET", f"/api/recipes/{slug}")

    def update_recipe(self, slug: str, recipe_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a specific recipe by its slug

        Args:
            slug: The slug identifier of the recipe to update
            recipe_data: Dictionary containing the recipe properties to update

        Returns:
            JSON response containing the updated recipe details
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")
        if not recipe_data:
            raise ValueError("Recipe data cannot be empty")

        logger.info({"message": "Updating recipe", "slug": slug})
        return self._handle_request("PUT", f"/api/recipes/{slug}", json=recipe_data)

    def create_recipe(self, name: str) -> str:
        """Create a new recipe

        Args:
            name: The name of the new recipe

        Returns:
            Slug of the newly created recipe
        """
        logger.info({"message": "Creating new recipe", "name": name})
        return self._handle_request("POST", "/api/recipes", json={"name": name})

    def patch_recipe(self, slug: str, recipe_data: Dict[str, Any]) -> Dict[str, Any]:
        """Partially update a recipe (only updates provided fields)

        Args:
            slug: The slug identifier of the recipe to patch
            recipe_data: Dictionary containing only the fields to update

        Returns:
            JSON response containing the updated recipe details
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")
        if not recipe_data:
            raise ValueError("Recipe data cannot be empty")

        logger.info({"message": "Patching recipe", "slug": slug})
        return self._handle_request("PATCH", f"/api/recipes/{slug}", json=recipe_data)

    def update_recipe_ingredients(
        self, slug: str, ingredients: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Replace the structured recipeIngredient array on an existing recipe.

        Fetches the current recipe, swaps in the new ingredient list, and PUTs
        the full recipe back. Mealie's PATCH endpoint rejects partial bodies
        containing recipeIngredient with a masked 500 ValidationError, so we
        use PUT to stay on the validated path.

        Args:
            slug: The slug identifier of the recipe to update.
            ingredients: List of ingredient dicts matching Mealie's
                RecipeIngredient shape (quantity, unit, food, note, title,
                originalText, ...).

        Returns:
            JSON response containing the updated recipe details.
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")
        if ingredients is None:
            raise ValueError("Ingredients list cannot be None")

        logger.info(
            {
                "message": "Updating recipe ingredients",
                "slug": slug,
                "count": len(ingredients),
            }
        )
        current = self._handle_request("GET", f"/api/recipes/{slug}")
        current["recipeIngredient"] = ingredients
        return self._handle_request("PUT", f"/api/recipes/{slug}", json=current)

    def duplicate_recipe(self, slug: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Duplicate an existing recipe

        Args:
            slug: The slug identifier of the recipe to duplicate
            name: Optional new name for the duplicate (defaults to original name + copy indicator)

        Returns:
            JSON response containing the newly created duplicate recipe
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")

        payload = {}
        if name:
            payload["name"] = name

        logger.info({"message": "Duplicating recipe", "slug": slug})
        return self._handle_request("POST", f"/api/recipes/{slug}/duplicate", json=payload)

    def update_recipe_last_made(self, slug: str, timestamp: Optional[str] = None) -> Dict[str, Any]:
        """Update the last made timestamp for a recipe

        Args:
            slug: The slug identifier of the recipe
            timestamp: ISO format timestamp (if None, uses current time)

        Returns:
            JSON response containing the updated recipe
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")

        # If no timestamp provided, use current time
        if not timestamp:
            from datetime import datetime
            timestamp = datetime.utcnow().isoformat() + "Z"

        payload = {"timestamp": timestamp}

        logger.info({"message": "Updating recipe last made", "slug": slug})
        return self._handle_request("PATCH", f"/api/recipes/{slug}/last-made", json=payload)

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
        return self._handle_request("POST", f"/api/recipes/{slug}/image", json=payload)

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

        # Mealie's PUT /recipes/{slug}/image requires both the file and a separate
        # form field naming the file extension (e.g. "png", "jpg").
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
        return self._handle_request(
            "PUT", f"/api/recipes/{slug}/image", files=files, data=data
        )

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

    def delete_recipe(self, slug: str) -> Dict[str, Any]:
        """Delete a recipe

        Args:
            slug: The slug identifier of the recipe to delete

        Returns:
            JSON response confirming deletion
        """
        if not slug:
            raise ValueError("Recipe slug cannot be empty")

        logger.info({"message": "Deleting recipe", "slug": slug})
        return self._handle_request("DELETE", f"/api/recipes/{slug}")

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
    ) -> Dict[str, Any]:
        """Attach categories to many recipes at once.

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
        return self._handle_request(
            "POST", "/api/recipes/bulk-actions/categorize", json=payload
        )

    def bulk_tag_recipes(
        self, recipe_slugs: List[str], tags: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Attach tags to many recipes at once.

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
        return self._handle_request(
            "POST", "/api/recipes/bulk-actions/tag", json=payload
        )

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

    def update_recipes_batch(self, recipes: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        return self._handle_request("PUT", "/api/recipes", json=recipes)

    def patch_recipes_batch(self, recipes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Partial-update many recipes in a single call (PATCH /api/recipes).

        Each entry must carry enough identifying info (slug and/or id) plus
        the fields to change. Unspecified fields are left alone.
        """
        if not recipes:
            raise ValueError("recipes cannot be empty")

        logger.info({"message": "Batch-patching recipes", "count": len(recipes)})
        return self._handle_request("PATCH", "/api/recipes", json=recipes)
