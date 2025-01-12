create_scatter_chart_tool = {
    "type": "function",
    "function": {
        "name": "create_scatter_chart",
        "description": f"""
                Use this function to create a scatter plot. You must ensure the data you pass is in the correct format.]
                Use this graph when you want to compare more than two variables.
                """,
        "parameters": {
            "type": "object",
            "properties": {
                "classes": {
                    "type": "string",
                    "description": f"""
                                Array with the classes in the format: ["className1", "className2", "className3"].
                                # Return Type:
                                    1-D Array on the format:
                                    []
                                """,
                },
                "x-axis": {
                    "type": "string",
                    "description": f"""
                                Matrix with the x values for each class in the format: [[value_0_class_1, value_1_class_1], [value_0_class_2, value_1_class_2]].
                                The number of rows must be the same as the number of classes.
                                Always return dates as strings on format "DD-MM-YYYY", "MM-YYYY" or "YYYY".
                                # Example:
                                    ["01-01-2021", "01-02-2021"]
                                All the elements of the array must be of the same type.
                                Example:
                                    If you need to return null and the array is made up string elements, you should return "null" instead of null.
                                # Return Type:
                                    2-D Matrix with the same numbers of rows as classes on the format:
                                    [[], [], ...]
                                """,
                },
                "y-axis": {
                    "type": "string",
                    "description": f"""
                                Matrix with the y values for each class in the format: [[value_0_class_1, value_1_class_1], [value_0_class_2, value_1_class_2]].
                                The number of rows must be the same as the number of classes.
                                All the elements of the array must be of the same type.
                                Example:
                                    If you need to return null and the array is made up string elements, you should return "null" instead of null.
                                # Return Type:
                                    2-D Matrix with the same numbers of rows as classes on the format:
                                    [[], [], ...]
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
            "required": ["classes", "x-axis", "y-axis", "x-label", "y-label", "title"],
        },
    },
}
