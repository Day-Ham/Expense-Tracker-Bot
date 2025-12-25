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
```

You can get your API key from [OpenAI Platform](https://platform.openai.com/api-keys).

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


