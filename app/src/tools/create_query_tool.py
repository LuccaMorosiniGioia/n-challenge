create_query_tool = {
    "type": "function",
    "function": {
        "name": "create_query",
        "description": f"""
                Use this function to query the database to answer users questions.
                """,
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": f"""
                                The question the user asked'.
                                """,
                },
            },
            "required": ["question"],
        },
    },
}
