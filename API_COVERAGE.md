# API Coverage Report

This document compares the MCP server implementation against the official Mealie API.

## Summary

| Category | Total Endpoints | Implemented | Coverage |
|----------|----------------|-------------|----------|
| Recipe Operations | 25 | 25 | 100% ✅ |
| Shopping Lists | 19 | 16 | 84% |
| Categories | 7 | 7 | 100% ✅ |
| Tags | 7 | 7 | 100% ✅ |
| Tools (organizer) | 6 | 6 | 100% ✅ |
| Labels | 5 | 5 | 100% ✅ |
| Foods | 6 | 6 | 100% ✅ |
| Units | 6 | 6 | 100% ✅ |
| Meal Plans | 8 | 8 | 100% ✅ |
| Meal Plan Rules | 5 | 5 | 100% ✅ |
| Cookbooks | 6 | 6 | 100% ✅ |
| User Self-Service | 7 | 7 | 100% ✅ |
| Account Management | 6 | 6 | 100% ✅ |
| Household Context | 7 | 7 | 100% ✅ |
| Household Invitations | 3 | 3 | 100% ✅ |
| Group Context | 10 | 10 | 100% ✅ |
| **Total Priority APIs** | **133** | **133** | **100% ✅** |

## Detailed Coverage

### ✅ Recipe Operations (25/25 implemented - 100%)

**CRUD:**
- ✅ `GET /api/recipes` - List/search recipes (with AND/OR tag/category filters)
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
- ✅ `GET /api/recipes/suggestions` - Get recipe suggestions (via search)

**Imports:**
- ✅ `POST /api/recipes/create/url` - Import recipe by URL
- ✅ `POST /api/recipes/create/url/bulk` - Bulk import from URLs
- ✅ `POST /api/recipes/test-scrape-url` - Preview scrape without saving
- ✅ `POST /api/recipes/create/html-or-json` - Parse HTML or schema.org/Recipe JSON
- ✅ `POST /api/recipes/create/zip` - Create from Mealie ZIP archive
- ✅ `POST /api/recipes/create/image` - OCR/vision import from image(s)

**Batch & bulk actions:**
- ✅ `PUT /api/recipes` - Batch replace many recipes
- ✅ `PATCH /api/recipes` - Batch patch many recipes
- ✅ `POST /api/recipes/bulk-actions/categorize` - Bulk assign categories
- ✅ `POST /api/recipes/bulk-actions/tag` - Bulk assign tags
- ✅ `POST /api/recipes/bulk-actions/settings` - Bulk update settings (public, locked, etc.)
- ✅ `POST /api/recipes/bulk-actions/delete` - Bulk delete

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
- ✅ `PUT /api/households/shopping/lists/{id}/label-settings` - Update label settings
- ✅ `POST /api/households/shopping/lists/{id}/recipe` - Add multiple recipes (array payload)

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

### ✅ Meal Plan Rules (5/5 implemented - 100%)

Rules constrain random-meal selection by day + entry_type + recipe filter.

- ✅ `GET /api/households/mealplans/rules` - List rules
- ✅ `POST /api/households/mealplans/rules` - Create rule
- ✅ `GET /api/households/mealplans/rules/{id}` - Get by ID
- ✅ `PUT /api/households/mealplans/rules/{id}` - Update rule
- ✅ `DELETE /api/households/mealplans/rules/{id}` - Delete rule

### ✅ User Self-Service (7/7 implemented - 100%)

- ✅ `GET /api/users/self` - Current user profile
- ✅ `GET /api/users/self/favorites` - List my favorites
- ✅ `POST /api/users/{id}/favorites/{slug}` - Add favorite
- ✅ `DELETE /api/users/{id}/favorites/{slug}` - Remove favorite
- ✅ `GET /api/users/self/ratings` - List my ratings
- ✅ `GET /api/users/self/ratings/{recipe_id}` - Get my rating for a recipe
- ✅ `POST /api/users/{id}/ratings/{slug}` - Rate a recipe

### ✅ Household Context (7/7 implemented - 100%)

- ✅ `GET /api/households/self` - Current household
- ✅ `GET /api/households/self/recipes/{slug}` - Household-scoped recipe
- ✅ `GET /api/households/members` - List members
- ✅ `GET /api/households/preferences` - Read preferences
- ✅ `PUT /api/households/preferences` - Update preferences
- ✅ `PUT /api/households/permissions` - Set member permissions
- ✅ `GET /api/households/statistics` - Household counts

### ✅ Household Invitations (3/3 implemented - 100%)

- ✅ `GET /api/households/invitations` - List outstanding invite tokens
- ✅ `POST /api/households/invitations` - Create invite token
- ✅ `POST /api/households/invitations/email` - Email an existing token

### ✅ Account Management (6/6 implemented - 100%)

- ✅ `PUT /api/users/password` - Change password
- ✅ `POST /api/users/forgot-password` - Trigger reset email
- ✅ `POST /api/users/reset-password` - Complete reset with token
- ✅ `POST /api/users/api-tokens` - Create API token
- ✅ `DELETE /api/users/api-tokens/{id}` - Revoke API token
- ✅ `POST /api/users/{id}/image` - Upload profile image

### ✅ Group Context (10/10 implemented - 100%)

- ✅ `GET /api/groups/self` - Current group
- ✅ `GET /api/groups/preferences` - Read group preferences
- ✅ `PUT /api/groups/preferences` - Update group preferences
- ✅ `GET /api/groups/members` - List members
- ✅ `GET /api/groups/members/{username_or_id}` - Get member
- ✅ `GET /api/groups/households` - List households
- ✅ `GET /api/groups/households/{slug}` - Get household by slug
- ✅ `GET /api/groups/storage` - Storage usage
- ✅ `GET /api/groups/reports` - List reports
- ✅ `GET /api/groups/reports/{id}` - Get report
- ✅ `DELETE /api/groups/reports/{id}` - Delete report

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

### Admin & User Management
- User administration (`/api/admin/users/*`)
- Authentication endpoints

### Other Features
- App settings and themes
- Backup/restore operations
- Parser settings
- Media management

## Implementation Priority

All user-facing priority APIs are now implemented. Remaining gaps are
intentional exclusions — either automation-config endpoints, admin/system
operations, or features that don't map naturally to an AI-chat interface.

- ✅ **Implemented**: Recipe CRUD + imports + bulk actions, shopping lists,
  categories, tags, tools, labels, foods, units, meal plans, meal plan rules,
  cookbooks, user favorites/ratings, account management (password reset,
  API tokens, profile image), household + group context, household invitations.
- ❌ **Out of scope**: Admin endpoints (`/api/admin/*`), auth
  (`/api/auth/*`), webhooks / event notifications / recipe actions,
  recipe comments / timeline / sharing / exports, `/api/explore/*`,
  backups, seeders, migrations, media serving.

## Mealie API Statistics

According to the OpenAPI specification (`openapi.json`):
- **Total Paths:** 169
- **Total Operations:** 254
- **Total Tags:** 55

**MCP Server Coverage:**
- **Tools Registered:** 134
- **Priority APIs Covered:** 133/133 (100%)
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

Tier 1 (45 tools): end-to-end tested against Claude Desktop with a live
Mealie instance — CRUD, bulk ops, empty/null handling, error paths, and
cross-feature integration (e.g., adding recipes to shopping lists).

Tiers 1–3 additions (80 more tools): verified via FastMCP registration
smoke tests; manual end-to-end validation is per-deploy.
