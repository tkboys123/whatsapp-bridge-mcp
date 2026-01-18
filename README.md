# WhatsApp Bridge MCP - Open Source WhatsApp Integration

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Go Version](https://img.shields.io/badge/go-1.21+-00ADD8.svg)
![Python Version](https://img.shields.io/badge/python-3.9+-3776AB.svg)

**Turn your personal WhatsApp into an AI-powered customer support channel - for FREE.**

Bypass the expensive WhatsApp Business API ($5,000+ annual commitment) by using your personal WhatsApp account with this lightweight bridge server.

## What Is This?

This project provides:

1. **WhatsApp Bridge Server** (Go) - Connects to WhatsApp Web and exposes a REST API
2. **Basic AI Bot Example** (Python) - Simple chatbot using Google Gemini AI
3. **Complete Documentation** - Get started in under 10 minutes

## Why This Exists

WhatsApp Business API is prohibitively expensive for:
- Small businesses
- Startups
- Individual developers
- Side projects

**Official WhatsApp Business API**: $5,000+/year minimum commitment  
**This Solution**: $0-60/year (hosting costs only)

## Features

### What's Included (Open Source)

- WhatsApp Web integration via Go bridge server
- REST API for sending/receiving messages
- SQLite database for message storage
- Basic AI chatbot example with Google Gemini
- Docker support for easy deployment
- Comprehensive documentation

### What's NOT Included

This is the **foundation** only. For production-grade AI, you'll need:

- **Advanced Empathy Framework** (TRACE)
  - Affective State Identification (emotion detection)
  - Causal Analysis Engine (understand WHY user is upset)
  - Strategic Response Planning (choose optimal approach)
  - Empathetic Response Synthesis (human-like conversations)

- **Cost Optimization** (80% API cost reduction)
  - Smart caching system
  - Pattern matching library
  - Selective API triggering
  - Response template management

- **Quality Assurance**
  - ML-based response evaluation
  - Multi-dimensional scoring
  - Automated mistake detection
  - Continuous improvement tracking

- **Enterprise Features**
  - Multi-tenant support
  - Advanced analytics dashboard
  - Google Sheets integration
  - Team collaboration tools
  - Human handoff workflows

**Want the full version?** Contact: w3j.btc@gmail.com

## Architecture

```
┌─────────────────┐
│  WhatsApp Web   │
└────────┬────────┘
         │ (WebSocket)
         ↓
┌─────────────────┐      ┌──────────────────┐
│  Bridge Server  │◄────►│ SQLite Database  │
│   (Go - 8080)   │      │  (messages.db)   │
└────────┬────────┘      └──────────────────┘
         │ (REST API)
         ↓
┌─────────────────┐      ┌──────────────────┐
│   Your AI Bot   │◄────►│   Gemini API     │
│    (Python)     │      │  (AI Responses)  │
└─────────────────┘      └──────────────────┘
```

## Quick Start

### Prerequisites

- Go 1.21+ (for bridge server)
- Python 3.9+ (for AI bot)
- Google Gemini API key ([Get one free](https://makersuite.google.com/app/apikey))
- WhatsApp account

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/W3JDev/whatsapp-bridge-mcp.git
cd whatsapp-bridge-mcp
```

#### 2. Start the WhatsApp Bridge

```bash
cd bridge
go mod download
go run main.go
```

Scan the QR code with your WhatsApp mobile app to authenticate.

#### 3. Configure the AI Bot

```bash
cd ../examples/basic-bot
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```bash
GEMINI_API_KEY=your_key_here
```

#### 4. Start the Bot

```bash
pip install -r requirements.txt
python bot.py
```

#### 5. Test It!

Send a message to your WhatsApp number from another phone. The bot will respond automatically!

## API Reference

### Send Message

```bash
POST http://localhost:8080/api/send
Content-Type: application/json

{
  "recipient": "1234567890@s.whatsapp.net",
  "message": "Hello from the bridge!"
}
```

### Get Messages

Messages are stored in SQLite database: `bridge/store/messages.db`

```sql
SELECT * FROM messages 
WHERE is_from_me = 0 
ORDER BY timestamp DESC 
LIMIT 10;
```

## Examples

### Basic Bot (Included)

Simple chatbot that responds to every message with AI-generated responses.

**Capabilities**:
- Single-turn conversations
- Generic Gemini responses
- ~3-5 second response time
- $0.0003 per message cost

**Limitations**:
- No conversation memory
- No emotion detection
- No personalization
- No cost optimization

See: `examples/basic-bot/`

### Advanced Bot (Enterprise)

Production-grade AI with TRACE empathy framework.

**Capabilities**:
- Multi-turn contextual conversations
- Emotion detection and empathy modeling
- 80% cost reduction via caching
- <2 second response time
- Human-like conversation patterns
- Quality assurance and mistake detection

**Contact for access**: w3j.btc@gmail.com

## Deployment

### Docker (Recommended)

```bash
docker-compose up -d
```

### Manual Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions on deploying to:
- AWS EC2
- Google Cloud Run
- DigitalOcean
- Heroku
- Railway

## Use Cases

- **Customer Support**: Automate FAQs and common inquiries
- **Lead Generation**: Qualify leads before human handoff
- **Appointment Booking**: Schedule meetings via WhatsApp
- **Order Updates**: Send status updates automatically
- **Community Management**: Moderate and engage with groups

## Performance

### Basic Bot (Open Source)

- Response Time: 3-5 seconds
- Cost per Message: $0.0003
- Throughput: ~30 messages/minute
- Conversation Quality: Basic

### Enterprise Bot (Contact for Access)

- Response Time: <2 seconds
- Cost per Message: $0.00006 (80% reduction)
- Throughput: Unlimited
- Conversation Quality: Human-like with empathy

## Limitations & Disclaimers

### Technical Limitations

- Uses WhatsApp Web (not official API)
- Requires phone to stay connected to internet
- Subject to WhatsApp's terms of service
- May break if WhatsApp updates their protocol

### Legal Considerations

- This is for **personal/business use** with your own WhatsApp account
- Do NOT use for spam or unsolicited messages
- Respect WhatsApp's [Terms of Service](https://www.whatsapp.com/legal/terms-of-service)
- Consider WhatsApp Business API for very high volume (1000+ msg/day)

### Production Readiness

The open source version is a **starting point**, not a complete solution:

- No built-in rate limiting (risk of account ban)
- No error recovery or retry logic
- No conversation context or memory
- No quality control or response validation
- No analytics or monitoring

**For production use**, consider the enterprise version with these features built-in.

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Roadmap

### Open Source (Community)

- [ ] Message media support (images, videos, documents)
- [ ] Group chat support
- [ ] Webhook support for real-time notifications
- [ ] Python SDK for easier integration
- [ ] More AI bot examples (OpenAI, Claude, etc.)

### Enterprise (Commercial)

- [x] TRACE empathy framework
- [x] Cost optimization engine
- [x] ML-based quality assurance
- [x] Google Sheets integration
- [ ] Multi-tenant architecture
- [ ] Advanced analytics dashboard
- [ ] Team collaboration features
- [ ] Human handoff workflows

## FAQ

**Q: Is this legal?**  
A: Yes, as long as you use it with your own WhatsApp account and follow their terms of service. Don't spam.

**Q: Will my account get banned?**  
A: Unlikely if you follow best practices (reasonable volume, no spam, authentic conversations). The enterprise version includes rate limiting and safety features.

**Q: How is this different from WhatsApp Business API?**  
A: This uses WhatsApp Web (personal account). Business API is official but costs $5,000+/year. This is free.

**Q: Can I use this for my business?**  
A: Yes! But consider the enterprise version for production use (includes quality assurance, cost optimization, etc.).

**Q: How do I get the TRACE framework?**  
A: Contact w3j.btc@gmail.com for licensing options.

**Q: Can I see a demo of the enterprise version?**  
A: Yes! Email w3j.btc@gmail.com to schedule a demo.

## Support

- **Bug Reports**: [Open an issue](https://github.com/W3JDev/whatsapp-bridge-mcp/issues)
- **Questions**: [Start a discussion](https://github.com/W3JDev/whatsapp-bridge-mcp/discussions)
- **Enterprise Support**: w3j.btc@gmail.com

## License

MIT License - Free for personal and commercial use.

See [LICENSE](LICENSE) for details.

## Acknowledgments

- [whatsmeow](https://github.com/tulir/whatsmeow) - WhatsApp Web multidevice library
- [Google Gemini](https://ai.google.dev/) - AI model for responses
- The open source community

## Contact

**Author**: W3J Development  
**Email**: w3j.btc@gmail.com  
**GitHub**: [@W3JDev](https://github.com/W3JDev)

---

**Like this project?** Star it on GitHub and share it with others!

**Need the full version?** Contact me for enterprise licensing, consulting, or custom development.
