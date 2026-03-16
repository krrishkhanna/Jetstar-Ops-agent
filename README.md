# Jetstar Ops Agent

An AI agent that helps Jetstar passengers check flight status, find rebooking options, and look up travel credits. Built with LangGraph.

I made this to learn how LangGraph handles back-and-forth conversations. Airlines are messy—lots of real-time stuff, edge cases, and decisions to make. Perfect for testing an agent.

## How it works

You ask a question → the agent figures out which tool it needs → runs it → reads what happened → keeps going if it needs to. Max 5 loops to stay safe.

```
your question
      ↓
 [agent]          hmm, what should I do?
      ↓
 [tool]           okay, doing it
      ↓
 [agent]          got it, done?
      ↓
 [final]          here's your answer
      ↓
  response
```

## What's inside

- **LangGraph** — handles the back-and-forth, routing to tools
- **LangChain** — tool setup and LLM stuff
- **GPT-4o-mini** — the brain
- **Python 3.10+**

## Files

```
jetstar-ops-agent/
├── agent/
│   ├── __init__.py
│   ├── state.py          # conversation state
│   ├── tools.py          # the 3 tools
│   ├── nodes.py          # agent, tool, final
│   └── graph.py          # wires it together
├── tests/
│   ├── __init__.py
│   ├── test_state.py
│   ├── test_tools.py
│   ├── test_nodes.py
│   └── test_graph.py
├── main.py
├── requirements.txt
└── .env.example
```

## Get it running

```bash
git clone https://github.com/krrishkhanna/Jetstar-Ops-agent
cd Jetstar-Ops-agent
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # put your OpenAI key here
python3 main.py
```

## Examples

```
"What's the status on JQ202?"
"JQ303 got cancelled. What can I do?"
"What travel credits do I have? (JS003)"
```

## Why I built it this way

**LangGraph instead of a chain?** Chains go step-by-step, done. This needs loops. Call a tool, see what it says, maybe call another, rinse and repeat. That's a graph.

**Why three separate nodes?** Keeps things clean. One thinks, one acts, one talks to you. Easier to test, easier to add more tools later.

**Why cap it at 5 loops?** Don't want a broken routing function hanging forever. This kills it if it goes sideways.

## Maybe later

- Wrap the tools in an MCP server
- LangSmith observability for prod
- Run multiple passengers at once with async
- Keep conversations between sessions

## Known limitations

- Mock data only — no connection to live Jetstar systems
- Flight number must be in JQ + 3-4 digit format
- Passenger IDs must match JS001, JS002, JS003
- Single passenger per query — no batch processing yet
- No session memory between separate runs
