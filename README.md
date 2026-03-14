# Jetstar Ops Agent

A stateful AI agent built with LangGraph that handles passenger queries for Jetstar Airways — flight status, rebooking options, and travel credits.

Built to explore LangGraph's stateful agent architecture using aviation as the domain. Aviation's real-time constraints and operational complexity make it an ideal domain for testing agentic reasoning and conditional routing.

## What it does

Takes a natural language passenger query → agent reasons about which tool to call → tool executes → agent reads result → formats a clean answer. Runs in a loop with a safety limit of 5 iterations.

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

## Tech stack

- **LangGraph** — stateful graph with conditional routing
- **LangChain** — tool definitions and LLM integration
- **GPT-4o-mini** — reasoning and response formatting
- **Python 3.10+**

## Project structure
```
jetstar-ops-agent/
├── agent/
│   ├── __init__.py   # package entry point
│   ├── state.py      # AgentState TypedDict
│   ├── tools.py      # 3 tools with @tool decorator
│   ├── nodes.py      # agent_node, tool_node, final_answer_node
│   └── graph.py      # StateGraph with conditional routing
├── main.py
├── requirements.txt
└── .env.example
```

## How to run
```bash
git clone https://github.com/krrishkhanna/Jetstar-Ops-agent
cd Jetstar-Ops-agent
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your OpenAI API key
python3 main.py
```

## Example queries
```
"What is the status of Jetstar flight JQ202?"
"My flight JQ303 was cancelled. What are my rebooking options?"
"Check travel credits for passenger JS003"
```

## Design decisions

**Why LangGraph over a plain LangChain chain?**
A chain is linear — A → B → C → done. This agent needs to loop: call a tool, read the result, decide if it needs another tool, loop back. That cycle is only possible with LangGraph's directed graph structure.

**Why three separate nodes?**
Single responsibility. agent_node thinks. tool_node acts. final_answer_node communicates. Each is independently testable and easy to extend — adding a 4th tool only requires changes to tools.py.

**Why an iteration limit?**
Production safety. A buggy routing function could loop forever. The limit guarantees the agent always terminates.

## What I would add next

- MCP server wrapping the tools so any model can use them
- LangSmith tracing for production observability
- Async support via asyncio.gather() for concurrent passengers
- Checkpointing so sessions persist across conversations
