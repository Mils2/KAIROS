# KAIROS agent rules

Project: KAIROS trading bot

Operational rules:
- Use only ./control/bot_control.sh status
- Use only ./control/bot_control.sh health
- Never run python main.py directly
- Never place trades
- Never modify risk values automatically
- Never call exchange actions from the agent
- Treat this workspace as monitor-only unless the user explicitly edits code manually
