"""GutGraph agent parliament — grokbot-clone-inspired agent runtime.

Modules:
  personas  — the 8 demo microbe agents + Mixologist (from the Notion master plan)
  llm       — DeepSeek client with automatic mock fallback (no key = demo mode)
  loop      — single agent turn: context -> model -> validate -> vote
  room      — GutParliament: serial agent queue over a shared MealContext
  pipeline  — Mixologist orchestrator: parse -> truth layer -> parliament -> drink
"""
