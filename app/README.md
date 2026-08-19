# Minimal Genie-backed Databricks App (Path 3 starter)

A tiny Flask app: one chat box that asks a Genie space and shows the answer, running as the
signed-in user (OBO) so Unity Catalog applies that person's permissions.

## Files
- `app.py` — the app (chat box + `/ask` endpoint calling the Genie Conversation API).
- `app.yaml` — how Databricks runs it; set your `GENIE_SPACE_ID` here.
- `requirements.txt` — Python dependencies.

## Use
1. Put your Genie space id in `app.yaml` (`GENIE_SPACE_ID`).
2. Deploy as a Databricks App (`Compute > Apps`, or the CLI).
3. Enable **user authorization** with scopes `sql` and `genie` in the app settings
   (see `../docs/path3-databricks-app-teams-tab.md`, step 4).
4. Open the app URL and test, then pin it in Teams as a tab (step 6 of the guide).

This is a starting point, not production code. Add error handling, result formatting,
and any charts you want.
