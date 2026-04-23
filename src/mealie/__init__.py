from .categories import CategoriesMixin
from .client import MealieClient
from .cookbooks import CookbooksMixin
from .foods import FoodsMixin
from .group import GroupMixin
from .labels import LabelsMixin
from .mealplan import MealplanMixin
from .recipe import RecipeMixin
from .shopping_list import ShoppingListMixin
from .tags import TagsMixin
from .tools_organizer import ToolsOrganizerMixin
from .units import UnitsMixin
from .user import UserMixin


class MealieFetcher(
    RecipeMixin,
    CategoriesMixin,
    TagsMixin,
    ToolsOrganizerMixin,
    FoodsMixin,
    UnitsMixin,
    LabelsMixin,
    ShoppingListMixin,
    MealplanMixin,
    CookbooksMixin,
    UserMixin,
    GroupMixin,
    MealieClient,
):
    pass
