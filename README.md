# Pharmacy Inventory Agent: Genie in Microsoft Teams

Plain-English walkthroughs for putting a Databricks **Genie** assistant for pharmacy inventory
in front of people **inside Microsoft Teams**, where each person only sees the data they're
allowed to.

This repo covers **two** ways to do it, both keeping the data and the "brain" in Databricks:

- **Path 3 (recommended, fully GA):** a small **Databricks App** backed by a **Genie space**,
  pinned inside Teams as a **tab**. Every component is generally available.
- **Path 4 (native chat, still Public Preview):** Databricks' **Genie app for Microsoft Teams**
  (users @-mention it), or a **bot** that connects a Databricks agent to Teams.

> Two other approaches exist (Microsoft Copilot Studio with the Databricks connector, or with
> Genie over MCP). They're valid but keep the "brain" in Microsoft and need cross-cloud
> networking, so they're out of scope for this repo.

**New to Databricks?** Read the [glossary](docs/glossary.md) first. Every term is explained in one line.

## Which path should I pick?

| | Path 3 (App + Teams tab) | Path 4 (native in Teams) |
|---|---|---|
| Experience | A web page pinned as a Teams tab | Chat: @-mention it in Teams |
| Maturity | **Fully GA** | **Public Preview** |
| Per-user data access | Yes (on behalf of the signed-in user) | Yes |
| Cross-cloud networking | Not needed | Not needed (Genie app); the bot needs Azure |
| Private Link (private networking) | Supported | Genie Teams app: not yet |
| Effort | Medium (build a small app) | Low (Genie app) / High (bot) |

Start with **Path 3** if you want something production-ready today. Choose **Path 4** if a native
chat experience matters more than GA status.

## Prerequisites (both paths)

- A Databricks workspace (this guide uses AWS) with Unity Catalog.
- For PHI: the Compliance Security Profile (HIPAA) enabled and a signed Databricks BAA.
- A Genie space over your inventory tables (each guide shows how).
- Microsoft 365 / Teams, and someone who can add or install a Teams app.

## Guides

- [Path 3: A Databricks App in a Teams tab (GA)](docs/path3-databricks-app-teams-tab.md)
- [Path 4: Native Databricks in Teams (Preview)](docs/path4-native-teams.md)
- [Glossary](docs/glossary.md)
- [`app/`](app/) — a minimal starter app for Path 3.
