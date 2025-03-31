from typing import List
import argparse
from pokebot.rag import RAGApp, AssistantRole
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing")


def _read_urls_from_file(filepath):
    # If a seed file is provided, parse and load the URLs into an array.
    seed_list = []
    if filepath:
        with open(filepath, 'r') as file:
            seed_list = [line.strip() for line in file.readlines()]
    return seed_list


ASSISTANTS = {
    "healthcare": AssistantRole("Your Healthcare AI Assistant", 
                                _read_urls_from_file("data/med/articles/healthcare.txt"),
                                "diabetes"),
    "diabetes": AssistantRole("Your Diabetes AI Assistant", 
                                _read_urls_from_file("data/med/articles/diabetes.txt"),
                                "diabetes"),
    "default": AssistantRole("Your Diabetes Lite AI Assistant", 
                                ["https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes"],
                                "diabetes"),
}


def _start_vuln_rag(args):
    # Use the seed file if provided; otherwise, use the selected assistant type.
    if args.seed:
        seed_urls = _read_urls_from_file(args.seed)
        assistant = AssistantRole("Your Diabetes AI Assistant", seed_urls, "diabetes")
    else:
        assistant = ASSISTANTS.get(args.assistant_type, ASSISTANTS["default"])
    # Initialize and run the RAGApp
    app = RAGApp(assistant=assistant)
    app.run()


def main():
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(description='RAG App with command-line options.')
    
    # Creating subparsers.
    subparsers = parser.add_subparsers(title='command', dest='command', description='Choose a command to start the app.')
    
    # Subparser for the rag command.
    rag_parser = subparsers.add_parser('rag', help='Manage the RAG app')
    rag_subparser = rag_parser.add_subparsers(title='subcommand', dest='subcommand', description='Choose a sub command to start the app.')
    
    # Subparser for starting the app.
    rag_start_parser = rag_subparser.add_parser("start", help="Start the rag app")
    rag_start_parser.add_argument('--assistant-type', type=str, 
                                  choices=["healthcare"], 
                                  default="default",
                                  help='Assistant Type')
    rag_start_parser.add_argument('--seed', type=str, default=None, help='Path to seed file with URLs')

    args = parser.parse_args()

    if args.command == 'rag' and args.subcommand == 'start':
        _start_vuln_rag(args)
    else:
        print("Please specify a valid subcommand.")


if __name__ == "__main__":
    main()







