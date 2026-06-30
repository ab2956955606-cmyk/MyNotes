# Legacy MyNotes

This folder records the previous product stage before the desktop migration.

The original MyNotes was a pure frontend daily planner based on HTML, CSS and JavaScript. It stored user data in browser `localStorage` and could be opened directly from an HTML file.

Legacy storage keys observed during migration:

- `my_notes_data`: dated plan data
- `my_notes_data_v2`: React migration plan data
- `my_notes_lang`: language preference
- `my_notes_preferences`: AI preference text
- `note_{year}_{month}`: monthly notes

The old implementation files were already removed before Phase 1 started. Future migration work should preserve compatibility by importing these localStorage keys into the new SQLite data model rather than silently dropping user data.
