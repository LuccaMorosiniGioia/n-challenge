import streamlit as st
from src.services.chat_service import ChatService

openai_service = ChatService()

st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "df":
        st.chat_message(msg["role"]).markdown(msg["content"])
    else:
        plot_name, plot = msg["content"]
        st.write(plot_name)
        st.pyplot(plot)

if prompt := st.chat_input():
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    reas_response, fin_resp, arr_plots = openai_service.process_message(prompt)

    if fin_resp is None:
        st.session_state.messages.append(
            {"role": "assistant", "content": reas_response}
        )
        st.chat_message("assistant").markdown(reas_response)
    else:
        text = f"""{reas_response}\n{fin_resp}"""
        st.session_state.messages.append({"role": "assistant", "content": text})
        st.chat_message("assistant").markdown(text)

    if len(arr_plots):
        for plots in arr_plots:
            for plot_name, plot in plots:
                st.session_state.messages.append(
                    {"role": "plot", "content": (plot_name, plot)}
                )
                st.write(plot_name)
                st.pyplot(plot)
