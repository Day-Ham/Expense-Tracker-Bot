import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from chatbot import run_chatbot
from datetime import date
# Load environment variables
load_dotenv()

# Google Sheets configuration
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]

# Initialize Google Sheets client
creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)
gs_client = gspread.authorize(creds)

# Open the spreadsheet
sheet_id = "1NO-1fymXvJefUZqMN6-stqJtyMCGujwssMBfIkOiTIw"
finance_sheet = gs_client.open_by_key(sheet_id)

# Get current month and year
current_month = date.today().strftime('%B')  # Full month name (e.g., "January")
current_year = date.today().year  # Year as integer (e.g., 2024)

# Get all worksheets
all_worksheets = finance_sheet.worksheets()

doesSheetExist = False
# Loop through all sheets and check if title matches month and year
for worksheet in all_worksheets:
    sheet_title = worksheet.title
    # Check if title matches current month and year
    # (You can customize the matching logic here)
    if current_month in sheet_title and str(current_year) in sheet_title:
        print(f"Found matching sheet: {sheet_title}")
        doesSheetExist = True
        # Do something with the matching sheet
    else:
        print(f"Sheet '{sheet_title}' does not match {current_month} {current_year}")
if  doesSheetExist == False:
    print(f"Sheet does not exist for {current_month} {current_year}")
    # Create a new sheet with the current month and year
    new_sheet = finance_sheet.add_worksheet(title=f"{current_month} {current_year}", rows="100", cols="26")
    print(f"Created new sheet: {new_sheet.title}")
    
    # Add headers to the first row
    headers = ["Date", "Name", "Type", "Category", "Note", "Amount"]
    new_sheet.update("A1:F1", [headers])
    print("Added headers to the new sheet")



def main():
    """Main entry point."""
    # Example: Run the chatbot
    #run_chatbot()


if __name__ == "__main__":
    main()
