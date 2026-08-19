# Path 4: Native Databricks in Teams (Public Preview)

**Goal:** the same Genie assistant, but as a **chat** inside Teams (users @-mention it), delivered by
Databricks rather than a web tab. This is the most Teams-native experience. It's **Public Preview**
today, so weigh that against Path 3's GA status.

There are two flavors.

## 4a. Genie app for Microsoft Teams (turnkey, lightest effort)

People type `@Databricks Genie` in Teams and ask questions.

### Prerequisites
- A Genie space (see Path 3, step 1).
- An account/workspace admin to turn on the preview.
- A Teams admin to install the app.
- For PHI: CSP on, BAA signed.

### Steps
1. **Enable the preview:** in the Databricks account/workspace **Previews** page, turn on the Genie app for Microsoft Teams.
2. **Set the safety flags:** turn **on** "Allow connection to collaboration platforms" and turn **off**
   "Allow public messages in collaboration platforms" (so PHI can't land in open channels).
3. **Install in Teams:** your Teams admin installs the Databricks Genie app from the Teams app store.
4. **Connect it** to your workspace and Genie space; users consent with their Microsoft identity.
5. **Use it:** @-mention the app in a chat or channel and ask questions. Each user is queried as themselves.

### Watch-outs
- **Public Preview**, and **no Private Link yet**, so it may not fit a private-networking requirement today.
- On the HIPAA supported list, but confirm the collaboration-platform flags and your Teams/M365 BAA.

Docs: https://docs.databricks.com/aws/en/integrations/msft-teams

## 4b. Connect a Databricks agent to Teams via a bot (more effort)

For when you want a custom agent (not just Genie) in Teams. This uses Microsoft Azure to host a bot
that forwards messages to your Databricks agent.

### Prerequisites
- A deployed Databricks agent (built with the Agent Framework; it can call your Genie space).
- An Azure subscription (for Azure Bot Service + an Azure Web App).
- Someone comfortable with Azure and app registrations.

### Steps (high level)
1. **Deploy your agent** in Databricks.
2. **Stand up the bot** on Azure: an Azure Bot plus a Web App, using Databricks' sample bot code.
3. **Set up OAuth federation** so the bot can call Databricks on behalf of the signed-in user (OBO).
4. **Register and publish** the bot in Teams.
5. **Use it:** chat with the bot in Teams.

### Watch-outs
- **Public Preview**, and it routes PHI through **Azure Bot Service + a Web App**, so those Azure pieces
  must be HIPAA-configured under your Microsoft BAA. **Confirm HIPAA coverage before using PHI.**
- More moving parts than 4a or Path 3.

Docs: https://learn.microsoft.com/en-us/azure/databricks/agents/agent-framework/teams-agent

## Which flavor?
- Want the quickest native chat and only need Genie? **4a.**
- Need a custom multi-step agent in Teams and have Azure skills? **4b.**
- Need something GA and production-ready now? Use **Path 3** instead.
