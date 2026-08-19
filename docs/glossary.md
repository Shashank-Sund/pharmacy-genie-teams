# Glossary (one line each)

- **Unity Catalog (UC):** Databricks' permission system. Decides who can see which tables, rows, and columns.
- **Genie space:** A Databricks feature you point at a few tables; people ask questions in plain English and Genie writes and runs the SQL.
- **Genie Conversation API:** The way your own app asks a Genie space a question in code. Generally available.
- **Databricks App:** A small web app (Python, etc.) that Databricks hosts for you, right next to your data.
- **Service principal:** A robot/app identity. If an app uses one, everyone shares its access.
- **OBO (on-behalf-of) / user authorization:** The app runs each query as the *signed-in person*, so Unity Catalog applies *their* permissions.
- **SCIM:** The automatic sync that copies your Microsoft Entra ID users into Databricks so you don't create accounts by hand.
- **Entra ID:** Microsoft's identity system (formerly Azure AD), where your users and single sign-on live.
- **CSP (Compliance Security Profile):** A hardened Databricks setting required for handling PHI/HIPAA data.
- **BAA:** Business Associate Agreement, the contract that lets a vendor handle PHI.
- **Teams tab:** A pinned page inside a Teams channel that displays a website or app.
- **MCP:** A protocol an *outside* tool (like Copilot Studio) uses to reach Genie. Not needed when the app lives in Databricks.
- **SQL warehouse:** The Databricks compute that actually runs the SQL Genie generates.
