#!/usr/bin/env python3

import requests
import json     
import os       
import sys       
from dotenv import load_dotenv  
load_dotenv()  

# SECTION 2: THE CHATBOT CLASS
class OpenRouterChatbot:
    
    def __init__(self, api_key=None, model="openai/gpt-oss-20b:free"):
        print("Initializing chatbot...")
        
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        
        if not self.api_key:
            raise ValueError("No API key found! Set OPENROUTER_API_KEY environment variable.")
        
        self.model = model
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.conversation_history = []
        self.max_tokens = 150
        self.temperature = 0.7
        
        print(f"Chatbot initialized with model: {self.model}")
    
    def add_message(self, role, content):
        """Add a message to our conversation history."""
        message = {"role": role, "content": content}
        self.conversation_history.append(message)
    
    def get_response(self, user_input):
        print(f"Thinking about: '{user_input}'...")
        
        # Step 1: Add the user's message to our conversation history
        self.add_message("user", user_input)
        
        # Step 2: Prepare the HTTP headers (like an envelope's address)
        headers = {
            "Authorization": f"Bearer {self.api_key}",  # API key for access
            "Content-Type": "application/json"          # Tell API we're sending JSON
        }
        
        # Step 3: Prepare the data to send (the actual letter content)
        data = {
            "model": self.model,                        # Which AI model to use                     
            "messages": self.conversation_history,      # Chat history
            "max_tokens": self.max_tokens,              # Limit the response length
            "temperature": self.temperature             # Creativity level
        }
        
        print(f"Sending request to {self.model}...")
        
        try:
            # Send the request to OpenRouter
            response = requests.post(
                self.api_url,           # Where to send it
                headers=headers,        # The envelope info
                data=json.dumps(data)   # The letter content (converted to JSON)
            )
            
            # Check if the request worked
            response.raise_for_status()  # This throws an error if something went wrong
            
            # Parse the response (open the return letter)
            response_data = response.json()
            
            # Extract the AI's actual message
            if 'choices' in response_data and len(response_data['choices']) > 0:
                ai_message = response_data['choices'][0]['message']['content'].strip()
            else:
                return "Error: No response generated"
            
            # Add AI's response to our conversation history
            self.add_message("assistant", ai_message)
            
            return ai_message
            
        except requests.exceptions.RequestException as e:
            return f"Network Error: {str(e)}"
        except json.JSONDecodeError as e:
            return f"JSON Error: {str(e)}"
        except Exception as e:
            return f"Unexpected Error: {str(e)}"

if __name__ == "__main__":
    print("Welcome to the OpenRouter Command Line Chatbot!")
    print("Type 'quit' to exit\n")
    
    try:
        # Create our chatbot
        bot = OpenRouterChatbot()
        
        # Simple chat loop
        while True:
            # Get input from user
            user_input = input("You: ").strip()
            
            # Check if user wants to quit
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
            
            if not user_input:  # Skip empty messages
                continue
                
            # Get AI response and print it
            response = bot.get_response(user_input)
            print(f"Bot: {response}\n")
            
    except ValueError as e:
        print(f"Setup Error: {e}")
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Unexpected Error: {e}")