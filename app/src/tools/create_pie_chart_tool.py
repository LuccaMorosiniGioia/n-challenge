create_pie_chart_tool = {
    "type": "function",
    "function": {
        "name": "create_pie_chart_tool",
        "description": f"""
                Use this function to create a pie chart. You must ensure the data you pass is in the correct format.
                Use this graph whenever you need to compare pertentages of a whole for a single variable.
                """,
        "parameters": {
            "type": "object",
            "properties": {
                "sizes": {
                    "type": "string",
                    "description": f"""
                                Array of values with the size of each slice in the format: [value1, value2, value3]
                                # Example:
                                    [15, 30, 45, 10]
                                # Return Type:
                                    1-D Array on the format:
                                    []
                                """,
                },
                "labels": {
                    "type": "string",
                    "description": f"""
                                Array with the label for each size in the format: [label1, label2, label3]
                                All the elements of the array must be a string.
                                Example:
                                    If you need to return null and the array is made up string elements, you should return "null" instead of null.
                                # Return Type:
                                    1-D Array on the format:
                                    []
                                """,
                },
                "title": {
                    "type": "string",
                    "description": f"""
                                Title of the pie chart.
                                """,
                },
            },
            "required": ["sizes", "labels", "title"],
        },
    },
}
