# Path 4: Native Databricks in Teams (Public Preview)

**What you'll build:** the same Genie assistant, but as a **chat** inside Teams (people @-mention it),
delivered by Databricks rather than as a web tab. This is the most Teams-native experience. It's
**Public Preview** today, so weigh that against Path 3's fully-GA status.

There are two flavors. **4a** is the quick, turnkey one. **4b** is for a custom agent and takes more work.

---

## 4a. Genie app for Microsoft Teams (turnkey, lightest effort)

**How it flows:**
```
Person in Teams  ->  @Databricks Genie  ->  Genie (writes + runs the SQL)  ->  your tables
```

### Before you start
- A Genie space (see Path 3, Step 2).
- Your people synced into Databricks (see Path 3, Step 1).
- An account/workspace admin (to turn on the preview) and a Teams admin (to install the app).
- For sensitive data: Compliance Security Profile on, BAA signed.

### Steps (in order)
1. **Create a Genie space** (the brain) - same as Path 3, Step 2.
2. **Confirm your people are in Databricks** (SCIM) - same as Path 3, Step 1 - and grant the group
   CAN VIEW on the space, SELECT on the tables, CAN USE on the warehouse.
3. **Turn on the preview:** in the Databricks account/workspace **Previews** page, enable the Genie app for Microsoft Teams.
4. **Set the safety flags:** turn **on** "Allow connection to collaboration platforms" and turn **off**
   "Allow public messages in collaboration platforms" (so sensitive answers can't land in open channels).
5. **Install in Teams:** your Teams admin installs the Databricks Genie app from the Teams app store.
6. **Connect it** to your workspace and Genie space; people sign in with their Microsoft identity.
7. **Use it:** @-mention the app and ask questions. Each person is queried as themselves.

### Watch-outs
- **Public Preview**, and **no Private Link yet**, so it may not fit a private-networking requirement today.
- It's on the HIPAA supported list, but confirm the safety flags above and your Teams/M365 BAA.

Docs: https://docs.databricks.com/aws/en/integrations/msft-teams

---

## 4b. Connect a custom Databricks agent to Teams via a bot (more effort)

Use this when you want a custom agent (not just a single Genie space) in Teams. It uses Microsoft Azure to
host a small bot that passes messages to your Databricks agent.

**How it flows:**
```
Person in Teams  ->  Azure bot  ->  your Databricks agent  ->  Genie / your tables
```

### Before you start
- A deployed Databricks agent (built with the Agent Framework; it can call your Genie space).
- An Azure subscription (for an Azure Bot plus a small web app).
- Someone comfortable with Azure and app registrations.

### Steps (in order)
1. **Build and deploy your agent** in Databricks.
2. **Stand up the bot on Azure:** an Azure Bot plus a web app, using Databricks' sample bot code.
3. **Set up sign-in passthrough (OAuth federation)** so the bot calls Databricks as the signed-in person.
4. **Register and publish** the bot in Teams.
5. **Use it:** chat with the bot in Teams.

### Watch-outs
- **Public Preview**, and it routes data through **Azure Bot Service + a web app**, so those Azure pieces
  must be HIPAA-configured under your Microsoft BAA. **Confirm HIPAA coverage before using sensitive data.**
- The most moving parts of any option here.

Docs: https://learn.microsoft.com/en-us/azure/databricks/agents/agent-framework/teams-agent

---

## Which flavor?
- Want the quickest native chat and only need one Genie space? **4a.**
- Need a custom multi-step agent in Teams and have Azure skills? **4b.**
- Need something GA and production-ready today? Use **Path 3** instead.
