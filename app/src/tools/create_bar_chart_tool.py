create_bar_chart_tool = {
    "type": "function",
    "function": {
        "name": "create_bar_chart",
        "description": f"""
                Use this function to create a bar chart. You must ensure the data you pass is in the correct format.
                """,
        "parameters": {
            "type": "object",
            "properties": {
                "x-axis": {
                    "type": "string",
                    "description": f"""
                                Array with the x values of the bars in the format: [value1, value2, value3]
                                """,
                },
                "y-axis": {
                    "type": "string",
                    "description": f"""
                                Array with the y values of the bars in the format: [value1, value2, value3]
                                """,
                },
                "y-label": {
                    "type": "string",
                    "description": f"""
                                Label for the y-axis of the bar chart.
                                """,
                },
                "title": {
                    "type": "string",
                    "description": f"""
                                Title of the bar chart.
                                """,
                },
            },
            "required": ["x-axis", "y-axis"],
        },
    },
}
