import os

from dotenv import load_dotenv
from langchain import hub
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

# Updated imports using the new langchain_community modules
from langchain_community.llms import OpenAI
from langchain_community.utilities import SQLDatabase

# Load environment variables from the .env file
load_dotenv()

# Ensure that the 'db' folder exists and create an absolute path for the database file
base_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(base_dir, "db")
os.makedirs(db_dir, exist_ok=True)  # Create 'db' folder if it doesn't exist
db_file = os.path.join(db_dir, "example.db")

# Construct the SQLite URI using the absolute path
db_uri = "sqlite:///" + db_file

# Retrieve the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the SQL database connection using the updated URI
db = SQLDatabase.from_uri(db_uri)

# Initialize the LLM with the provided API key and desired parameters
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)


# Pull prompt (or define your own)
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message = prompt_template.format(dialect="SQLite", top_k=5)


print(system_message)

# Create the SQL Database Toolkit by providing both the database and the LLM
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Create a SQL agent with verbose logging enabled
agent = create_sql_agent(
    llm=llm, toolkit=toolkit, state_modifier=system_message, verbose=True
)


if __name__ == "__main__":
    # Interactive mode only when running this file directly.

    # Optionally display the full LLM prompt
    show_full_prompt = (
        input("Do you want to see the full LLM prompt? (yes/no): ").strip().lower()
        == "yes"
    )

    # Get the natural language query from the user
    user_query = input("Enter your SQL natural language query: ")

    # Execute the agent to process the query and get the result
    result = agent.run(user_query)

    # Display the result
    print("\n=== Query Result ===")
    print(result)

    if show_full_prompt:
        print("\n=== Full LLM Prompt (if available) ===")
        # For example: print(agent.prompt_history)
