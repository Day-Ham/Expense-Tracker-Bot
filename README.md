# OpenAI Chatbot

A simple command-line chatbot using OpenAI's API.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_api_key_here
GOOGLE_CREDENTIALS_PATH=credentials.json
GOOGLE_SPREADSHEET_ID=your_spreadsheet_id_here
```

You can get your API key from [OpenAI Platform](https://platform.openai.com/api-keys).

3. **Google Sheets Setup** (Optional):
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Sheets API and Google Drive API
   - Create a Service Account and download the JSON credentials file
   - Save the credentials file as `credentials.json` in the project root
   - Share your Google Sheet with the service account email (found in credentials.json)
   - Get your Spreadsheet ID from the Google Sheet URL: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`

## Usage

Run the chatbot:
```bash
python main.py
```

Type your messages and press Enter. Type `quit`, `exit`, or `q` to end the conversation.

## Features

- Interactive command-line interface
- Conversation history maintained during session
- Uses GPT-3.5-turbo model
- Error handling for API issues


