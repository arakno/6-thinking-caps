# 6-thinking-caps
Multi-agent project to help make decisions


A system where an LLM uses **tools** and **control flow** to arive at a decision given a single prompt.

**Core ideas to explore:**

1. **Tool Use:** Give the model "hands" (e.g., ability to control a browser, run code, or query an API).
2. **Routing:** Have a "router" step that decides *which* specialized agent should handle a user request.

**Evaluation:**
Implement a loop where one agent critiques the output of another (e.g., a code reviewer agent checking a coder agent's work).
