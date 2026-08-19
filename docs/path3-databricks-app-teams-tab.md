# Path 3: A Databricks App in a Teams tab (fully GA)

**What you'll build:** a chat box, living in a Microsoft Teams tab, where people ask plain-English
questions about your data and get exact answers. Each person only sees data they're allowed to.
Everything runs in Databricks.

**How it flows:**
```
Person in Teams  ->  Databricks App (chat box)  ->  Genie (writes + runs the SQL)  ->  your tables
```

**Three pieces, in plain words:**
- **Genie** is like a data analyst: it turns a plain-English question into SQL and runs it.
- A **Databricks App** is a small web page with a chat box that hands questions to Genie.
- A **Teams tab** is just that web page, pinned inside a Teams channel.

Because the app and the data both live in Databricks, there's no cross-cloud networking to build.

**What makes it per-user:** the app runs each query *as the signed-in person* (called OBO), so Unity
Catalog only returns what that person is allowed to see. No shared robot account.

---

## Before you start

- A Databricks workspace with Unity Catalog.
- Your data already in Unity Catalog tables.
- Permission to create a Databricks App.
- Your people already able to sign in to Databricks (see Step 1).
- For sensitive data (PHI/HIPAA): the Compliance Security Profile turned on and a signed Databricks BAA.

Estimated effort: a day or two for a first working version.

---

## Steps (in order)

### Step 1 - Confirm your people exist in Databricks
Per-user access only works if each person is a Databricks user. Most orgs sync this automatically from
Microsoft Entra ID using **SCIM**: an admin sets it up once, assigns a group (for example
`inventory-users`), and Entra copies those people into Databricks (right away, then every 20-40 minutes).
Add someone to the group later and they appear on their own.
*Why first: nothing per-user works until your people exist in Databricks.*
Docs: https://docs.databricks.com/aws/en/admin/users-groups/scim/aad

### Step 2 - Create a Genie space (the brain)
In Databricks, open **Genie** and create a space. Add the tables you want people to ask about. Add a few
example questions and one or two lines of plain instructions so answers come out consistent. Copy the
**space ID** from the URL (the long id after `/genie/`).
*Why: this is the thing that understands questions and writes the SQL.*

### Step 3 - Give your group access (three grants)
Grant the group from Step 1:
- **CAN VIEW** on the Genie space
- **SELECT** on the tables
- **CAN USE** on the SQL warehouse the space uses

Grant to the group once; new members inherit it automatically.
*Why: Genie runs as each person, so each person needs these rights.*

### Step 4 - Build the app (the chat box)
Create a Databricks App (**Compute > Apps > Create app**, or the CLI) from a template. The [`app/`](../app)
folder in this repo is a minimal starting point. Set an environment variable `GENIE_SPACE_ID` to the id
from Step 2.
*Why: this is the web page people will actually type into.*

### Step 5 - Turn on per-user (OBO)
In the app's settings, enable **user authorization** and add the scopes `sql` and `genie`. Now Databricks
passes the signed-in person's token to the app, and the app queries Genie as that person.
*Why: this is what makes each person see only their own permitted data.*
Docs: https://docs.databricks.com/aws/en/dev-tools/databricks-apps/auth

### Step 6 - Deploy and test
Deploy the app. Databricks gives you a URL. Open it and ask a test question to confirm it works.

### Step 7 - Put it in Teams (as a tab)
In Teams, add a website/app tab pointing at your app URL. Add the app's domain to the Teams app manifest's
`validDomains`, and set up single sign-on so the Teams user signs in as their Databricks identity (using the
same Entra tenant keeps this simple). Pin the tab in the channel your people use.

**Done.** People open the tab, ask questions in plain English, and each sees only what they're allowed to.

---

## HIPAA notes
- Databricks Apps and Genie can be used with PHI when the Compliance Security Profile is on and a BAA is signed.
- The data stays inside the Databricks App; Teams only displays it, which is covered by your Microsoft/Teams BAA.

## Links
- Databricks Apps + Genie: https://docs.databricks.com/aws/en/dev-tools/databricks-apps/genie
- Genie Conversation API: https://docs.databricks.com/aws/en/genie/conversation-api
- App authorization (OBO): https://docs.databricks.com/aws/en/dev-tools/databricks-apps/auth
- Embedding apps: https://docs.databricks.com/aws/en/dev-tools/databricks-apps/embed
- SCIM from Entra ID: https://docs.databricks.com/aws/en/admin/users-groups/scim/aad
