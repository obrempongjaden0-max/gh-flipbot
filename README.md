import requests
import time
import json

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}/"
    
    def get_updates(self, offset=None):
        """Get new messages from Telegram"""
        url = self.base_url + "getUpdates"
        params = {"timeout": 100, "offset": offset}
        try:
            response = requests.get(url, params=params)
            return response.json()
        except Exception as e:
            print(f"Error getting updates: {e}")
            return {"result": []}
    
    def send_message(self, chat_id, text):
        """Send message back to user"""
        url = self.base_url + "sendMessage"
        params = {"chat_id": chat_id, "text": text}
        try:
            response = requests.post(url, params=params)
            return response.json()
        except Exception as e:
            print(f"Error sending message: {e}")
            return None
    
    def process_message(self, message):
        """Process incoming message and prepare response"""
        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()
        user_name = message["from"].get("first_name", "User")
        
        print(f"Received message from {user_name}: {text}")
        
        # Handle different types of messages
        if text.startswith('/'):
            return self.handle_commands(chat_id, text, user_name)
        else:
            return self.handle_text(chat_id, text, user_name)
    
    def handle_commands(self, chat_id, text, user_name):
        """Handle command messages"""
        if text == '/start':
            return f"Hello {user_name}! 👋 I'm your Telegram bot. Send me a message or use /help to see what I can do!"
        
        elif text == '/help':
            return """🤖 Available Commands:
/start - Start the bot
/help - Show this help message
/time - Get current time
/echo [text] - Repeat your text
/about - About this bot"""
        
        elif text == '/time':
            from datetime import datetime
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return f"🕐 Current time: {current_time}"
        
        elif text == '/about':
            return "This is a simple Telegram bot created with Python! 🐍"
        
        elif text.startswith('/echo '):
            echo_text = text[6:]  # Remove '/echo ' from the beginning
            if echo_text:
                return f"🔊 You said: {echo_text}"
            else:
                return "Please provide text to echo. Example: /echo Hello World"
        
        else:
            return "❓ Unknown command. Type /help to see available commands."
    
    def handle_text(self, chat_id, text, user_name):
        """Handle regular text messages"""
        if not text:
            return "I received your message, but it appears to be empty! 🤔"
        
        text_lower = text.lower()
        
        # Simple responses based on message content
        if any(word in text_lower for word in ['hello', 'hi', 'hey']):
            return f"Hello {user_name}! 😊 How can I help you today?"
        
        elif any(word in text_lower for word in ['how are you', 'how are u']):
            return "I'm just a bot, but I'm functioning perfectly! Thanks for asking! 🤖"
        
        elif any(word in text_lower for word in ['thank', 'thanks']):
            return "You're welcome! 😊"
        
        elif any(word in text_lower for word in ['bye', 'goodbye']):
            return f"Goodbye {user_name}! 👋 Feel free to message me anytime!"
        
        else:
            # Echo with some engagement
            responses = [
                f"Interesting! You said: '{text}'",
                f"Got it: '{text}' 👍",
                f"'{text}' - noted! 📝",
                f"I see you wrote: '{text}'",
                f"Message received: '{text}' 📨"
            ]
            import random
            return random.choice(responses)
    
    def run(self):
        """Main bot loop"""
        last_update_id = None
        print("🤖 Bot started! Send a message to your bot in Telegram...")
        print("Press Ctrl+C to stop the bot")
        
        try:
            while True:
                # Get new messages
                updates = self.get_updates(last_update_id)
                
                if "result" in updates:
                    for update in updates["result"]:
                        last_update_id = update["update_id"] + 1
                        
                        # Check if it's a text message
                        if "message" in update and "text" in update["message"]:
                            response_text = self.process_message(update["message"])
                            
                            if response_text:
                                # Send response back to user
                                self.send_message(
                                    update["message"]["chat"]["id"], 
                                    response_text
                                )
                                print(f"Sent response: {response_text[:50]}...")
                
                # Wait before checking for new messages again
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user")

# ===== USAGE =====
if __name__ == "__main__":
    # Replace with your actual bot token from @BotFather
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
    
    # Create and run the bot
    bot = TelegramBot(BOT_TOKEN)
    bot.run()
