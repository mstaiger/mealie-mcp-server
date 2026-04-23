# API Coverage Report

This document compares the MCP server implementation against the official Mealie API.

## Summary

| Category | Total Endpoints | Implemented | Coverage |
|----------|----------------|-------------|----------|
| Recipe Operations | 20 | 16 | 80% |
| Shopping Lists | 17 | 14 | 82% |
| Categories | 7 | 7 | 100% ✅ |
| Tags | 7 | 7 | 100% ✅ |
| Tools (organizer) | 6 | 6 | 100% ✅ |
| Labels | 5 | 5 | 100% ✅ |
| Foods | 6 | 6 | 100% ✅ |
| Units | 6 | 6 | 100% ✅ |
| Meal Plans | 8 | 8 | 100% ✅ |
| Cookbooks | 6 | 6 | 100% ✅ |
| **Total Priority APIs** | **88** | **81** | **92%** |

## Detailed Coverage

### ✅ Recipe Operations (16/20 implemented)

**Implemented:**
- ✅ `GET /api/recipes` - List/search recipes
- ✅ `POST /api/recipes` - Create recipe
- ✅ `GET /api/recipes/{slug}` - Get recipe details
- ✅ `PUT /api/recipes/{slug}` - Update recipe (full)
- ✅ `PATCH /api/recipes/{slug}` - Partial update
- ✅ `DELETE /api/recipes/{slug}` - Delete recipe
- ✅ `POST /api/recipes/{slug}/duplicate` - Duplicate recipe
- ✅ `PATCH /api/recipes/{slug}/last-made` - Update last made
- ✅ `POST /api/recipes/{slug}/image` - Scrape image from URL
- ✅ `PUT /api/recipes/{slug}/image` - Upload image file
- ✅ `POST /api/recipes/{slug}/assets` - Upload asset file
- ✅ `POST /api/recipes/create/url` - Import recipe by URL
- ✅ `POST /api/recipes/create/url/bulk` - Bulk import from URLs
- ✅ `POST /api/recipes/test-scrape-url` - Preview scrape without saving
- ✅ `GET /api/recipes/suggestions` - Get recipe suggestions (via search)
- ✅ Advanced filtering with AND/OR logic for tags/categories

**Not Yet Implemented:**
- ⏳ `POST /api/recipes/create/zip` - Create from ZIP
- ⏳ `POST /api/recipes/create/html-or-json` - Create from HTML/JSON
- ⏳ `PUT /api/recipes` - Bulk update
- ⏳ `PATCH /api/recipes` - Bulk patch
- ⏳ Recipe comments, timeline, and sharing features

### ✅ Shopping Lists (14/17 implemented)

**Shopping List Management:**
- ✅ `GET /api/households/shopping/lists` - List all
- ✅ `POST /api/households/shopping/lists` - Create
- ✅ `GET /api/households/shopping/lists/{id}` - Get by ID
- ✅ `PUT /api/households/shopping/lists/{id}` - Update
- ✅ `DELETE /api/households/shopping/lists/{id}` - Delete

**Recipe Integration:**
- ✅ `POST /api/households/shopping/lists/{id}/recipe/{recipe_id}` - Add recipe
- ✅ `POST /api/households/shopping/lists/{id}/recipe/{recipe_id}/delete` - Remove recipe

**Shopping List Items:**
- ✅ `GET /api/households/shopping/items` - List all items
- ✅ `GET /api/households/shopping/items/{id}` - Get item
- ✅ `POST /api/households/shopping/items` - Create item
- ✅ `POST /api/households/shopping/items/create-bulk` - Bulk create
- ✅ `PUT /api/households/shopping/items/{id}` - Update item
- ✅ `PUT /api/households/shopping/items` - Bulk update
- ✅ `DELETE /api/households/shopping/items/{id}` - Delete item
- ✅ `DELETE /api/households/shopping/items` - Bulk delete (query params)

**Not Yet Implemented:**
- ⏳ `PUT /api/households/shopping/lists/{id}/label-settings` - Update label settings
- ⏳ `POST /api/households/shopping/lists/{id}/recipe` - Add multiple recipes (array payload)

### ✅ Categories (7/7 implemented - 100%)

- ✅ `GET /api/organizers/categories` - List all
- ✅ `GET /api/organizers/categories/empty` - Get empty
- ✅ `POST /api/organizers/categories` - Create
- ✅ `GET /api/organizers/categories/{id}` - Get by ID
- ✅ `GET /api/organizers/categories/slug/{slug}` - Get by slug
- ✅ `PUT /api/organizers/categories/{id}` - Update
- ✅ `DELETE /api/organizers/categories/{id}` - Delete

### ✅ Tags (7/7 implemented - 100%)

- ✅ `GET /api/organizers/tags` - List all
- ✅ `GET /api/organizers/tags/empty` - Get empty
- ✅ `POST /api/organizers/tags` - Create
- ✅ `GET /api/organizers/tags/{id}` - Get by ID
- ✅ `GET /api/organizers/tags/slug/{slug}` - Get by slug
- ✅ `PUT /api/organizers/tags/{id}` - Update
- ✅ `DELETE /api/organizers/tags/{id}` - Delete

### ✅ Foods (6/6 implemented - 100%)

- ✅ `GET /api/foods` - List all
- ✅ `POST /api/foods` - Create
- ✅ `GET /api/foods/{id}` - Get by ID
- ✅ `PUT /api/foods/{id}` - Update
- ✅ `DELETE /api/foods/{id}` - Delete
- ✅ `PUT /api/foods/merge` - Merge two foods

