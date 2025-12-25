import os
from dotenv import load_dotenv
from chatbot import run_chatbot
from sheets_handler import add_expense_to_vacant_row

# Load environment variables
load_dotenv()

# Spreadsheet configuration
SHEET_ID = "1NO-1fymXvJefUZqMN6-stqJtyMCGujwssMBfIkOiTIw"




def main():
    """Main entry point."""
    # Example: Run the chatbot
    run_chatbot()
    pass


if __name__ == "__main__":
    main()
