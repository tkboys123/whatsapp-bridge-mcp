# Basic WhatsApp AI Bot

A simple example demonstrating how to build a WhatsApp chatbot using the whatsapp-bridge and Google's Gemini API.

## What This Does

- Polls the WhatsApp bridge database for new messages
- Generates AI responses using Google Gemini
- Sends responses back via the bridge API
- Simple, single-file implementation (~150 lines)

## What This Doesn't Do

This is a **basic example** for learning and experimentation. For production use, you'll need:

- **Multi-agent empathy framework** (emotion detection, causal analysis, strategic planning)
- **Cost optimization** (caching, pattern matching, selective API triggering)
- **Quality assurance** (ML-based response evaluation)
- **Human-like conversation** (tone matching, natural language, typing simulation)
- **Enterprise features** (analytics, multi-tenant support, conversation memory)

**Interested in the full version?** Contact: w3j.btc@gmail.com

## Setup

### 1. Install Dependencies

```bash
pip install google-generativeai requests python-dotenv
```

### 2. Configure Environment

Create a `.env` file:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
BRIDGE_URL=http://localhost:8080
BRIDGE_DB_PATH=../whatsapp-bridge/store/messages.db
POLLING_INTERVAL=2
```

### 3. Start WhatsApp Bridge

Make sure the whatsapp-bridge is running (see parent directory instructions).

### 4. Run the Bot

```bash
python bot.py
```

## How It Works

```
User sends WhatsApp message
         ↓
Bridge saves to SQLite database
         ↓
Bot polls database every 2 seconds
         ↓
Bot sends user message to Gemini API
         ↓
Bot sends AI response via Bridge API
         ↓
User receives response on WhatsApp
```

## Limitations

- **Single-turn conversations** (no memory of previous messages)
- **No emotion detection** (treats all messages the same)
- **No cost optimization** (every message = API call)
- **Generic responses** (no personalization or context)
- **No quality control** (no validation of AI responses)

For production-grade AI with these features, see the enterprise version.

## Example Usage

```
User: "Hi, what are your business hours?"
Bot: "Hello! I'd be happy to help with that. Could you let me know which 
      location you're asking about? Our hours may vary by location."

User: "What services do you offer?"
Bot: "We offer a range of services tailored to your needs. To give you 
      the most relevant information, could you tell me a bit more about 
      what you're looking for?"
```

## Performance

- **Response Time**: 3-5 seconds (API latency)
- **Cost**: $0.0003 per message (Gemini Flash pricing)
- **Throughput**: ~30 messages/minute (polling-based)

**Enterprise version**: 80% cost reduction, <2s response time, unlimited throughput

## License

MIT License - Free for personal and commercial use

## Questions?

- **General questions**: Open an issue on GitHub
- **Enterprise features**: w3j.btc@gmail.com
- **Consulting/Training**: w3j.btc@gmail.com
