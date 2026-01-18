# Architecture Overview

## System Components

The WhatsApp Bridge MCP consists of three main components:

### 1. WhatsApp Bridge (Go Server)

**Purpose**: Connects to WhatsApp Web and exposes a REST API

**Key Features**:
- Authenticates via QR code (WhatsApp Web protocol)
- Maintains persistent WebSocket connection
- Stores messages in SQLite database
- Provides REST API for sending messages
- Auto-reconnects on connection loss

**Technology**: Go 1.21+, whatsmeow library, SQLite

**Endpoints**:
- `POST /api/send` - Send message to WhatsApp
- `GET /health` - Health check endpoint

### 2. Message Database (SQLite)

**Purpose**: Stores all incoming and outgoing messages

**Schema**:
```sql
CREATE TABLE messages (
    id TEXT PRIMARY KEY,
    chat_jid TEXT NOT NULL,        -- WhatsApp JID (e.g., 1234567890@s.whatsapp.net)
    sender TEXT NOT NULL,           -- Sender's phone number
    content TEXT NOT NULL,          -- Message text
    timestamp DATETIME NOT NULL,    -- When message was sent/received
    is_from_me BOOLEAN NOT NULL     -- 0 = incoming, 1 = outgoing
);
```

**Location**: `bridge/store/messages.db`

### 3. AI Bot (Python)

**Purpose**: Polls for new messages and generates AI responses

**Flow**:
1. Poll database every N seconds for new messages
2. Filter out already processed messages
3. Send user message to Gemini API
4. Receive AI-generated response
5. Send response via Bridge API
6. Mark message as processed

**Technology**: Python 3.9+, Google Gemini, SQLite

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     WhatsApp Web                             │
│                 (User's Phone Stays Connected)               │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ WebSocket Connection
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                   WhatsApp Bridge (Go)                       │
│                                                              │
│  ┌──────────────┐    ┌─────────────┐    ┌──────────────┐  │
│  │   Receiver   │───→│  Database   │←───│   Sender     │  │
│  │   Handler    │    │   Writer    │    │   Handler    │  │
│  └──────────────┘    └─────────────┘    └──────────────┘  │
│                             │                    ↑          │
└─────────────────────────────┼────────────────────┼──────────┘
                              │                    │
                              ↓                    │
                    ┌──────────────────┐           │
                    │  SQLite Database │           │
                    │   messages.db    │           │
                    └──────────────────┘           │
                              ↓                    │
                    ┌──────────────────┐           │
                    │   AI Bot (Poll)  │           │
                    │                  │           │
                    │  1. Read new msg │           │
                    │  2. Call Gemini  │           │
                    │  3. Send via API │───────────┘
                    └──────────────────┘
                              ↓
                    ┌──────────────────┐
                    │   Gemini API     │
                    │  (AI Response)   │
                    └──────────────────┘
```

## Message Processing Sequence

### Incoming Message

```
1. User sends WhatsApp message
   ↓
2. Bridge receives via WebSocket
   ↓
3. Bridge saves to database (is_from_me=0)
   ↓
4. Bot polls database (every 2 seconds)
   ↓
5. Bot finds new message (timestamp > last_checked)
   ↓
6. Bot sends to Gemini API
   ↓
7. Gemini generates response
   ↓
8. Bot sends response via Bridge API
   ↓
9. Bridge sends to WhatsApp Web
   ↓
10. User receives response
```

### Outgoing Message

```
1. Bot calls POST /api/send
   ↓
2. Bridge validates recipient JID
   ↓
3. Bridge sends via WhatsApp Web
   ↓
4. Bridge saves to database (is_from_me=1)
   ↓
5. WhatsApp delivers message
```

## Scalability Considerations

### Current Architecture (Open Source)

**Strengths**:
- Simple to understand and deploy
- No external dependencies (except Gemini API)
- Low resource usage (< 100MB RAM)
- Works on any platform (Windows, Linux, Mac)

**Limitations**:
- Polling-based (2-second delay minimum)
- Single-threaded processing
- No built-in rate limiting
- No horizontal scaling support
- Requires phone to stay online

### Enterprise Architecture (Contact for Access)

**Enhancements**:
- Event-driven architecture (webhook support)
- Multi-threaded conversation processing
- Built-in rate limiting and safety controls
- Redis caching for cost optimization
- Horizontal scaling support (multiple bots)
- Failover and auto-recovery
- Advanced analytics and monitoring

## Security Considerations

### What's Protected

- All API communications are HTTP (localhost only)
- WhatsApp session stored locally
- Database file access controlled by OS permissions

### What's NOT Protected (Yet)

- No API authentication (anyone on localhost can send)
- No message encryption at rest
- No input validation/sanitization
- No rate limiting (risk of account ban)

**For production use**, implement:
- API key authentication
- Database encryption
- Input validation and sanitization
- Rate limiting and abuse prevention
- Monitoring and alerting

## Technology Stack

### Bridge Server

- **Language**: Go 1.21+
- **WhatsApp Library**: [whatsmeow](https://github.com/tulir/whatsmeow)
- **Database**: SQLite
- **HTTP Server**: net/http (standard library)

### AI Bot (Basic)

- **Language**: Python 3.9+
- **AI Model**: Google Gemini Flash
- **HTTP Client**: requests
- **Database**: sqlite3 (standard library)

### AI Bot (Enterprise)

- **Language**: Python 3.11+
- **AI Framework**: Custom TRACE multi-agent system
- **Caching**: Redis
- **Analytics**: Google Sheets API
- **Monitoring**: Custom ML Judge system

## Deployment Options

### Development

```bash
# Terminal 1: Start bridge
cd bridge && go run main.go

# Terminal 2: Start bot
cd examples/basic-bot && python bot.py
```

### Production (Docker)

```bash
docker-compose up -d
```

### Cloud Deployment

See deployment guides for:
- AWS EC2
- Google Cloud Run
- DigitalOcean
- Railway
- Heroku

## Performance Metrics

### Basic Bot (Open Source)

| Metric | Value |
|--------|-------|
| Response Time | 3-5 seconds |
| Throughput | ~30 messages/minute |
| Memory Usage | ~50MB (bridge) + ~100MB (bot) |
| API Cost | $0.0003/message |
| Concurrent Users | ~10-20 |

### Enterprise Bot

| Metric | Value |
|--------|-------|
| Response Time | <2 seconds |
| Throughput | Unlimited |
| Memory Usage | ~200MB (with caching) |
| API Cost | $0.00006/message (80% reduction) |
| Concurrent Users | 1000+ |

## Future Enhancements

### Planned (Open Source)

- Media message support (images, videos, documents)
- Group chat support
- Webhook integration for real-time events
- Python SDK for easier bot development
- Rate limiting and safety controls

### Available Now (Enterprise)

- TRACE empathy framework
- Cost optimization engine
- ML-based quality assurance
- Google Sheets integration
- Multi-tenant support
- Advanced analytics dashboard

Contact w3j.btc@gmail.com for enterprise features.
