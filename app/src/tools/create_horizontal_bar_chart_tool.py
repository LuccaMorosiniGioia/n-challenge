create_horizontal_bar_chart_tool = {
    "type": "function",
    "function": {
        "name": "create_horizontal_bar_chart_tool",
        "description": f"""
                Use this function to create a horizontal bar chart. You must ensure the data you pass is in the correct format.
                Use this graph whenever you need to compare up to two variables.
                """,
        "parameters": {
            "type": "object",
            "properties": {
                "x-axis": {
                    "type": "string",
                    "description": f"""
                                Array with the x values of the bars in the format: [value1, value2, value3]
                                Always return dates as strings on format "DD-MM-YYYY", "MM-YYYY" or "YYYY".
                                # Example:
                                    ["01-01-2021", "01-02-2021"]
                                All the elements of the array must be of the same type.
                                Example:
                                    If you need to return null and the array is made up string elements, you should return "null" instead of null.
                                # Return Type:
                                    1-D Array on the format:
                                    []
                                """,
                },
                "y-axis": {
                    "type": "string",
                    "description": f"""
                                Array with the y values of the bars in the format: [value1, value2, value3]
                                All the elements of the array must be of the same type.
                                Example:
                                    If you need to return null and the array is made up string elements, you should return "null" instead of null.
                                # Return Type:
                                    1-D Array on the format:
                                    []
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
            "required": ["x-axis", "y-axis", "x-label", "y-label", "title"],
        },
    },
}
