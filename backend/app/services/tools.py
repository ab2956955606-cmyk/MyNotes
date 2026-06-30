AGENT_TOOLS = [
    {
        "name": "create_task",
        "description": "Create a scheduled task with time, text and rationale.",
        "schema": {"time": "HH:MM", "text": "string", "reason": "string"},
    },
    {
        "name": "update_task",
        "description": "Adjust a task when the user misses or delays work.",
        "schema": {"task_id": "string", "new_time": "HH:MM", "new_text": "string"},
    },
    {
        "name": "search_materials",
        "description": "Retrieve relevant JD, course or note snippets from the RAG store.",
        "schema": {"query": "string", "top_k": "number"},
    },
    {
        "name": "summarize_week",
        "description": "Summarize completed tasks and unresolved risks for weekly review.",
        "schema": {"week_start": "date", "week_end": "date"},
    },
]


def list_tools():
    return {"tools": AGENT_TOOLS}
