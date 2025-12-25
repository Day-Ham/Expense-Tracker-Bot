import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import date
from dotenv import load_dotenv

load_dotenv()

# Google Sheets configuration
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]

# Headers for expense tracking
EXPENSE_HEADERS = ["Date", "Name", "Type", "Category", "Note", "Amount"]


def get_google_sheets_client(credentials_path="credentials.json"):
    """
    Initialize and return Google Sheets client.
    
    Args:
        credentials_path: Path to the credentials JSON file
        
    Returns:
        gspread.Client object
    """
    creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    return gspread.authorize(creds)


def get_or_create_monthly_sheet(spreadsheet_id, month=None, year=None):
    """
    Get or create a worksheet for the specified month and year.
    
    Args:
        spreadsheet_id: The ID of the Google Spreadsheet
        month: Month name (e.g., "December"). If None, uses current month
        year: Year as integer (e.g., 2024). If None, uses current year
        
    Returns:
        Worksheet object
    """
    if month is None:
        month = date.today().strftime('%B')
    if year is None:
        year = date.today().year
    
    gs_client = get_google_sheets_client()
    finance_sheet = gs_client.open_by_key(spreadsheet_id)
    
    # Get all worksheets
    all_worksheets = finance_sheet.worksheets()
    
    # Check if sheet exists
    for worksheet in all_worksheets:
        sheet_title = worksheet.title
        if month in sheet_title and str(year) in sheet_title:
            print(f"Found matching sheet: {sheet_title}")
            return worksheet
    
    # Sheet doesn't exist, create it
    print(f"Sheet does not exist for {month} {year}")
    new_sheet = finance_sheet.add_worksheet(
        title=f"{month} {year}",
        rows="100",
        cols="26"
    )
    print(f"Created new sheet: {new_sheet.title}")
    
    # Add headers to the first row
    new_sheet.update([EXPENSE_HEADERS], "A1:F1")
    print("Added headers to the new sheet")
    
    return new_sheet


def find_vacant_row(worksheet, start_row=2, end_row=100):
    """
    Find the first vacant row in a worksheet.
    
    Args:
        worksheet: The worksheet to check
        start_row: Starting row number (default: 2, to skip headers)
        end_row: Ending row number (default: 100)
        
    Returns:
        Row number if vacant row found, None otherwise
    """
    print(f"\nChecking vacant rows in '{worksheet.title}'...")
    
    for row_num in range(start_row, end_row + 1):
        try:
            row_data = worksheet.row_values(row_num)
            print(f"Row {row_num}: {row_data}")
            
            # Check if row is vacant (all cells are empty or None)
            if not row_data or not any(cell.strip() if cell else False for cell in row_data):
                print(f"Row {row_num} is vacant")
                return row_num
        except Exception as e:
            # If row doesn't exist or error occurs, treat as vacant
            print(f"Row {row_num} appears vacant (error or empty)")
            return row_num
    
    print("No vacant rows found")
    return None


def update_row(worksheet, row_num, data):
    """
    Update a specific row in the worksheet.
    
    Args:
        worksheet: The worksheet to update
        row_num: Row number to update
        data: List of values to write (should match number of columns)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        range_string = f"A{row_num}:F{row_num}"
        worksheet.update([data], range_string)
        print(f"Updated row {row_num} with data: {data}")
        return True
    except Exception as e:
        print(f"Error updating row {row_num}: {str(e)}")
        return False


def add_expense(worksheet, date_str, name, expense_type, category, note, amount):
    """
    Add an expense entry to the worksheet.
    
    Args:
        worksheet: The worksheet to add the expense to
        date_str: Date string (e.g., "2024-12-19")
        name: Name/description of the expense
        expense_type: Type of expense
        category: Category of expense
        note: Additional notes
        amount: Amount as string (e.g., "100.00")
        
    Returns:
        True if successful, False otherwise
    """
    vacant_row = find_vacant_row(worksheet)
    if vacant_row:
        data = [date_str, name, expense_type, category, note, amount]
        return update_row(worksheet, vacant_row, data)
    else:
        print("No vacant rows available to add expense")
        return False


def add_expense_to_vacant_row(spreadsheet_id, date_str, name, expense_type, category, note, amount, month=None, year=None):
    """
    Convenient function to add an expense to a vacant row.
    Handles getting/creating the worksheet and finding/updating a vacant row.
    
    Args:
        spreadsheet_id: The ID of the Google Spreadsheet
        date_str: Date string (e.g., "2024-12-19")
        name: Name/description of the expense
        expense_type: Type of expense
        category: Category of expense
        note: Additional notes
        amount: Amount as string (e.g., "100.00")
        month: Month name (optional, defaults to current month)
        year: Year as integer (optional, defaults to current year)
        
    Returns:
        True if successful, False otherwise
    """
    # Get or create the worksheet
    worksheet = get_or_create_monthly_sheet(spreadsheet_id, month, year)
    
    # Find vacant row and add expense
    return add_expense(worksheet, date_str, name, expense_type, category, note, amount)

