#!/bin/bash
set -e
echo "🚀 Starting N4 VIP Bot One-Click Setup..."

# Update system
apt update && apt upgrade -y
apt install -y python3 python3-venv python3-pip git

# Clone repo
if [ ! -d "/root/n4_vip.bot" ]; then
    git clone https://github.com/rururat/n4_vip.bot /root/n4_vip.bot
fi
cd /root/n4_vip.bot

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate venv and install dependencies
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# Create .env interactively
echo "⚡ Configure Bot Token and Admin IDs"
read -p "Enter your Bot Token: " BOT_TOKEN
read -p "Enter Admin IDs (comma separated): " ADMIN_IDS

cat > .env <<EOL
BOT_TOKEN=$BOT_TOKEN
ADMIN_IDS=$ADMIN_IDS
EOL

# systemd service
cat > /etc/systemd/system/n4vipbot.service <<EOL
[Unit]
Description=N4 VIP Telegram Bot
After=network.target

[Service]
User=root
WorkingDirectory=/root/n4_vip.bot
EnvironmentFile=/root/n4_vip.bot/.env
ExecStart=/root/n4_vip.bot/venv/bin/python /root/n4_vip.bot/bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd and start bot
systemctl daemon-reload
systemctl enable n4vipbot.service
systemctl restart n4vipbot.service

echo "✅ N4 VIP Bot setup completed!"
echo "Check status: sudo systemctl status n4vipbot"
echo "View logs: sudo journalctl -u n4vipbot -f"