memory = {}
MAX_MESSAGES = 12  # keep latest 12 messages in memory


def get_memory(user_id: str):
    if user_id not in memory:
        memory[user_id] = []
    return memory[user_id]


def trim_history(history: list) -> None:
    """
    Keep system message (if present) + latest messages.
    Mutates the same history list in place.
    """
    if len(history) <= MAX_MESSAGES:
        return

    system_part = []
    rest = history

    if history and history[0].get("role") == "system":
        system_part = [history[0]]
        rest = history[1:]

    keep_rest = MAX_MESSAGES - len(system_part)
    trimmed = system_part + rest[-keep_rest:]

    history.clear()
    history.extend(trimmed)