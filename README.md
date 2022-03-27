# bpsync

Roadmap:
- Correct threading for SongWorker and integration with progress bar dialog
  - Fix worker thread not stopping on exit (possible option is another signal/slot); better user flow on progress window (block exiting, cancel button, etc?)
- Fix database calls (global engine + entry appending instead of overwriting, etc)
- Main menu
- Set up standard sync

Extras:
- Context menu displaying all available libpytunes fields
- Arbitrary volume adjustment context menu directly editing underlying `Song` object
- Statistics calculations for checked items in table
- Clean up imports