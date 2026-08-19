# Path 3: A Databricks App in a Teams tab (fully GA)

**Goal:** a pharmacist opens a tab in Teams, types "how many naloxone sprays are on hand in the
Pavilion today?", and gets an exact answer. Each person only sees data they're allowed to.
Everything runs in Databricks.

## The big picture (in plain words)

Three simple pieces:

1. **Genie** is like a data analyst that turns plain-English questions into SQL and runs them on your inventory tables.
2. A **Databricks App** is a small web page with a chat box. When someone asks a question, the app hands it to Genie and shows the answer.
3. A **Teams tab** is just that web page pinned inside a Teams channel.

Because the app and the data both live in Databricks, there's no cross-cloud plumbing to build.

## What makes it per-user

The app is set to run **on behalf of the signed-in user** (called OBO). So when a pharmacist asks
a question, Genie queries as *that pharmacist*, and Unity Catalog only returns what they're allowed
to see. No shared robot account, and the audit log shows the real person.

## Prerequisites

- A Databricks workspace with Unity Catalog (and, for PHI, CSP/HIPAA + a signed BAA).
- Your inventory tables in Unity Catalog.
- Permission to create a Databricks App.
- The ability to add a custom tab/app in Teams (you or a Teams admin).

## Steps

### 1. Make a Genie space
- In Databricks, open **Genie** and create a space.
- Add your inventory tables.
- Add a few sample questions and short instructions (for example: "'usage' means the Pyxis table
  plus logistics transactions"). Good instructions produce better answers.
- Copy the **space ID** from the URL (the long id after `/genie/`).

### 2. Grant access to the pharmacist group (once)
Give the pharmacy group:
- **CAN VIEW** on the Genie space
- **SELECT** on the inventory tables
- **CAN USE** on the SQL warehouse the space uses

New pharmacists inherit this automatically once they're in the group (see **SCIM** below).

### 3. Create the Databricks App
- In Databricks, go to **Compute > Apps > Create app** (or use the CLI).
- Start from a template (Python/Flask or Streamlit). The [`app/`](../app) folder here is a minimal starting point.
- Set an environment variable `GENIE_SPACE_ID` to the id from step 1.

### 4. Turn on per-user (OBO)
- In the app's settings, enable **user authorization** and add the scopes `sql` and `genie`.
- Databricks then passes the signed-in user's token to your app (in the `X-Forwarded-Access-Token`
  header), and the app uses it to call Genie as that user.
- Docs: https://docs.databricks.com/aws/en/dev-tools/databricks-apps/auth

### 5. Deploy the app
- Deploy it. Databricks gives you a URL (a `databricksapps.com` address). Open it and test a question.

### 6. Put it in Teams as a tab
- In Teams, add a custom app / website tab pointing to your app URL.
- Add the app's domain to the Teams app manifest's `validDomains`.
- Set up single sign-on so the Teams user signs in as their Databricks identity (same Entra tenant makes this clean).
- Pin the tab in the pharmacy channel.

### 7. Done
Pharmacists open the tab and ask questions. Each sees only their permitted data.

## SCIM: how people become Databricks users automatically

Per-user access needs each pharmacist to exist as a Databricks user. **SCIM** does this for you:
your admin sets up the Entra provisioning connector once and assigns the pharmacist group; Entra then
syncs those users into Databricks (right away, then every 20 to 40 minutes). Add someone to the Entra
group and they show up in Databricks on their own; remove them and they're deactivated.
Docs: https://docs.databricks.com/aws/en/admin/users-groups/scim/aad

## HIPAA notes
- Databricks Apps and Genie are HIPAA-supported when CSP is on and a BAA is signed.
- The PHI stays inside the Databricks App; Teams only displays it, covered by your Microsoft/Teams BAA.

## Links
- Databricks Apps + Genie: https://docs.databricks.com/aws/en/dev-tools/databricks-apps/genie
- Genie Conversation API: https://docs.databricks.com/aws/en/genie/conversation-api
- App authorization (OBO): https://docs.databricks.com/aws/en/dev-tools/databricks-apps/auth
- Embedding apps: https://docs.databricks.com/aws/en/dev-tools/databricks-apps/embed
