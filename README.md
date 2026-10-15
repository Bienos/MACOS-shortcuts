# Command Club

Polish-language, static web app for learning Mac keyboard shortcuts. It uses the existing HTML/CSS/JavaScript stack and needs no build step.

## Run locally

From this `Command_Club_Web_App` directory:

```sh
python3 -m http.server 4173
```

Open [http://localhost:4173](http://localhost:4173).

## Refresh shortcut data and mappings

The importer reads the repository's `Mac_Keyboard_Shortcuts_Master.xlsx` workbook's canonical `01_WSZYSTKIE` sheet, the curated path in `22_UCZ_SIE_30`, and the key legend in `17_KLAWIATURA`. It preserves each workbook row and adds a `playgroundType` and `playgroundReason` mapping without merging duplicate shortcuts.

```sh
python3 scripts/import_workbook.py
python3 scripts/check_playground_coverage.py
```

The coverage check writes `data/playground-coverage.json`, including every source record assigned to the explicitly safe `guided` visualization type, with its reason. The current mapping covers all 879 imported records. It flags any missing or unknown mapping and exits with an error.

## Learning experience

- The 30-item workbook path remains available. “Znam już podstawy” resumes from stage 2.
- Every catalogue detail panel can launch its record's mapped scene: editable text with selection/clipboard/undo state, Finder files, browser, windows, screen capture, isolated code/terminal, app-specific mockups (Calendar, Mail, spreadsheets, chat), or safe guided visualization.
- Each playground opens with a three-step coach: prepare the scene, use the shortcut, then inspect the result. The instruction names the exact item to select; text scenes also accept a real cursor or text selection.
- Every record displays a miniature keyboard and highlights the record’s key combination when it is time to use it. The keyboard is illustrative; Polish keyboard layouts can place printed symbols differently.
- The scene changes only inside the page and has a simulated-action button, hint, reset, and review-queue action. Matching combinations are handled only while the playground has focus; browser or macOS interception is explained, and the on-screen simulation remains available.
- “Spróbuj na Macu” remains a separate guided step. The site does not execute commands on the learner's Mac or claim that the real shortcut worked.
- Learning status and review items are stored in browser local storage.
- The supplied Plan, Lesson, Practice, and Catalogue PNG artwork is copied into `assets/` for the screen treatments. The original reference files and source workbook are unchanged.

The imported workbook metadata remains authoritative for shortcut, context, configuration, version, layout note, and source. The 68 rows assigned to a guided visualization do not have a behaviorally detailed scene: the page explains that limitation rather than simulating a guessed system action. Their IDs and reasons are listed in `data/playground-coverage.json`.
