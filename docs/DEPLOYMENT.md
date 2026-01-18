# Deployment Guide

Complete guide for deploying WhatsApp Bridge MCP to production.

## Prerequisites

- Server with 1GB+ RAM
- Linux/Ubuntu recommended (or Windows Server)
- Docker installed (for containerized deployment)
- Domain name (optional, for HTTPS)
- WhatsApp account

## Deployment Options

### Option 1: Docker Compose (Recommended)

Easiest and most reliable deployment method.

#### 1. Clone Repository

```bash
git clone https://github.com/W3JDev/whatsapp-bridge-mcp.git
cd whatsapp-bridge-mcp
```

#### 2. Configure Environment

```bash
cp examples/basic-bot/.env.example examples/basic-bot/.env
nano examples/basic-bot/.env
```

Add your Gemini API key:
```bash
GEMINI_API_KEY=your_key_here
```

#### 3. Start Services

```bash
docker-compose up -d
```

#### 4. Authenticate WhatsApp

```bash
docker logs whatsapp-bridge
```

Scan the QR code with your WhatsApp mobile app.

#### 5. Verify

```bash
# Check bridge logs
docker logs -f whatsapp-bridge

# Check bot logs
docker logs -f whatsapp-bot
```

Send a test message to your WhatsApp number. You should get a response!

### Option 2: Manual Deployment (Linux)

For custom setups or when Docker is not available.

#### 1. Install Dependencies

```bash
# Install Go
wget https://go.dev/dl/go1.21.6.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.21.6.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin

# Install Python
sudo apt update
sudo apt install python3.11 python3-pip
```

#### 2. Clone and Setup

```bash
git clone https://github.com/W3JDev/whatsapp-bridge-mcp.git
cd whatsapp-bridge-mcp
```

#### 3. Start Bridge

```bash
cd bridge
go mod download
nohup go run main.go > bridge.log 2>&1 &
```

#### 4. Configure Bot

```bash
cd ../examples/basic-bot
cp .env.example .env
nano .env
```

Add your Gemini API key.

#### 5. Start Bot

```bash
pip3 install -r requirements.txt
nohup python3 bot.py > bot.log 2>&1 &
```

#### 6. Authenticate WhatsApp

```bash
cat ../bridge/bridge.log
```

Scan the QR code.

### Option 3: systemd Services (Production)

For reliable production deployment with auto-restart.

#### 1. Create Bridge Service

```bash
sudo nano /etc/systemd/system/whatsapp-bridge.service
```

```ini
[Unit]
Description=WhatsApp Bridge Server
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/whatsapp-bridge-mcp/bridge
ExecStart=/usr/local/go/bin/go run main.go
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 2. Create Bot Service

```bash
sudo nano /etc/systemd/system/whatsapp-bot.service
```

```ini
[Unit]
Description=WhatsApp AI Bot
After=network.target whatsapp-bridge.service
Requires=whatsapp-bridge.service

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/whatsapp-bridge-mcp/examples/basic-bot
ExecStart=/usr/bin/python3 bot.py
Restart=always
RestartSec=10
Environment="GEMINI_API_KEY=your_key_here"

[Install]
WantedBy=multi-user.target
```

#### 3. Enable and Start

```bash
sudo systemctl daemon-reload
sudo systemctl enable whatsapp-bridge
sudo systemctl enable whatsapp-bot
sudo systemctl start whatsapp-bridge
sudo systemctl start whatsapp-bot
```

#### 4. Check Status

```bash
sudo systemctl status whatsapp-bridge
sudo systemctl status whatsapp-bot
```

## Cloud Platform Deployment

### AWS EC2

#### 1. Launch Instance

- AMI: Ubuntu 22.04 LTS
- Instance Type: t3.small (2GB RAM)
- Security Group: Open port 8080 (if exposing API)

#### 2. Connect and Install

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
sudo apt update && sudo apt upgrade -y
```

Follow "Manual Deployment (Linux)" steps above.

#### 3. Keep Alive

Use systemd services or screen/tmux:

```bash
screen -S bridge
cd bridge && go run main.go
# Ctrl+A, D to detach

screen -S bot
cd examples/basic-bot && python3 bot.py
# Ctrl+A, D to detach
```

### DigitalOcean Droplet

#### 1. Create Droplet

- Image: Ubuntu 22.04 LTS
- Size: Basic ($12/month - 2GB RAM)
- Region: Closest to you

#### 2. Deploy

Same as AWS EC2 instructions.

### Google Cloud Run (Experimental)

**Note**: Cloud Run is serverless and may disconnect WhatsApp Web. Use with caution.

