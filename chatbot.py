import os
import json
import ast
from openai import OpenAI
from dotenv import load_dotenv
from sheets_handler import add_expense_to_vacant_row

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SHEET_ID = "1NO-1fymXvJefUZqMN6-stqJtyMCGujwssMBfIkOiTIw"

def chat_with_bot(user_message: str) -> str:
    """
    Send a message to the OpenAI chatbot and get a response.
    
    Args:
        user_message: The user's message/query
        
    Returns:
        The assistant's response
    """
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Whenever the user gives a financial transaction, respond ONLY in this JSON array format: "
        "[\"Date\", \"Name\", \"Type\", \"Category\", \"Note\", \"Amount\"]. "
        "Date must be YYYY-MM-DD, Type is either 'Income' or 'Expense', Amount is a number, "
        "and other fields as described. DO NOT add any extra text."},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def run_chatbot():
    """Main function to run the chatbot interactively."""
    print("OpenAI Chatbot - Type 'quit' or 'exit' to end the conversation\n")
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        return
    
    conversation_history = [
        {"role": "system", "content": (
            "You are a helpful assistant that helps the user track their finances. "
            "Whenever the user gives a financial transaction, respond ONLY in this JSON array format: "
            "[\"Date\", \"Name\", \"Type\", \"Category\", \"Note\", \"Amount\"]. "
            "Date must be YYYY-MM-DD, Type is either 'Income' or 'Expense', Amount is a number, "
            "and other fields as described. DO NOT add any extra text. "
            "If no mention of the date, use the current date. "
            "If no mention of the type, use 'Expense'. "
            "If no mention of the category, use 'Uncategorized'. "
            "If no mention of the note, use 'No note'. "
            "If no mention of the amount, use '0'."
            "Category are only one of the following: 'Food', 'Transportation', 'Housing', 'Utilities', 'Entertainment', 'Other'."
        )}
    ]
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # Get response from OpenAI
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation_history
            )
            
            assistant_message = response.choices[0].message.content
            print(f"Assistant: {assistant_message} Transaction has been recorded! \n")
            
            # Parse the string response into a list
            try:
                # Try to parse as Python literal (handles both strings and numbers)
                expense_data = ast.literal_eval(assistant_message.strip())
                add_expense_to_vacant_row(SHEET_ID, expense_data)
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing expense data: {str(e)}")
                print(f"Received: {assistant_message}")
            
            # Add assistant response to history
            conversation_history.append({"role": "assistant", "content": assistant_message})
            
        except Exception as e:
            print(f"Error: {str(e)}\n")

