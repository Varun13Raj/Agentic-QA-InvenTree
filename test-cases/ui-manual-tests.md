# InvenTree Parts Module - Manual UI Test Cases

## Test Suite Overview
Comprehensive manual test cases for InvenTree Parts module covering part creation, detail views, categories, parameters, templates, and revisions.

---

| Test ID | Module | Scenario Description | Steps to Reproduce | Expected Result | Test Type |
|---------|--------|---------------------|-------------------|-----------------|-----------|
| TC-PART-001 | Part Creation | Create a new part with all mandatory fields | 1. Navigate to Parts menu<br>2. Click "New Part" button<br>3. Enter Part Name (e.g., "Resistor 10K")<br>4. Enter Description<br>5. Select Category<br>6. Click "Submit" | Part is created successfully and appears in parts list with correct details | Positive |
| TC-PART-002 | Part Creation | Create part without mandatory Part Name | 1. Navigate to Parts menu<br>2. Click "New Part" button<br>3. Leave Part Name field empty<br>4. Fill other fields<br>5. Click "Submit" | Validation error displayed: "Part Name is required"<br>Form is not submitted | Negative |
| TC-PART-003 | Part Creation | Create part with maximum character limit in name field | 1. Navigate to Parts menu<br>2. Click "New Part" button<br>3. Enter 255 characters in Part Name field<br>4. Fill other required fields<br>5. Click "Submit" | Part is created successfully with full name displayed | Boundary |
| TC-PART-004 | Part Creation | Create part exceeding maximum character limit in name field | 1. Navigate to Parts menu<br>2. Click "New Part" button<br>3. Enter 256 characters in Part Name field<br>4. Fill other required fields<br>5. Click "Submit" | Validation error: "Part Name exceeds maximum length"<br>Form is not submitted | Boundary |
| TC-PART-005 | Part Creation | Create part with duplicate name | 1. Create a part with name "Test Part"<br>2. Navigate to create new part<br>3. Enter same name "Test Part"<br>4. Fill other fields<br>5. Click "Submit" | System allows creation (parts can have duplicate names) OR shows warning if duplicates not allowed | Negative |
| TC-PART-006 | Part Creation | Create part with special characters in name | 1. Navigate to Parts menu<br>2. Click "New Part" button<br>3. Enter name with special chars: "Part@#$%&*"<br>4. Fill other required fields<br>5. Click "Submit" | Part is created successfully with special characters in name | Boundary |
| TC-PART-007 | Part Creation | Create part with IPN (Internal Part Number) | 1. Navigate to Parts menu<br>2. Click "New Part" button<br>3. Fill required fields<br>4. Enter unique IPN (e.g., "IPN-2024-001")<br>5. Click "Submit" | Part created with IPN assigned and visible in part details | Positive |
| TC-PART-008 | Part Creation | Create part with duplicate IPN | 1. Create part with IPN "IPN-001"<br>2. Create another part<br>3. Enter same IPN "IPN-001"<br>4. Click "Submit" | Validation error: "IPN must be unique"<br>Part is not created | Negative |
| TC-PART-009 | Part Creation | Create assembly part with BOM | 1. Navigate to Parts menu<br>2. Click "New Part"<br>3. Fill required fields<br>4. Check "Assembly" checkbox<br>5. Click "Submit" | Part created as assembly type with BOM tab available | Positive |
| TC-PART-010 | Part Creation | Create component part (non-assembly) | 1. Navigate to Parts menu<br>2. Click "New Part"<br>3. Fill required fields<br>4. Leave "Assembly" unchecked<br>5. Click "Submit" | Part created as component without BOM tab | Positive |
| TC-PART-011 | Part Creation | Create template part | 1. Navigate to Parts menu<br>2. Click "New Part"<br>3. Fill required fields<br>4. Check "Template" checkbox<br>5. Click "Submit" | Part created as template with variants capability enabled | Positive |
| TC-PART-012 | Part Creation | Cancel part creation mid-process | 1. Navigate to Parts menu<br>2. Click "New Part"<br>3. Fill some fields<br>4. Click "Cancel" button | Part creation cancelled, no new part added, returned to parts list | Positive |
| TC-PART-013 | Part Detail View | View part overview tab | 1. Navigate to existing part<br>2. Click on part name to open details<br>3. Verify Overview tab is displayed | Overview tab shows: part name, description, IPN, category, keywords, units, stock information | Positive |
| TC-PART-014 | Part Detail View | View part parameters tab | 1. Open part details<br>2. Click "Parameters" tab | Parameters tab displays all assigned parameters with names, values, and units | Positive |
| TC-PART-015 | Part Detail View | View part stock tab | 1. Open part details<br>2. Click "Stock" tab | Stock tab shows: stock locations, quantities, status, batch codes | Positive |
| TC-PART-016 | Part Detail View | View part BOM tab for assembly | 1. Open assembly part details<br>2. Click "BOM" tab | BOM tab displays list of sub-components with quantities and references | Positive |
| TC-PART-017 | Part Detail View | View part BOM tab for non-assembly | 1. Open non-assembly part details<br>2. Check for BOM tab | BOM tab is not available/hidden for non-assembly parts | Negative |
| TC-PART-018 | Part Detail View | View part variants tab for template | 1. Open template part details<br>2. Click "Variants" tab | Variants tab shows all part variants derived from this template | Positive |
| TC-PART-019 | Part Detail View | View part suppliers tab | 1. Open part details<br>2. Click "Suppliers" tab | Suppliers tab shows: supplier names, SKUs, pricing, lead times | Positive |
| TC-PART-020 | Part Detail View | View part manufacturers tab | 1. Open part details<br>2. Click "Manufacturers" tab | Manufacturers tab displays manufacturer names and MPN (Manufacturer Part Numbers) | Positive |
| TC-PART-021 | Part Detail View | View part attachments tab | 1. Open part details<br>2. Click "Attachments" tab | Attachments tab shows uploaded files with names, types, and download options | Positive |
| TC-PART-022 | Part Detail View | View part notes tab | 1. Open part details<br>2. Click "Notes" tab | Notes tab displays markdown-formatted notes and allows editing | Positive |
| TC-PART-023 | Part Edit | Edit part name | 1. Open part details<br>2. Click "Edit" button<br>3. Modify part name<br>4. Click "Save" | Part name updated successfully, new name displayed in all views | Positive |
| TC-PART-024 | Part Edit | Edit part description | 1. Open part details<br>2. Click "Edit"<br>3. Modify description<br>4. Click "Save" | Description updated successfully | Positive |
| TC-PART-025 | Part Edit | Clear mandatory field during edit | 1. Open part details<br>2. Click "Edit"<br>3. Clear Part Name field<br>4. Click "Save" | Validation error: "Part Name is required"<br>Changes not saved | Negative |
| TC-PART-026 | Part Edit | Change part category | 1. Open part details<br>2. Click "Edit"<br>3. Select different category<br>4. Click "Save" | Part moved to new category, visible in new category list | Positive |
| TC-PART-027 | Part Edit | Convert component to assembly | 1. Open non-assembly part<br>2. Click "Edit"<br>3. Check "Assembly" checkbox<br>4. Click "Save" | Part converted to assembly, BOM tab now available | Positive |
| TC-PART-028 | Part Delete | Delete part with no dependencies | 1. Open part with no stock/BOM references<br>2. Click "Delete" button<br>3. Confirm deletion | Part deleted successfully, removed from parts list | Positive |
| TC-PART-029 | Part Delete | Attempt to delete part with stock | 1. Open part that has stock items<br>2. Click "Delete" button<br>3. Attempt to confirm | Warning message: "Cannot delete part with existing stock"<br>Deletion prevented | Negative |
| TC-PART-030 | Part Delete | Attempt to delete part used in BOM | 1. Open part used in another part's BOM<br>2. Click "Delete" button<br>3. Attempt to confirm | Warning message: "Cannot delete part used in assemblies"<br>Deletion prevented | Negative |
| TC-PART-031 | Part Delete | Cancel part deletion | 1. Open part details<br>2. Click "Delete"<br>3. Click "Cancel" on confirmation | Deletion cancelled, part remains in system | Positive |
| TC-PART-032 | Part Category | Create new part category | 1. Navigate to Categories<br>2. Click "New Category"<br>3. Enter category name (e.g., "Electronics")<br>4. Enter description<br>5. Click "Submit" | New category created and appears in category tree | Positive |
| TC-PART-033 | Part Category | Create subcategory | 1. Select parent category<br>2. Click "New Subcategory"<br>3. Enter subcategory name<br>4. Click "Submit" | Subcategory created under parent, visible in hierarchy | Positive |
| TC-PART-034 | Part Category | Create category with duplicate name | 1. Create category "Capacitors"<br>2. Create another category<br>3. Enter same name "Capacitors"<br>4. Click "Submit" | System allows duplicate OR shows error if duplicates not allowed | Negative |
| TC-PART-035 | Part Category | Delete empty category | 1. Navigate to category with no parts<br>2. Click "Delete"<br>3. Confirm deletion | Category deleted successfully | Positive |
| TC-PART-036 | Part Category | Attempt to delete category with parts | 1. Navigate to category containing parts<br>2. Click "Delete"<br>3. Attempt to confirm | Warning: "Cannot delete category with parts"<br>Deletion prevented | Negative |
| TC-PART-037 | Part Category | Move part between categories | 1. Open part details<br>2. Edit part<br>3. Change category selection<br>4. Save | Part moved to new category, visible in new category only | Positive |
| TC-PART-038 | Part Parameters | Add parameter to part | 1. Open part details<br>2. Go to Parameters tab<br>3. Click "Add Parameter"<br>4. Select parameter template (e.g., "Resistance")<br>5. Enter value (e.g., "10K")<br>6. Click "Save" | Parameter added and displayed in Parameters tab | Positive |
| TC-PART-039 | Part Parameters | Add parameter with units | 1. Open part details<br>2. Go to Parameters tab<br>3. Add parameter<br>4. Enter value with unit (e.g., "100 Ohm")<br>5. Save | Parameter saved with value and unit displayed | Positive |
| TC-PART-040 | Part Parameters | Add duplicate parameter | 1. Open part with existing parameter<br>2. Try to add same parameter type again<br>3. Attempt to save | Validation error: "Parameter already exists" OR system allows multiple instances | Negative |
| TC-PART-041 | Part Parameters | Edit parameter value | 1. Open part with parameters<br>2. Go to Parameters tab<br>3. Click edit on parameter<br>4. Modify value<br>5. Save | Parameter value updated successfully | Positive |
| TC-PART-042 | Part Parameters | Delete parameter from part | 1. Open part with parameters<br>2. Go to Parameters tab<br>3. Select parameter<br>4. Click "Delete"<br>5. Confirm | Parameter removed from part | Positive |
| TC-PART-043 | Part Parameters | Add parameter with invalid data type | 1. Open part details<br>2. Add numeric parameter template<br>3. Enter text value instead of number<br>4. Try to save | Validation error: "Invalid data type"<br>Parameter not saved | Negative |
| TC-PART-044 | Part Template | Create template part | 1. Create new part<br>2. Check "Template" option<br>3. Fill required fields<br>4. Submit | Template part created with Variants tab available | Positive |
| TC-PART-045 | Part Template | Create variant from template | 1. Open template part<br>2. Go to Variants tab<br>3. Click "Create Variant"<br>4. Enter variant-specific details<br>5. Submit | New variant created, linked to template, appears in Variants tab | Positive |
| TC-PART-046 | Part Template | Convert regular part to template | 1. Open non-template part<br>2. Edit part<br>3. Check "Template" option<br>4. Save | Part converted to template, Variants tab now available | Positive |
| TC-PART-047 | Part Template | View all variants of template | 1. Open template part<br>2. Navigate to Variants tab | All variants displayed with names and key differentiating parameters | Positive |
| TC-PART-048 | Part Revision | Create part with initial revision | 1. Create new part<br>2. Enter revision code (e.g., "A")<br>3. Submit | Part created with revision "A" displayed | Positive |
| TC-PART-049 | Part Revision | Create new revision of existing part | 1. Open part details<br>2. Click "New Revision"<br>3. Enter new revision code (e.g., "B")<br>4. Enter revision notes<br>5. Submit | New revision created, part displays latest revision | Positive |
| TC-PART-050 | Part Revision | View revision history | 1. Open part with multiple revisions<br>2. Navigate to Revisions tab | All revisions displayed chronologically with revision codes, dates, and notes | Positive |
| TC-PART-051 | Part Revision | Create revision with duplicate code | 1. Open part with revision "A"<br>2. Create new revision<br>3. Enter same code "A"<br>4. Submit | Validation error: "Revision code must be unique"<br>Revision not created | Negative |
| TC-PART-052 | Part Revision | Create revision without code | 1. Open part details<br>2. Click "New Revision"<br>3. Leave revision code empty<br>4. Submit | Validation error: "Revision code required" OR system auto-generates code | Negative |
| TC-PART-053 | Part Revision | Switch active revision | 1. Open part with multiple revisions<br>2. Go to Revisions tab<br>3. Select older revision<br>4. Set as active | Selected revision becomes active, displayed as current revision | Positive |
| TC-PART-054 | Part Search | Search part by name | 1. Go to Parts page<br>2. Enter part name in search box<br>3. Press Enter | Matching parts displayed in results list | Positive |
| TC-PART-055 | Part Search | Search part by IPN | 1. Go to Parts page<br>2. Enter IPN in search box<br>3. Press Enter | Part with matching IPN displayed | Positive |
| TC-PART-056 | Part Search | Search with partial name match | 1. Go to Parts page<br>2. Enter partial part name (e.g., "Res" for "Resistor")<br>3. Press Enter | All parts containing the search term displayed | Positive |
| TC-PART-057 | Part Search | Search with no results | 1. Go to Parts page<br>2. Enter non-existent part name<br>3. Press Enter | "No results found" message displayed | Negative |
| TC-PART-058 | Part Search | Search with special characters | 1. Go to Parts page<br>2. Enter search with special chars: "@#$%"<br>3. Press Enter | System handles gracefully, shows no results or matching parts | Boundary |
| TC-PART-059 | Part Filter | Filter parts by category | 1. Go to Parts page<br>2. Select category from filter dropdown<br>3. Apply filter | Only parts in selected category displayed | Positive |
| TC-PART-060 | Part Filter | Filter active/inactive parts | 1. Go to Parts page<br>2. Select "Active" or "Inactive" filter<br>3. Apply | Parts filtered by active status correctly | Positive |
| TC-PART-061 | Part Filter | Filter assembly parts only | 1. Go to Parts page<br>2. Apply "Assembly" filter<br>3. View results | Only assembly parts displayed | Positive |
| TC-PART-062 | Part Filter | Filter template parts only | 1. Go to Parts page<br>2. Apply "Template" filter<br>3. View results | Only template parts displayed | Positive |
| TC-PART-063 | Part Filter | Combine multiple filters | 1. Go to Parts page<br>2. Select category filter<br>3. Add active status filter<br>4. Apply | Parts matching all filter criteria displayed | Positive |
| TC-PART-064 | Part Filter | Clear all filters | 1. Apply multiple filters<br>2. Click "Clear Filters" button | All filters removed, full parts list displayed | Positive |
| TC-PART-065 | Part Stock | View stock levels for part | 1. Open part details<br>2. Navigate to Stock tab | All stock items displayed with quantities and locations | Positive |
| TC-PART-066 | Part Stock | View part with zero stock | 1. Open part with no stock<br>2. Navigate to Stock tab | "No stock items" message displayed, total stock shows 0 | Positive |
| TC-PART-067 | Part Image | Upload part image | 1. Open part details<br>2. Click on image placeholder<br>3. Select image file (JPG/PNG)<br>4. Upload | Image uploaded and displayed as part thumbnail | Positive |
| TC-PART-068 | Part Image | Upload invalid image format | 1. Open part details<br>2. Try to upload .txt or .exe file as image<br>3. Attempt upload | Validation error: "Invalid file format"<br>Upload rejected | Negative |
| TC-PART-069 | Part Image | Upload oversized image | 1. Open part details<br>2. Try to upload image > 10MB<br>3. Attempt upload | Validation error: "File size exceeds limit"<br>Upload rejected | Boundary |
| TC-PART-070 | Part Image | Delete part image | 1. Open part with image<br>2. Click delete image button<br>3. Confirm | Image removed, placeholder displayed | Positive |
| TC-PART-071 | Part Units | Set custom units for part | 1. Create/edit part<br>2. Enter custom units (e.g., "pieces", "meters")<br>3. Save | Part saved with custom units displayed | Positive |
| TC-PART-072 | Part Keywords | Add keywords to part | 1. Edit part<br>2. Add keywords in keywords field (e.g., "resistor, 10K, through-hole")<br>3. Save | Keywords saved and used for search/filtering | Positive |
| TC-PART-073 | Part Pricing | View part pricing | 1. Open part details<br>2. Navigate to Pricing section | Purchase and internal pricing displayed if available | Positive |
| TC-PART-074 | Part Notes | Add notes to part | 1. Open part details<br>2. Go to Notes tab<br>3. Enter notes in markdown editor<br>4. Save | Notes saved and displayed with markdown formatting | Positive |
| TC-PART-075 | Part Notes | Edit existing notes | 1. Open part with notes<br>2. Modify notes content<br>3. Save | Notes updated successfully | Positive |

---

## Test Execution Notes

- Execute tests in a clean InvenTree test environment
- Create test data as needed for dependencies (categories, parameters, etc.)
- Document any deviations from expected results
- Capture screenshots for failed test cases
- Test on supported browsers: Chrome, Firefox, Edge
- Verify responsive behavior on different screen sizes

## Test Data Requirements

- Valid part categories hierarchy
- Parameter templates for various types (numeric, text, boolean)
- Sample supplier and manufacturer data
- Test users with appropriate permissions

## Coverage Summary

- **Part Creation**: 12 test cases
- **Part Detail Views**: 11 test cases
- **Part Edit/Delete**: 8 test cases
- **Categories**: 6 test cases
- **Parameters**: 6 test cases
- **Templates**: 4 test cases
- **Revisions**: 6 test cases
- **Search/Filter**: 11 test cases
- **Stock View**: 2 test cases
- **Images**: 4 test cases
- **Miscellaneous**: 5 test cases

**Total**: 75 comprehensive test cases covering positive, negative, and boundary scenarios.
