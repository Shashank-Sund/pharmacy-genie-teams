"""
Minimal Databricks App: a chat box that asks a Genie space and shows the answer.

It runs each query on behalf of the signed-in user (OBO), so Unity Catalog applies
that person's permissions. This is a starting skeleton, not production code:
adapt the answer parsing and add error handling for your needs.
"""
import os
from flask import Flask, request, jsonify, render_template_string
from databricks.sdk import WorkspaceClient

app = Flask(__name__)

GENIE_SPACE_ID = os.environ["GENIE_SPACE_ID"]
HOST = os.environ.get("DATABRICKS_HOST")  # set automatically inside Databricks Apps

PAGE = """
<!doctype html>
<title>Pharmacy Inventory Assistant</title>
<h2>Pharmacy Inventory Assistant</h2>
<input id="q" style="width:70%" placeholder="e.g. How many units are on hand today?">
<button onclick="ask()">Ask</button>
<pre id="out"></pre>
<script>
async function ask(){
  const q = document.getElementById('q').value;
  document.getElementById('out').textContent = 'Thinking...';
  const r = await fetch('/ask', {method:'POST', headers:{'Content-Type':'application/json'},
                                 body: JSON.stringify({question:q})});
  const d = await r.json();
  document.getElementById('out').textContent = d.answer + (d.sql ? '\\n\\nSQL:\\n'+d.sql : '');
}
</script>
"""


def workspace_client():
    # OBO: use the signed-in user's forwarded token so queries run as THAT user.
    user_token = request.headers.get("X-Forwarded-Access-Token")
    if user_token:
        return WorkspaceClient(host=HOST, token=user_token)
    # Local-dev fallback: your own CLI/profile auth.
    return WorkspaceClient()


@app.route("/")
def home():
    return render_template_string(PAGE)


@app.route("/ask", methods=["POST"])
def ask():
    question = (request.json or {}).get("question", "").strip()
    if not question:
        return jsonify({"answer": "Please type a question.", "sql": ""})

    w = workspace_client()
    result = w.genie.start_conversation_and_wait(space_id=GENIE_SPACE_ID, content=question)

    # Pull the natural-language answer and the SQL if present.
    # (Exact fields can vary by SDK version; see the Conversation API docs.)
    answer, sql = "", ""
    for a in (result.attachments or []):
        text = getattr(a, "text", None)
        if text and getattr(text, "content", None):
            answer = text.content
        query = getattr(a, "query", None)
        if query and getattr(query, "query", None):
            sql = query.query
    return jsonify({"answer": answer or "No answer returned.", "sql": sql})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("DATABRICKS_APP_PORT", "8080")))
