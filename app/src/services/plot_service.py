import openai
from openai import OpenAI
from typing import Dict
import json


from ..tools.create_scatter_chart_tool import create_scatter_chart_tool
from ..tools.create_bar_chart_tool import create_bar_chart_tool
from ..tools.create_horizontal_bar_chart_tool import create_horizontal_bar_chart_tool
from ..tools.create_pie_chart_tool import create_pie_chart_tool
from ..config.settings import Settings
import matplotlib.pyplot as plt
from ast import literal_eval
from dotenv import load_dotenv

load_dotenv()


class PlotService:
    def __init__(self):
        self.settings = Settings()
        openai.api_key = self.settings.OPENAI_API_KEY
        self.model = self.settings.OPENAI_MODEL
        self.temperature = 0
        self.client = OpenAI(api_key=self.settings.OPENAI_API_KEY)
        self.messages = self.settings.BASE_PLOT_MESSAGES
        self.tools = [
            create_bar_chart_tool,
            create_scatter_chart_tool,
            create_horizontal_bar_chart_tool,
            create_pie_chart_tool,
        ]

    def __append_to_msgs__(self, message: str, role: str) -> None:
        msg_dict = {"role": role, "content": message}
        self.messages.append(msg_dict)

    def process_message(self, message: str) -> str:
        self.__append_to_msgs__(message, "user")
        try:
            response = self.__send_completion_msg__()

            return self.__process_tools__(response.choices[0].message)

        except Exception as e:
            print(f"Error processing message on plot service: {e}")
            raise RuntimeError(f"{e}")

    def __eval_arr__(self, arr) -> list:
        if not isinstance(arr, list):
            # Ensure that null is a string
            arr = arr.replace("null", '"null"').replace('""', '"')

            if "[" in arr and "]" in arr:
                try:
                    return literal_eval(arr)
                except Exception as e:
                    print(f"Error evaluating array: {e}")
                    raise RuntimeError(f"{e}")
            else:
                try:
                    arr = arr.split(",")
                except Exception as e:
                    print(f"Error evaluating array: {e}")
                    raise RuntimeError(f"{e}")
        try:
            arr = [float(x) for x in arr]  # Try to convert to float
        except Exception as e:
            print(f"Error converting to float: {e}")

        return arr

    def __process_h_bar_chart__(self, tool_args: Dict[str, str]) -> plt.figure:
        x = self.__eval_arr__(tool_args.get("x-axis"))
        y = self.__eval_arr__(tool_args.get("y-axis"))
        title = tool_args.get("title")
        xlabel = tool_args.get("x-label")
        ylabel = tool_args.get("y-label")

        fig, ax = plt.subplots()

        plt.xticks(rotation=45)
        ax.barh(x, y, align="center")
        ax.invert_yaxis()
        ax.set_xlabel(ylabel)
        ax.set_ylabel(xlabel)
        ax.set_title(title)

        return fig

    def __process_bar_chart__(self, tool_args: Dict[str, str]) -> plt.figure:
        x = self.__eval_arr__(tool_args.get("x-axis"))
        y = self.__eval_arr__(tool_args.get("y-axis"))
        title = tool_args.get("title")
        xlabel = tool_args.get("x-label")
        ylabel = tool_args.get("y-label")

        fig, ax = plt.subplots()
        ax.bar(x, y)

        plt.xticks(rotation=45)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)

        return fig

    def __process_scatter_plot__(self, tool_args: Dict[str, str]) -> plt.figure:
        classes = self.__eval_arr__(tool_args.get("classes"))
        x = self.__eval_arr__(tool_args.get("x-axis"))
        y = self.__eval_arr__(tool_args.get("y-axis"))
        title = tool_args.get("title")
        xlabel = tool_args.get("x-label")
        ylabel = tool_args.get("y-label")

        fig, ax = plt.subplots()

        if isinstance(classes, str):
            ax.scatter(x[0], y[0], label=classes, alpha=0.8, edgecolors="none")
            ax.set_xticks(x[0])
            ax.set_xticklabels(x[0], rotation=45)
        else:
            for index, clss in enumerate(classes):
                ax.scatter(x[index], y[index], label=clss, alpha=0.8, edgecolors="none")
                ax.set_xticks(x[index])
                ax.set_xticklabels(x[index], rotation=45)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend()
        ax.grid(True)

        return fig

    def __process_pie_chart__(self, tool_args: Dict[str, str]) -> plt.figure:
        labels = self.__eval_arr__(tool_args.get("labels"))
        sizes = self.__eval_arr__(tool_args.get("sizes"))
        title = tool_args.get("title")

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct="%1.1f%%")
        ax.set_title(title)

        return fig

    def __process_tools__(self, response_message: Dict[str, str]) -> str:
        tool_calls = getattr(response_message, "tool_calls", None)
        if not tool_calls:
            print("No tool calls. Response: ", response_message)
            return []

        processor_map = {
            "create_bar_chart": ("Bar Chart", self.__process_bar_chart__),
            "create_scatter_chart": ("Scatter Plot", self.__process_scatter_plot__),
            "create_horizontal_bar_chart_tool": (
                "Horizontal Bar Chart",
                self.__process_h_bar_chart__,
            ),
            "create_pie_chart_tool": ("Pie Chart", self.__process_pie_chart__),
        }

        plots = []
        for tool_call in tool_calls:
            tool_function_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            print("tool name:", tool_function_name)
            print(tool_args)

            plot_name, processor = processor_map.get(tool_function_name)
            if processor is None:
                raise ValueError(f"Error: tool {tool_function_name} does not exist")

            plots.append((plot_name, processor(tool_args)))

        return plots

    def __append_to_msgs__(self, message: str, role: str) -> None:
        msg_dict = {"role": role, "content": message}
        self.messages.append(msg_dict)

    def __send_completion_msg__(self):
        ret = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools,
            tool_choice="auto",
            temperature=self.temperature,
        )

        return ret
