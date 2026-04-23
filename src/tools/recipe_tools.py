import logging
import traceback
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from mealie import MealieFetcher
from models.recipe import Recipe, RecipeIngredient, RecipeInstruction

logger = logging.getLogger("mealie-mcp")


def _normalize_ingredient_for_write(ingredient: Dict[str, Any]) -> Dict[str, Any]:
    """Strip food/unit objects whose id is null — Mealie's write path rejects
    them with a ValueError. Fold the stripped names into `note` so the
    ingredient still renders readably.
    """
    result = dict(ingredient)
    note_parts: List[str] = []

    unit = result.get("unit")
    if isinstance(unit, dict) and not unit.get("id"):
        name = unit.get("name")
        if name:
            note_parts.append(str(name))
        result["unit"] = None

    food = result.get("food")
    if isinstance(food, dict) and not food.get("id"):
        name = food.get("name")
        if name:
            note_parts.append(str(name))
        result["food"] = None

    if note_parts:
        existing = result.get("note") or ""
        combined = " ".join(note_parts)
        result["note"] = f"{combined} {existing}".strip() if existing else combined

    return result


def register_recipe_tools(mcp: FastMCP, mealie: MealieFetcher) -> None:
    """Register all recipe-related tools with the MCP server."""

    @mcp.tool()
    def get_recipes(
        search: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        categories: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        require_all_tags: Optional[bool] = None,
        require_all_categories: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Provides a paginated list of recipes with optional filtering.

        IMPORTANT: When filtering by tags or categories, you MUST use slugs or UUIDs, NOT display names!
        - ✅ Correct: tags=["quick-meals", "vegetarian"]
        - ❌ Wrong: tags=["Quick Meals", "Vegetarian"]

        Use get_tags() or get_categories() first to find the correct slugs.

        Args:
            search: Filters recipes by name or description.
            page: Page number for pagination.
            per_page: Number of items per page.
            categories: Filter by category SLUGS (e.g., ["breakfast", "dinner"]).
            tags: Filter by tag SLUGS or UUIDs (e.g., ["quick", "healthy"]).
            require_all_tags: If True, recipe must have ALL specified tags (AND). Default False (OR).
            require_all_categories: If True, recipe must have ALL specified categories (AND).

        Returns:
            Dict[str, Any]: Recipe summaries with details like ID, name, description, and image information.
        """
        try:
            logger.info(
                {
                    "message": "Fetching recipes",
                    "search": search,
                    "page": page,
                    "per_page": per_page,
                    "categories": categories,
                    "tags": tags,
                    "require_all_tags": require_all_tags,
                    "require_all_categories": require_all_categories,
                }
            )
            return mealie.get_recipes(
                search=search,
                page=page,
                per_page=per_page,
                categories=categories,
                tags=tags,
                require_all_tags=require_all_tags,
                require_all_categories=require_all_categories,
            )
        except Exception as e:
            error_msg = f"Error fetching recipes: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug(
                {"message": "Error traceback", "traceback": traceback.format_exc()}
            )
            raise ToolError(error_msg)

    @mcp.tool()
    def get_recipe_detailed(slug: str) -> Dict[str, Any]:
        """Retrieve a specific recipe by its slug identifier. Use this when to get full recipe
        details for tasks like updating or displaying the recipe.

        Args:
            slug: The unique text identifier for the recipe, typically found in recipe URLs
                or from get_recipes results.

        Returns:
            Dict[str, Any]: Comprehensive recipe details including ingredients, instructions,
                nutrition information, notes, and associated metadata.
        """
        try:
            logger.info({"message": "Fetching recipe", "slug": slug})
            return mealie.get_recipe(slug)
        except Exception as e:
            error_msg = f"Error fetching recipe with slug '{slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug(
                {"message": "Error traceback", "traceback": traceback.format_exc()}
            )
            raise ToolError(error_msg)

    @mcp.tool()
    def get_recipe_concise(slug: str) -> Dict[str, Any]:
        """Retrieve a concise version of a specific recipe by its slug identifier. Use this when you only
        need a summary of the recipe, such as for when mealplaning.

        Args:
            slug: The unique text identifier for the recipe, typically found in recipe URLs
                or from get_recipes results.

        Returns:
            Dict[str, Any]: Concise recipe summary with essential fields.
        """
        try:
            logger.info({"message": "Fetching recipe", "slug": slug})
            recipe_json = mealie.get_recipe(slug)
            recipe = Recipe.model_validate(recipe_json)
            return recipe.model_dump(
                include={
                    "name",
                    "slug",
                    "recipeServings",
                    "recipeYieldQuantity",
                    "recipeYield",
                    "totalTime",
                    "rating",
                    "recipeIngredient",
                    "lastMade",
                },
                exclude_none=True,
            )
        except Exception as e:
            error_msg = f"Error fetching recipe with slug '{slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug(
                {"message": "Error traceback", "traceback": traceback.format_exc()}
            )
            raise ToolError(error_msg)

    @mcp.tool()
    def create_recipe(
        name: str, ingredients: List[str], instructions: List[str]
    ) -> Dict[str, Any]:
        """Create a new recipe

        Args:
            name: The name of the new recipe to be created.
            ingredients: A list of ingredients for the recipe include quantities and units.
            instructions: A list of instructions for preparing the recipe.

        Returns:
            Dict[str, Any]: The created recipe details.
        """
        try:
            logger.info({"message": "Creating recipe", "name": name})
            slug = mealie.create_recipe(name)
            recipe_json = mealie.get_recipe(slug)
            recipe = Recipe.model_validate(recipe_json)
            recipe.recipeIngredient = [RecipeIngredient(note=i) for i in ingredients]
            recipe.recipeInstructions = [
                RecipeInstruction(text=i) for i in instructions
            ]
            return mealie.update_recipe(slug, recipe.model_dump(exclude_none=True))
        except Exception as e:
            error_msg = f"Error creating recipe '{name}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug(
                {"message": "Error traceback", "traceback": traceback.format_exc()}
            )
            raise ToolError(error_msg)

    @mcp.tool()
    def update_recipe(
        slug: str,
        ingredients: List[str],
        instructions: List[str],
    ) -> Dict[str, Any]:
        """Replaces the ingredients and instructions of an existing recipe.

        Args:
            slug: The unique text identifier for the recipe to be updated.
            ingredients: A list of ingredients for the recipe include quantities and units.
            instructions: A list of instructions for preparing the recipe.

        Returns:
            Dict[str, Any]: The updated recipe details.
        """
        try:
            logger.info({"message": "Updating recipe", "slug": slug})
            recipe_json = mealie.get_recipe(slug)
            recipe = Recipe.model_validate(recipe_json)
            recipe.recipeIngredient = [RecipeIngredient(note=i) for i in ingredients]
            recipe.recipeInstructions = [
                RecipeInstruction(text=i) for i in instructions
            ]
            return mealie.update_recipe(slug, recipe.model_dump(exclude_none=True))
        except Exception as e:
            error_msg = f"Error updating recipe '{slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug(
                {"message": "Error traceback", "traceback": traceback.format_exc()}
            )
            raise ToolError(error_msg)

    @mcp.tool()
    def patch_recipe(
        slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        recipe_yield: Optional[str] = None,
        total_time: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Partially update a recipe (only updates provided fields).

        Args:
            slug: The unique text identifier for the recipe to be updated.
            name: New name for the recipe (optional)
            description: New description for the recipe (optional)
            recipe_yield: New yield/servings for the recipe (optional)
            total_time: New total time for the recipe (optional)

        Returns:
            Dict[str, Any]: The updated recipe details.
        """
        try:
            logger.info({"message": "Patching recipe", "slug": slug})

            recipe_data = {}
            if name is not None:
                recipe_data["name"] = name
            if description is not None:
                recipe_data["description"] = description
            if recipe_yield is not None:
                recipe_data["recipeYield"] = recipe_yield
            if total_time is not None:
                recipe_data["totalTime"] = total_time

            if not recipe_data:
                raise ValueError("At least one field must be provided to update")

            return mealie.patch_recipe(slug, recipe_data)
        except Exception as e:
            error_msg = f"Error patching recipe '{slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def update_recipe_ingredients(
        slug: str,
        ingredients: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Replace a recipe's structured ingredient list with parsed fields
        (quantity, unit, food). Typical flow: call parse_ingredients on
        free-text strings, then pass the returned dicts here. Fetches the
        current recipe, swaps in the new ingredients, and PUTs — other
        recipe fields are preserved.

        Food/unit objects whose `id` is null are stripped before sending:
        Mealie's write path rejects food/unit references without a resolved
        UUID. The food/unit name is folded into the ingredient's `note` so
        the ingredient still renders readably. To keep the structured
        reference, create the Food/Unit via Mealie's admin endpoints first
        and pass its UUID in `food.id` / `unit.id`.

        Args:
            slug: The unique text identifier for the recipe to update.
            ingredients: List of ingredient dicts. Accepted shape matches
                Mealie's RecipeIngredient: quantity (float|None),
                unit ({id, name, ...}|None), food ({id, name, ...}|None),
                note (str|None), title (str|None), originalText (str|None),
                disableAmount (bool), isFood (bool).

        Returns:
            Dict[str, Any]: The updated recipe details.
        """
        try:
            logger.info(
                {
                    "message": "Updating recipe ingredients",
                    "slug": slug,
                    "count": len(ingredients),
                }
            )
            validated = [
                _normalize_ingredient_for_write(
                    RecipeIngredient.model_validate(i).model_dump(
                        exclude_none=True, by_alias=True
                    )
                )
                for i in ingredients
            ]
            return mealie.update_recipe_ingredients(slug, validated)
        except Exception as e:
            error_msg = f"Error updating recipe ingredients '{slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug(
                {"message": "Error traceback", "traceback": traceback.format_exc()}
            )
            raise ToolError(error_msg)

    @mcp.tool()
    def duplicate_recipe(slug: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Duplicate an existing recipe, creating a copy with a new slug.

        Args:
            slug: The unique text identifier for the recipe to duplicate.
            name: Optional new name for the duplicate (if not provided, uses original name with copy indicator).

        Returns:
            Dict[str, Any]: The newly created duplicate recipe details.
        """
        try:
            logger.info({"message": "Duplicating recipe", "slug": slug, "name": name})
            return mealie.duplicate_recipe(slug, name)
        except Exception as e:
            error_msg = f"Error duplicating recipe '{slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def mark_recipe_last_made(slug: str) -> Dict[str, Any]:
        """Mark a recipe as having been made today (updates last made timestamp).

        Args:
            slug: The unique text identifier for the recipe.

        Returns:
            Dict[str, Any]: The updated recipe details.
        """
        try:
            logger.info({"message": "Marking recipe as last made", "slug": slug})
            return mealie.update_recipe_last_made(slug)
        except Exception as e:
            error_msg = f"Error updating recipe last made '{slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def set_recipe_image_from_url(slug: str, image_url: str) -> Dict[str, Any]:
        """Set a recipe's image by scraping it from a URL.

        Args:
            slug: The unique text identifier for the recipe.
            image_url: URL of the image to scrape and use as the recipe image.

        Returns:
            Dict[str, Any]: Confirmation that the image was set.
        """
        try:
            logger.info({"message": "Setting recipe image from URL", "slug": slug, "url": image_url})
            return mealie.scrape_recipe_image_from_url(slug, image_url)
        except Exception as e:
            error_msg = f"Error setting recipe image from URL '{slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def upload_recipe_image_file(slug: str, image_path: str) -> Dict[str, Any]:
        """Upload an image file for a recipe.

        Args:
            slug: The unique text identifier for the recipe.
            image_path: Local file path to the image to upload.

        Returns:
            Dict[str, Any]: Confirmation that the image was uploaded.
        """
        try:
            import os

            logger.info({"message": "Uploading recipe image", "slug": slug, "path": image_path})

            if not os.path.exists(image_path):
                raise ValueError(f"Image file not found: {image_path}")

            with open(image_path, "rb") as f:
                image_data = f.read()

            filename = os.path.basename(image_path)
            return mealie.upload_recipe_image(slug, image_data, filename)
        except Exception as e:
            error_msg = f"Error uploading recipe image '{slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def upload_recipe_asset_file(slug: str, asset_path: str) -> Dict[str, Any]:
        """Upload an asset file (document, PDF, etc.) for a recipe.

        Args:
            slug: The unique text identifier for the recipe.
            asset_path: Local file path to the asset to upload.

        Returns:
            Dict[str, Any]: Details of the uploaded asset.
        """
        try:
            import os

            logger.info({"message": "Uploading recipe asset", "slug": slug, "path": asset_path})

            if not os.path.exists(asset_path):
                raise ValueError(f"Asset file not found: {asset_path}")

            with open(asset_path, "rb") as f:
                asset_data = f.read()

            filename = os.path.basename(asset_path)
            return mealie.upload_recipe_asset(slug, asset_data, filename)
        except Exception as e:
            error_msg = f"Error uploading recipe asset '{slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def parse_ingredient(ingredient: str) -> Dict[str, Any]:
        """Parse a single ingredient string into structured quantity/unit/food fields
        using Mealie's NLP parser.

        Args:
            ingredient: The ingredient string to parse (e.g. "2 cups all-purpose flour").

        Returns:
            Dict[str, Any]: Parsed ingredient with quantity, unit, food, and other fields.
        """
        try:
            logger.info({"message": "Parsing ingredient", "ingredient": ingredient})
            return mealie.parse_ingredient(ingredient)
        except Exception as e:
            error_msg = f"Error parsing ingredient '{ingredient}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug(
                {"message": "Error traceback", "traceback": traceback.format_exc()}
            )
            raise ToolError(error_msg)

    @mcp.tool()
    def parse_ingredients(ingredients: List[str]) -> List[Dict[str, Any]]:
        """Parse multiple ingredient strings into structured quantity/unit/food fields
        using Mealie's NLP parser. More efficient than calling parse_ingredient one at a time.

        Args:
            ingredients: List of ingredient strings to parse.

        Returns:
            List[Dict[str, Any]]: List of parsed ingredients with quantity, unit, food, and other fields.
        """
        try:
            logger.info({"message": "Parsing ingredients", "count": len(ingredients)})
            return mealie.parse_ingredients(ingredients)
        except Exception as e:
            error_msg = f"Error parsing ingredients: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug(
                {"message": "Error traceback", "traceback": traceback.format_exc()}
            )
            raise ToolError(error_msg)

    @mcp.tool()
    def parse_recipe_ingredients(
        slug: str,
        skip_parsed: bool = True,
    ) -> Dict[str, Any]:
        """Parse a recipe's ingredient text into structured quantity/unit/food
        fields using Mealie's NLP parser and update the recipe in place.

        Fetches the recipe, extracts the best available text for each
        ingredient (originalText > display > note > reconstructed), runs
        them through the parser in a single batch, and writes the
        structured results back via PUT. Section headers (ingredients
        with only a title) are preserved as-is.

        Args:
            slug: The unique text identifier for the recipe.
            skip_parsed: If True (default), skip ingredients that already
                have a resolved food.id. Set False to re-parse every
                ingredient (useful when the parser has learned new
                foods/units since the last run).

        Returns:
            Dict[str, Any]: Summary with slug, parsed_count, skipped_count,
                total_count, and the updated recipe (or a message when
                nothing needed parsing).
        """
        try:
            logger.info(
                {
                    "message": "Parsing recipe ingredients",
                    "slug": slug,
                    "skip_parsed": skip_parsed,
                }
            )

            recipe = mealie.get_recipe(slug)
            ingredients = list(recipe.get("recipeIngredient") or [])
            total_count = len(ingredients)

            if total_count == 0:
                return {
                    "slug": slug,
                    "parsed_count": 0,
                    "skipped_count": 0,
                    "total_count": 0,
                    "message": "Recipe has no ingredients to parse",
                }

            texts_to_parse: List[str] = []
            parse_indices: List[int] = []

            for idx, ing in enumerate(ingredients):
                food = ing.get("food") if isinstance(ing.get("food"), dict) else None
                unit = ing.get("unit") if isinstance(ing.get("unit"), dict) else None

                # Section header: only has a title, nothing parseable
                is_section_header = (
                    ing.get("title")
                    and not ing.get("originalText")
                    and not ing.get("note")
                    and not food
                )
                if is_section_header:
                    continue

                if skip_parsed and food and food.get("id"):
                    continue

                text = ing.get("originalText") or ing.get("display") or ing.get("note")
                if not text:
                    parts: List[str] = []
                    if ing.get("quantity") is not None:
                        parts.append(str(ing["quantity"]))
                    if unit and unit.get("name"):
                        parts.append(unit["name"])
                    if food and food.get("name"):
                        parts.append(food["name"])
                    if ing.get("note"):
                        parts.append(ing["note"])
                    text = " ".join(parts) if parts else None

                if not text or not text.strip():
                    continue

                texts_to_parse.append(text.strip())
                parse_indices.append(idx)

            if not texts_to_parse:
                return {
                    "slug": slug,
                    "parsed_count": 0,
                    "skipped_count": total_count,
                    "total_count": total_count,
                    "message": "No unparsed ingredients found",
                }

            parsed_results = mealie.parse_ingredients(texts_to_parse)

            if len(parsed_results) != len(texts_to_parse):
                logger.warning(
                    {
                        "message": "Parser result count mismatch",
                        "expected": len(texts_to_parse),
                        "got": len(parsed_results),
                    }
                )

            parsed_count = 0
            for i, parsed in enumerate(parsed_results):
                if i >= len(parse_indices):
                    break
                # Mealie's parser wraps each result as {confidence, ingredient, input}
                if isinstance(parsed, dict) and "ingredient" in parsed:
                    merged = dict(parsed["ingredient"])
                elif isinstance(parsed, dict):
                    merged = dict(parsed)
                else:
                    continue

                target_idx = parse_indices[i]
                original = ingredients[target_idx]

                for key in ("title", "referenceId", "isFood", "disableAmount"):
                    if original.get(key) is not None:
                        merged[key] = original[key]

                if not merged.get("originalText"):
                    merged["originalText"] = texts_to_parse[i]

                ingredients[target_idx] = merged
                parsed_count += 1

            validated = [
                _normalize_ingredient_for_write(
                    RecipeIngredient.model_validate(ing).model_dump(
                        exclude_none=True, by_alias=True
                    )
                )
                for ing in ingredients
            ]

            updated_recipe = mealie.update_recipe_ingredients(slug, validated)

            return {
                "slug": slug,
                "parsed_count": parsed_count,
                "skipped_count": total_count - parsed_count,
                "total_count": total_count,
                "recipe": updated_recipe,
            }
        except Exception as e:
            error_msg = f"Error parsing recipe ingredients '{slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug(
                {"message": "Error traceback", "traceback": traceback.format_exc()}
            )
            raise ToolError(error_msg)

    @mcp.tool()
    def delete_recipe(slug: str) -> Dict[str, Any]:
        """Delete a recipe permanently.

        Args:
            slug: The unique text identifier for the recipe to delete.

        Returns:
            Dict[str, Any]: Confirmation of deletion.
        """
        try:
            logger.info({"message": "Deleting recipe", "slug": slug})
            return mealie.delete_recipe(slug)
        except Exception as e:
            error_msg = f"Error deleting recipe '{slug}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def import_recipe_from_url(url: str, include_tags: bool = False) -> str:
        """Scrape a recipe from a URL and save it to the database.

        Args:
            url: The source URL to scrape.
            include_tags: If True, attempt to import tags from the scraped page.

        Returns:
            The slug of the newly created recipe.
        """
        try:
            logger.info({"message": "Importing recipe from URL", "url": url})
            return mealie.import_recipe_from_url(url=url, include_tags=include_tags)
        except Exception as e:
            error_msg = f"Error importing recipe from '{url}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def import_recipes_from_urls(imports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Scrape multiple recipes from URLs (async bulk import).

        Args:
            imports: List of items, each with a ``url`` key and optional
                ``categories`` / ``tags`` arrays. Example:
                ``[{"url": "https://..."}, {"url": "https://...", "tags": [{"id": "..."}]}]``

        Returns:
            Acknowledgement from Mealie; processing happens asynchronously.
        """
        try:
            logger.info({"message": "Bulk-importing recipes", "count": len(imports)})
            return mealie.import_recipes_from_urls(imports)
        except Exception as e:
            error_msg = f"Error bulk-importing recipes: {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)

    @mcp.tool()
    def test_recipe_scrape(url: str, use_openai: bool = False) -> Dict[str, Any]:
        """Preview a recipe scrape without saving it.

        Args:
            url: The source URL to test-scrape.
            use_openai: If True, use Mealie's OpenAI-assisted scraper (requires server config).

        Returns:
            The scraped-but-not-saved recipe structure.
        """
        try:
            logger.info({"message": "Testing recipe scrape", "url": url, "use_openai": use_openai})
            return mealie.test_recipe_scrape(url=url, use_openai=use_openai)
        except Exception as e:
            error_msg = f"Error test-scraping '{url}': {str(e)}"
            logger.error({"message": error_msg})
            logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
            raise ToolError(error_msg)