```bash
# Build and push
gcloud builds submit --tag gcr.io/YOUR_PROJECT/whatsapp-bridge
gcloud run deploy whatsapp-bridge --image gcr.io/YOUR_PROJECT/whatsapp-bridge
```

**Limitation**: WhatsApp session may disconnect frequently due to cold starts.

### Railway.app (Easiest)

#### 1. Fork Repository

Fork the GitHub repository to your account.

#### 2. Deploy to Railway

- Go to [railway.app](https://railway.app)
- Create new project from GitHub repo
- Add environment variable: `GEMINI_API_KEY`
- Deploy!

Railway automatically detects Dockerfile and builds.

### Heroku

**Note**: Heroku free tier ended. Requires paid dyno.

```bash
heroku login
heroku create your-app-name
heroku stack:set container
git push heroku main
heroku logs --tail
```

## Production Best Practices

### 1. Process Management

Use systemd, pm2, or supervisord to auto-restart on crashes:

```bash
# With pm2 (for Node.js-style process management)
npm install -g pm2
pm2 start "go run main.go" --name bridge
pm2 start "python3 bot.py" --name bot
pm2 save
pm2 startup
```

### 2. Monitoring

Monitor service health:

```bash
# Check if bridge is running
curl http://localhost:8080/health

# Watch logs in real-time
tail -f bridge/bridge.log
tail -f examples/basic-bot/bot.log
```

### 3. Backup

Backup WhatsApp session and database:

```bash
# Backup script
#!/bin/bash
tar -czf backup-$(date +%Y%m%d).tar.gz \
  bridge/store/messages.db \
  bridge/*.session

# Add to crontab for daily backups
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

### 4. Security

**Critical**:
- Never expose bridge port 8080 to internet
- Use firewall to restrict access
- Keep API key in environment variables
- Regularly update dependencies

```bash
# UFW firewall (Ubuntu)
sudo ufw enable
sudo ufw allow ssh
sudo ufw deny 8080  # Don't expose bridge
```

### 5. Rate Limiting

WhatsApp may ban accounts sending too many messages. Implement:

```python
# Add to bot.py
import time
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_per_minute=20):
        self.max_per_minute = max_per_minute
        self.messages = []
    
    def can_send(self):
        now = datetime.now()
        # Remove messages older than 1 minute
        self.messages = [t for t in self.messages if now - t < timedelta(minutes=1)]
        
        if len(self.messages) < self.max_per_minute:
            self.messages.append(now)
            return True
        return False
```

## Troubleshooting

### Bridge Won't Start

```bash
# Check if port 8080 is in use
sudo lsof -i :8080

# Kill process using port
sudo kill -9 <PID>
```

### Bot Not Responding

```bash
# Check bot logs
tail -f examples/basic-bot/bot.log

# Verify database exists
ls -l bridge/store/messages.db

# Check Gemini API key
echo $GEMINI_API_KEY
```

### WhatsApp Disconnected

```bash
# Restart bridge
sudo systemctl restart whatsapp-bridge

# Check logs for QR code
sudo journalctl -u whatsapp-bridge -f
```

### Database Locked

```bash
# Check if multiple processes are accessing database
ps aux | grep bot.py

# Kill duplicate processes
pkill -f bot.py
```

## Scaling Considerations

### Current Limitations

- Single-threaded (one message at a time)
- Polling-based (2-second minimum delay)
- No load balancing
- No horizontal scaling

### For High Volume

Consider the enterprise version with:
- Event-driven architecture
- Redis caching
- Multiple worker processes
- Load balancing support
- Advanced rate limiting

Contact w3j.btc@gmail.com for enterprise features.

## Cost Estimates

### Self-Hosted (Cloud VPS)

| Provider | Specs | Cost/Month |
|----------|-------|------------|
| DigitalOcean | 2GB RAM | $12 |
| AWS Lightsail | 2GB RAM | $10 |
| Linode | 2GB RAM | $10 |
| Railway | 2GB RAM | $5-20 |

### API Costs

| Volume | Gemini API Cost |
|--------|-----------------|
| 1,000 messages/month | $0.30 |
| 10,000 messages/month | $3.00 |
| 100,000 messages/month | $30.00 |

**Total**: ~$15-45/month for most small businesses

Compare to WhatsApp Business API: $5,000+/year minimum

## Support

- **Issues**: [GitHub Issues](https://github.com/W3JDev/whatsapp-bridge-mcp/issues)
- **Questions**: [GitHub Discussions](https://github.com/W3JDev/whatsapp-bridge-mcp/discussions)
- **Enterprise**: w3j.btc@gmail.com
