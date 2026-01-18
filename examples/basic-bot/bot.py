"""
Basic WhatsApp AI Bot Example
==============================

This is a simplified example demonstrating how to build a WhatsApp chatbot
using the whatsapp-bridge and Google's Gemini API.

For production-grade AI with advanced empathy features, contact: w3j.btc@gmail.com

Requirements:
- whatsapp-bridge running on localhost:8080
- Google Gemini API key
- Python 3.9+

Install: pip install google-generativeai requests python-dotenv
"""

import os
import time
import sqlite3
import requests
from datetime import datetime
from typing import Optional, Dict
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BRIDGE_URL = os.getenv("BRIDGE_URL", "http://localhost:8080")
BRIDGE_DB_PATH = os.getenv("BRIDGE_DB_PATH", "../whatsapp-bridge/store/messages.db")
POLLING_INTERVAL = int(os.getenv("POLLING_INTERVAL", "2"))

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


class SimpleWhatsAppBot:
    """
    A simple WhatsApp chatbot that:
    1. Polls the bridge database for new messages
    2. Generates responses using Gemini AI
    3. Sends responses back via the bridge API

    This is a basic example. For production use with advanced empathy,
    multi-agent orchestration, and cost optimization, see the full version.
    """

    def __init__(self):
        self.last_checked = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.processed_messages = set()
        print(f"[Bot] Starting WhatsApp Bot v1.0")
        print(f"[Bot] Bridge: {BRIDGE_URL}")
        print(f"[Bot] Polling interval: {POLLING_INTERVAL}s")

    def get_new_messages(self) -> list:
        """Poll the bridge database for new incoming messages."""
        try:
            conn = sqlite3.connect(BRIDGE_DB_PATH)
            cursor = conn.cursor()

            query = """
                SELECT id, chat_jid, sender, content, timestamp 
                FROM messages 
                WHERE is_from_me = 0 
                AND datetime(substr(timestamp, 1, 19)) > datetime(?)
                ORDER BY timestamp ASC
            """

            cursor.execute(query, (self.last_checked,))
            messages = cursor.fetchall()
            conn.close()

            # Filter out already processed messages
            new_messages = [
                {
                    "id": msg[0],
                    "chat_jid": msg[1],
                    "sender": msg[2],
                    "content": msg[3],
                    "timestamp": msg[4],
                }
                for msg in messages
                if msg[0] not in self.processed_messages
            ]

            return new_messages

        except Exception as e:
            print(f"[Error] Failed to fetch messages: {e}")
            return []

    def generate_response(self, user_message: str) -> str:
        """
        Generate AI response using Gemini.

        Note: This is a basic implementation. The production version includes:
        - Multi-agent TRACE framework (Affective State, Causal Analysis, Strategy, Response)
        - Emotion detection and empathy modeling
        - Context-aware response generation
        - Cost optimization with caching
        - Human-like conversation patterns
        """
        try:
            prompt = f"""You are a helpful customer support assistant. 
Respond to the customer's message in a friendly, professional manner.
Keep responses concise and under 3 sentences.

Customer message: {user_message}

Your response:"""

            response = model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            print(f"[Error] Failed to generate response: {e}")
            return (
                "Sorry, I'm having trouble processing your message. Please try again."
            )

    def send_message(self, chat_jid: str, message: str) -> bool:
        """Send message via the WhatsApp bridge API."""
        try:
            url = f"{BRIDGE_URL}/api/send"
            payload = {"recipient": chat_jid, "message": message}

            response = requests.post(url, json=payload, timeout=10)

            if response.status_code == 200:
                print(f"[Sent] Message to {chat_jid}: {message[:50]}...")
                return True
            else:
                print(f"[Error] Failed to send message: {response.status_code}")
                return False

        except Exception as e:
            print(f"[Error] Failed to send message: {e}")
            return False

    def process_message(self, message: Dict):
        """Process a single incoming message."""
        msg_id = message["id"]
        chat_jid = message["chat_jid"]
        user_message = message["content"]
        timestamp = message["timestamp"]

        print(f"\n[Received] From {chat_jid}")
        print(f"[Message] {user_message}")

        # Generate AI response
        print(f"[AI] Generating response...")
        response = self.generate_response(user_message)

        # Send response
        success = self.send_message(chat_jid, response)

        if success:
            # Mark as processed
            self.processed_messages.add(msg_id)
            # Update last checked timestamp
            self.last_checked = timestamp.split(" +")[0].strip()
            print(f"[Success] Response sent at {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"[Failed] Could not send response")

    def run(self):
        """Main bot loop - continuously poll for new messages."""
        print(f"\n[Bot] Started successfully! Waiting for messages...")
        print(f"[Bot] Press Ctrl+C to stop\n")

        try:
            while True:
                messages = self.get_new_messages()

                if messages:
                    print(f"[Poll] Found {len(messages)} new message(s)")
                    for message in messages:
                        self.process_message(message)

                time.sleep(POLLING_INTERVAL)

        except KeyboardInterrupt:
            print(f"\n[Bot] Shutting down...")
        except Exception as e:
            print(f"\n[Error] Bot crashed: {e}")


def main():
    """Entry point for the basic WhatsApp bot."""

    # Validate configuration
    if not GEMINI_API_KEY:
        print("[Error] GEMINI_API_KEY not found in environment variables")
        print("[Help] Create a .env file with: GEMINI_API_KEY=your_key_here")
        return

    if not os.path.exists(BRIDGE_DB_PATH):
        print(f"[Error] Bridge database not found at: {BRIDGE_DB_PATH}")
        print(
            "[Help] Make sure whatsapp-bridge is running and BRIDGE_DB_PATH is correct"
        )
        return

    # Start the bot
    bot = SimpleWhatsAppBot()
    bot.run()


if __name__ == "__main__":
    main()
