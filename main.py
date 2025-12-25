import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_bot(user_message: str) -> str:
    """
    Send a message to the OpenAI chatbot and get a response.
    
    Args:
        user_message: The user's message/query
        
    Returns:
        The assistant's response
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main function to run the chatbot."""
    print("OpenAI Chatbot - Type 'quit' or 'exit' to end the conversation\n")
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        return
    
    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant."}
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
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation_history
            )
            
            assistant_message = response.choices[0].message.content
            print(f"Assistant: {assistant_message}\n")
            
            # Add assistant response to history
            conversation_history.append({"role": "assistant", "content": assistant_message})
            
        except Exception as e:
            print(f"Error: {str(e)}\n")

if __name__ == "__main__":
    main()
