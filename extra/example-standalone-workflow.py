# This is NOT a fully functional set of code
# This is just a high-level code flow showing how to 
# use existing AGENTS.md and SKILL.md in a standalone agent

from anthropic import Anthropic

# Load the same files Copilot uses
with open("AGENTS.md") as f:
    agent_instructions = f.read()

with open(".github/skills/resume-scoring/SKILL.md") as f:
    skill_rubric = f.read()

# Combine them into a system prompt
system_prompt = f"""
{agent_instructions}

## Scoring Rubric
{skill_rubric}
"""

# Use with any LLM
client = Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    system=system_prompt,
    messages=[{"role": "user", "content": f"Score this resume:\n\n{resume_text}"}]
)
