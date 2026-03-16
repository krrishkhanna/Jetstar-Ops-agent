# jetstar-ops-agent

A stateful AI agent built with LangGraph that handles passenger queries for Jetstar Airways — flight status, rebooking options, and travel credits.

Built to explore LangGraph's stateful agent architecture using aviation as the domain. Aviation's real-time constraints and operational complexity make it an ideal domain for testing agentic reasoning and conditional routing.

> Read more about LangGraph: [LangGraph Docs](https://langchain-ai.github.io/langgraph/)

---

## Architecture
```
passenger query
      ↓
 [agent node]     thinks, decides which tool to call
      ↓  ← conditional routing via should_continue()
 [tool node]      executes the chosen tool
      ↓
 [agent node]     reads tool result, decides if done
      ↓
[final node]      formats clean response for passenger
      ↓
  final answer
```

---

## 1. Project Setup

### 1.1. Install Python and Dependencies

> Make sure you have Python 3.10+ installed before starting.

Steps:

1. Clone the repository:
```bash
   git clone https://github.com/krrishkhanna/Jetstar-Ops-agent
   cd Jetstar-Ops-agent
```

2. Create and activate a virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate
```

3. Confirm Python version:
```bash
   python --version
```

4. Install dependencies:
```bash
   pip install -r requirements.txt
```

5. Set up your environment variables:
```bash
   cp .env.example .env
   # Add your OpenAI API key to .env
```

> You can deactivate the venv at any time by running `deactivate`

---

### 1.2. Update Dependencies

> Important: Keep dependencies updated to ensure consistent setup across environments.

If your changes require new packages:
```bash
pip install <package>
pip freeze > requirements.txt
```

---

## 2. Project Structure
```
jetstar-ops-agent/
├── agent/
│   ├── __init__.py   # package entry point
│   ├── state.py      # AgentState TypedDict
│   ├── tools.py      # 3 tools with @tool decorator
│   ├── nodes.py      # agent_node, tool_node, final_answer_node
│   └── graph.py      # StateGraph with conditional routing
├── tests/
│   └── tools.py      # unit tests for all 3 tools
├── main.py           # entry point
├── requirements.txt
├── .env.example
└── README.md
```

---

## 3. General Development Commands

> Make sure your virtual environment is active before running any commands.

Activate virtual environment:
```bash
source venv/bin/activate
```

Run the agent:
```bash
python3 main.py
```

Run tests:
```bash
python3 tests/tools.py
```

Deactivate virtual environment:
```bash
deactivate
```

---

## 4. Example Queries
```
"What is the status of Jetstar flight JQ202?"
"My flight JQ303 was cancelled. What are my rebooking options?"
"Check travel credits for passenger JS003"
```

---

## 5. Design Decisions

<<<<<<< HEAD
- Wrap the tools in an MCP server
- LangSmith observability for prod
- Run multiple passengers at once with async
- Keep conversations between sessions

## Known limitations
=======
**Why LangGraph over a plain LangChain chain?**
A chain is linear — A → B → C → done. This agent needs to loop: call a tool, read the result, decide if it needs another tool, loop back. That cycle is only possible with LangGraph's directed graph structure.

**Why three separate nodes?**
Single responsibility. `agent_node` thinks. `tool_node` acts. `final_answer_node` communicates. Each is independently testable and easy to extend — adding a 4th tool only requires changes to `tools.py`.

**Why an iteration limit?**
Production safety. A buggy routing function could loop forever. The limit guarantees the agent always terminates.

---

## 6. Known Limitations
>>>>>>> 844c893 (docs: restructure README with professional formatting)

- Mock data only — no connection to live Jetstar systems
- Flight number must be in JQ + 3-4 digit format
- Passenger IDs must match JS001, JS002, JS003
- Single passenger per query — no batch processing yet
- No session memory between separate runs
<<<<<<< HEAD
=======

---

## 7. What I Would Add Next

- MCP server wrapping the tools so any model can use them
- LangSmith tracing for production observability
- Async support via `asyncio.gather()` for concurrent passengers
- Checkpointing so sessions persist across conversations
>>>>>>> 844c893 (docs: restructure README with professional formatting)
