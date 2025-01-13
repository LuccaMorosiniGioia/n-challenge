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

```secrets.toml
OPENAI_API_KEY="your-openai-api-key"
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

## Design Choices

- **LLM:** OpenAI api was chosen for the familiarity i had with its API and tool calling format.
- **Chat Service:** The current model calling format of `model_class.process_message()` can be easily ported to a API service serving multiple users. All we need as input is the question asked and some identifier for the user in order to load previous messages from the database. For sake of testing and easily using the streamlit interface everything is being done synchronously. 
- **Tools:** Although the main chat_service does not use a loot of tools, its current structure is ready to receive more with an ease of implementation. All we have to do is create the tool json definition and a method/class to process its call and add a call to it whenever that tool is called by the model. 
- **SQL Service:** An sql specific agent was created to create SQL queries to maximize its probability of generating the correct one. We could have everything inside the same model `chat_service+sql_service+plot_service` (all the prompts together), but passing to the open AI API just the knowledge and instruction to query the specific table we needed made it so much more powerful.
- **Plot Service:** The same logic goes to the chart creating model. We feed to it only the information needed to come up with the best plot to fit the data and user question. 
- **Database:** In order to have more users interacting with the application all that would be needed is an extra column on the conversation history identifying the user. With this coming along side the questions asked from the frontend each user would have it's own chat history. 
- **AWS:** It was chosen for the ease of creating a new database on RDS to host our data. Mostly everything could be used inside the free-tier plans. AWS only charged small amounts (cents of dolar) for the public VPC in order to connect to the database from outside of AWS services. 
- **Streamlit Interface:** Not a lot of work was put into the frontend of the applicantion. I used as starting point an example chatbot interface provided by streamlit that worked well to focus more on developing the LLMs prompts and "backend" processing. The backend itself holds the information of the conversation history, but if the front is reloaded it will not reload it. 



