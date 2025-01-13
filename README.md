# Data Analytics Chatbot with LLMs

This project provides a natural language interface to retrieve database information. It allows users to interact with the database by asking questions in plain language. 
The chatbot is capable of creating complex SQL Queries and Plots to represent the extracted data. It will choose the best plot to fit the data if it thinks a plot is needed (It may not create a plot to represent basic data).

![chat1](https://i.ibb.co/pQD82qt/chat-1.jpg)  
![chat2](https://i.ibb.co/zS6Z7n4/chat-2.jpg)


## Tools and Frameworks

- **LLM**: ChatGPT-4o (OpenAI API)
- **Frontend**: Streamlit 
- **Database**: PostgreSQL + SQLAlchemy & psycopg2
- **Cloud**: AWS RDS
- **Data Manipulation and Visualization**: Pandas + Matplotlib

## Prerequisites

Before getting started, ensure you have the following installed on your machine:

- [Python v3.12.0](https://www.python.org/downloads/release/python-3120/) and [virtualenv](https://pypi.org/project/virtualenv/).

## Setup and Run

Follow these steps to setup and run the project:

### 1. Create and activate the virtual environment

```bash
# Navigate to the project directory
cd app

# Create and activate the virtual environment
python -m venv venv
source venv/bin/activate # Linux
.\venv\Scripts\activate # Windows
```

### 2. Install the required dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Set up your `secrets.toml` in `app/.streamlit/secrets.toml` file with the required credentials and other environment variables:

```.env
OPENAI_API_KEY='your-openai-api-key'
...
```

### 4. Run the application

Once the environment is set up, you can run the application with:

```
streamlit run app.py
```

## 🗂️ Project Structure

### App
    
- **app.py**: Main file to run the chat interface.
- **requirements.txt**: Dependencies required for the project.
- **src/**: Core logic for the chatbot and tool processing.
  - **services/**: 
    - **chat_service.py**: Main LLM interface. Definition of the chatbot the user interact with.
    - **sql_service.py**: LLM agent responsible for receiving users question and creating the correct SQL query to retrive database information.
    - **plot_service.py**: LLM agent responsible for choosing one or more plots to represent the data given the user question and the query output. Capable of choosing and creating the following plots: 
      - Bar Char
      - Horizontal Bar Chart
      - Scatter Plot
      - Pie Chart
    - **tool_processor.py**: chat_service tool processor Class. Responsible for integrating the user desire to query the database with the sql and plot service returning the data the chat_service needs to create an output and plots to represent the data.
    - **database_service**: Class responsible for interfacing all database related tools.
- **tools/**: Tools definitions used by the services.
- **config/settings.py**: .env & LLM-Prompts interface.

### Database

- **db_script.py**: Python script to extract .csv file and upload it to PostgreSQL database hosted on RDS.

### Design Choices



