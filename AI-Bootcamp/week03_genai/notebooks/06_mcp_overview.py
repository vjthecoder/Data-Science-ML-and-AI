import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __(mo):
    mo.md(
        r"""
        # 06. MCP — Model Context Protocol

        ## Theory

        **Level 1 (10-year-old):** Imagine every app spoke a different language, so your AI helper
        needed a separate translator for each one. MCP is a *shared language* so the AI can plug
        into any app — files, calendars, databases — using the same connector every time.

        **Level 2 (College Student):** The Model Context Protocol (MCP) is an open standard for
        connecting LLM applications to external **tools**, **resources** (readable data), and
        **prompts**. An **MCP server** exposes capabilities; an **MCP client** (inside the AI app)
        consumes them over a standard transport (stdio for local, HTTP/SSE for remote). Instead of
        hand-writing a bespoke integration per tool, you write/host an MCP server once and any
        MCP-compatible client can use it.

        **Level 3 (Industry Professional):** MCP decouples capability providers from AI
        applications — the same GitHub or database MCP server works in Claude Desktop, an IDE, or
        your custom agent. Benefits: reuse, consistent auth, and a clean security boundary
        (credentials live with the server/host, not in the model's context). The Anthropic SDK
        can connect to remote MCP servers directly (`mcp_servers` parameter) or convert local MCP
        tools into tool-runner tools. Treat MCP servers like any dependency: pin versions, scope
        permissions, and audit what data/actions they expose.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Visual Explanation

        ```
        ┌──────────────────────────┐         MCP (standard protocol)        ┌────────────────┐
        │  LLM App (MCP client)    │ ◄───────────────────────────────────► │  MCP Server A  │  files
        │  - Claude Desktop        │   tools / resources / prompts          ├────────────────┤
        │  - your custom agent     │ ◄───────────────────────────────────► │  MCP Server B  │  GitHub
        │  - an IDE                 │                                        ├────────────────┤
        └──────────────────────────┘ ◄───────────────────────────────────► │  MCP Server C  │  database
                                                                            └────────────────┘
        Write a server ONCE → every MCP client can use it.
        Transports: stdio (local) | HTTP+SSE (remote)
        ```
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## MCP Primitives

        | Primitive  | What it is                          | Example                       |
        |------------|-------------------------------------|-------------------------------|
        | **Tools**  | Functions the model can invoke      | `create_issue`, `run_query`   |
        | **Resources** | Readable data the model can load | a file, a wiki page, a row     |
        | **Prompts** | Reusable prompt templates          | "summarize this PR"           |
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Real-World Example: a minimal MCP server (Python)

        ```python
        # pip install mcp
        from mcp.server.fastmcp import FastMCP

        mcp = FastMCP("demo-server")

        @mcp.tool()
        def add(a: int, b: int) -> int:
            \"\"\"Add two integers.\"\"\"
            return a + b

        @mcp.resource("greeting://{name}")
        def greeting(name: str) -> str:
            \"\"\"A friendly greeting resource.\"\"\"
            return f"Hello, {name}!"

        if __name__ == "__main__":
            mcp.run()      # serves over stdio by default
        ```

        ## Consuming MCP from the Anthropic SDK

        Convert local MCP tools into tool-runner tools:

        ```python
        # pip install "anthropic[mcp]"
        from anthropic import AsyncAnthropic
        from anthropic.lib.tools.mcp import async_mcp_tool
        from mcp import ClientSession
        from mcp.client.stdio import stdio_client, StdioServerParameters

        client = AsyncAnthropic()

        async with stdio_client(StdioServerParameters(command="python", args=["demo_server.py"])) as (r, w):
            async with ClientSession(r, w) as session:
                await session.initialize()
                tools = (await session.list_tools()).tools
                runner = client.beta.messages.tool_runner(
                    model="claude-opus-4-8",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": "Use the tools to add 21 and 21."}],
                    tools=[async_mcp_tool(t, session) for t in tools],
                )
                async for message in runner:
                    print(message)
        ```

        Alternatively, point the API at a **remote** MCP server with the `mcp_servers` parameter so
        Claude connects to it directly.
        """
    )
    return


@app.cell
def __():
    # Offline-safe conceptual model of an MCP server (a registry of tools + resources)
    class MiniMCPServer:
        def __init__(self, name):
            self.name = name
            self.tools = {}
            self.resources = {}

        def tool(self, fn):
            self.tools[fn.__name__] = fn
            return fn

        def resource(self, uri):
            def deco(fn):
                self.resources[uri] = fn
                return fn
            return deco

        def list_tools(self):
            return list(self.tools)

        def call_tool(self, name, **kwargs):
            return self.tools[name](**kwargs)

    server = MiniMCPServer("demo")

    @server.tool
    def add(a: int, b: int) -> int:
        return a + b

    print("Exposed tools:", server.list_tools())
    print("add(21, 21) =", server.call_tool("add", a=21, b=21))
    return MiniMCPServer, add, server


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Coding Exercise

        1. Extend `MiniMCPServer` with a `subtract` and `multiply` tool and a
           `config://app` resource that returns a dict.
        2. Write a tiny "client" function that lists the server's tools and calls one by name with
           arguments — mimicking the MCP request/response shape.
        3. (Stretch, requires `pip install mcp`) Build the real FastMCP server above and call it
           from the Anthropic tool runner.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Assignment
        See `../assignments/week03_assignments.md` — Assignment 6.

        ## Interview Questions
        See `../../interview-prep/week03_genai_questions.md` — Section: MCP.

        ## Industry Use Cases
        - Reusable connectors (GitHub, Slack, databases) shared across AI apps
        - IDE/desktop assistants that plug into many tools via one protocol
        - Enterprise platforms standardizing tool access + auth across teams

        ## Common Mistakes
        - Putting credentials in the model's context instead of the server/host
        - Over-broad MCP servers that expose more than the task needs
        - Treating MCP servers as un-versioned, un-audited dependencies

        ## Best Practices
        - Keep secrets server-side; scope permissions to least privilege
        - Pin server versions; audit exposed tools/resources
        - Reuse community MCP servers before building your own

        ## Further Reading
        - Model Context Protocol specification (modelcontextprotocol.io)
        - Anthropic MCP documentation and the `mcp` Python SDK
        - The growing ecosystem of open-source MCP servers
        """
    )
    return


if __name__ == "__main__":
    app.run()
