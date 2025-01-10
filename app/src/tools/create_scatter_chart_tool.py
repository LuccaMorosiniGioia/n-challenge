create_scatter_chart_tool = {
    "type": "function",
    "function": {
        "name": "create_scatter_chart",
        "description": f"""
                Use this function to create a scatter plot. You must ensure the data you pass is in the correct format.
                """,
        "parameters": {
            "type": "object",
            "properties": {
                "classes": {
                    "type": "string",
                    "description": f"""
                                Array with the classes in the format: ["className1", "className2", "className3"].
                                """,
                },
                "x-axis": {
                    "type": "string",
                    "description": f"""
                                Matrix with the x values for each class in the format: [[value_0_class_1, value_1_class_1], [value_0_class_2, value_1_class_2]].
                                The number of rows must be the same as the number of classes.
                                """,
                },
                "y-axis": {
                    "type": "string",
                    "description": f"""
                                Matrix with the y values for each class in the format: [[value_0_class_1, value_1_class_1], [value_0_class_2, value_1_class_2]].
                                The number of rows must be the same as the number of classes.
                                """,
                },
                "x-label": {
                    "type": "string",
                    "description": f"""
                                Label for the x-axis of the chart.
                                """,
                },
                "y-label": {
                    "type": "string",
                    "description": f"""
                                Label for the y-axis of the chart.
                                """,
                },
                "title": {
                    "type": "string",
                    "description": f"""
                                Title of the chart.
                                """,
                },
            },
            "required": ["classes", "x-axis", "y-axis"],
        },
    },
}
