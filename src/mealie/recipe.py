"""Recipe API — split into focused mixins for maintainability.

Import the individual mixins directly, or use RecipeMixin as a combined
facade (preserves backwards compatibility with existing code that
references ``from mealie.recipe import RecipeMixin``).
"""

from .recipe_bulk import RecipeBulkMixin
from .recipe_crud import RecipeCrudMixin
from .recipe_image import RecipeImageMixin
from .recipe_import import RecipeImportMixin


class RecipeMixin(RecipeCrudMixin, RecipeImageMixin, RecipeImportMixin, RecipeBulkMixin):
    """Combined recipe mixin — aggregates all recipe sub-mixins."""

    pass