### ✅ Units (6/6 implemented - 100%)

- ✅ `GET /api/units` - List all
- ✅ `POST /api/units` - Create
- ✅ `GET /api/units/{id}` - Get by ID
- ✅ `PUT /api/units/{id}` - Update
- ✅ `DELETE /api/units/{id}` - Delete
- ✅ `PUT /api/units/merge` - Merge two units

### ✅ Meal Plans (8/8 implemented - 100%)

- ✅ `GET /api/households/mealplans` - List meal plans
- ✅ `GET /api/households/mealplans/today` - Get today's plan
- ✅ `POST /api/households/mealplans` - Create entry
- ✅ `GET /api/households/mealplans/{id}` - Get by ID
- ✅ `PUT /api/households/mealplans/{id}` - Update entry
- ✅ `DELETE /api/households/mealplans/{id}` - Delete entry
- ✅ `POST /api/households/mealplans/random` - Create random entry (respects household rules)
- ✅ Bulk creation via loop (not a native bulk endpoint)

### ✅ Cookbooks (6/6 implemented - 100%)

- ✅ `GET /api/households/cookbooks` - List cookbooks
- ✅ `POST /api/households/cookbooks` - Create cookbook
- ✅ `GET /api/households/cookbooks/{id}` - Get by id or slug
- ✅ `PUT /api/households/cookbooks/{id}` - Update cookbook
- ✅ `DELETE /api/households/cookbooks/{id}` - Delete cookbook
- ✅ `PUT /api/households/cookbooks` - Bulk update (primarily for reordering)

### ✅ Tools / Kitchen Equipment (6/6 implemented - 100%)

- ✅ `GET /api/organizers/tools` - List all
- ✅ `POST /api/organizers/tools` - Create
- ✅ `GET /api/organizers/tools/{id}` - Get by ID
- ✅ `GET /api/organizers/tools/slug/{slug}` - Get by slug
- ✅ `PUT /api/organizers/tools/{id}` - Update
- ✅ `DELETE /api/organizers/tools/{id}` - Delete

### ✅ Labels (5/5 implemented - 100%)

- ✅ `GET /api/groups/labels` - List labels
- ✅ `POST /api/groups/labels` - Create label
- ✅ `GET /api/groups/labels/{id}` - Get by ID
- ✅ `PUT /api/groups/labels/{id}` - Update label
- ✅ `DELETE /api/groups/labels/{id}` - Delete label

## Not Yet Covered (Lower Priority)

The following API areas are available but not yet implemented:

### Recipe Advanced Features
- Recipe comments (`/api/recipes/{slug}/comments/*`)
- Recipe timeline (`/api/recipes/timeline/*`)
- Recipe sharing (`/api/recipes/{slug}/share`)
- Recipe exports (`/api/recipes/{slug}/exports`)
- Recipe scraper settings

### Household Management
- Webhooks (`/api/households/webhooks/*`)
- Event notifications (`/api/households/event-notifications/*`)
- Recipe actions (`/api/households/recipe-actions/*`)
- Meal plan rules (`/api/households/mealplans/rules/*`)

### Admin & User Management
- User administration (`/api/admin/users/*`)
- Group management (`/api/groups/*`)
- User profiles (`/api/users/self/*`)
- Authentication endpoints

### Other Features
- App settings and themes
- Backup/restore operations
- Parser settings
- Media management

## Implementation Priority

Based on user value and API usage, the implementation priorities were:

1. **High Priority (Implemented)**
   - ✅ Recipe CRUD and search
   - ✅ Shopping list management
   - ✅ Categories and tags
   - ✅ Basic meal planning

2. **Medium Priority (Partially Implemented)**
   - 🔶 Advanced recipe features (URL import, bulk operations)
   - 🔶 Complete meal plan management
   - 🔶 Recipe sharing and exports

3. **Lower Priority (Not Yet Implemented)**
   - ⏳ Admin and user management
   - ⏳ Cookbooks and webhooks
   - ⏳ System settings and backups

## Coverage Goals

**Current: 78% of priority APIs**

Target for future releases:
- v1.1: 85% (add recipe URL import, complete meal plan CRUD)
- v1.2: 90% (add cookbooks, recipe sharing)
- v2.0: 95%+ (comprehensive coverage including admin features)

## Mealie API Statistics

According to the OpenAPI specification (`openapi.json`):
- **Total Paths:** 169
- **Total Operations:** 254
- **Total Tags:** 55

**MCP Server Coverage:**
- **Paths Covered:** ~50
- **Operations Implemented:** 45 tools
- **Tags Covered:** 8 major categories

## Notes

1. **100% Coverage Not Required**: Many API endpoints are for admin/system operations that don't make sense in an MCP context (e.g., server backups, user administration).

2. **Practical Coverage**: The 78% coverage focuses on user-facing features that are actually useful through an AI assistant interface.

3. **Extensible Design**: The mixin architecture makes it easy to add new endpoints as needed.

4. **Quality Over Quantity**: Each implemented endpoint includes:
   - Comprehensive error handling
   - Field preservation where needed
   - Proper request/response validation
   - Clear documentation

## Testing Coverage

All 45 implemented tools have been tested end-to-end with Claude Desktop:
- ✅ CRUD operations verified
- ✅ Bulk operations tested
- ✅ Edge cases handled (empty responses, null values, field preservation)
- ✅ Error scenarios validated
- ✅ Integration between features (e.g., adding recipes to shopping lists)
