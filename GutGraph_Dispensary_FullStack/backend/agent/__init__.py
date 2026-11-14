"""GutGraph agent parliament — grokbot-clone-inspired agent runtime.

Modules:
  personas  — the 8 demo microbe agents + Mixologist (from the Notion master plan)
  llm       — DeepSeek/OpenRouter client, streamed; failures raise LLMError
              instead of silently falling back (no key at all = mock mode)
  loop      — single agent turn: truth layer decides the vote, model words it
  room      — GutParliament: serial agent queue over a shared MealContext
  pipeline  — Mixologist orchestrator: parse -> truth layer -> parliament -> drink

Demo-morning check: `python -m agent.llm` makes one live call and prints the
verdict, so a bad key or an empty balance is caught before judges are watching.
"""
