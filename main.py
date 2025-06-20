from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
import os
import re
from keep_alive import keep_alive

# Load API credentials from environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
session_string = os.environ['SESSION_STRING']

# Create the Telegram client
client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Source signal groups/channels
source_channels = [
    'https://t.me/firepipsignals',
    'https://t.me/Forex_Top_Premium_Signals',
    'https://t.me/forexsignals01_trade',
    'https://t.me/forexgdp0',
    'https://t.me/Goldforexsignalfx11',
    'https://t.me/habbyforex',
    'https://t.me/kojoforextrades'
]

# Your private target channel
target_channel = 'https://t.me/+LWjMM6W7LtdjOTM0'

# Legit trading keywords to allow
keywords = ['buy', 'sell', 'tp', 'sl', 'xauusd', 'gold', 'nas100', 'eurusd', 'gbpusd']

# Spam filtering setup
BLOCKED_KEYWORDS = [
    "successful investment payout",
    "successfully paid",
    "congratulations to all our investors",
    "invest & earn"
]

SPAM_LINKS_RE = re.compile(
    r"(tronscan\.org|blockchain\.com|amounts\s*.*?)",
    re.IGNORECASE
)

def is_spam(text):
    text = text.lower()
    if any(bad in text for bad in BLOCKED_KEYWORDS):
        return True
    if SPAM_LINKS_RE.search(text):
        return True
    return False

# Signature added to forwarded messages
signature = "\n\nForwarded by @RealDonwise 🔥 | Donwise Copytrade Vault"

# Main forwarding logic
@client.on(events.NewMessage(chats=source_channels))
async def forward_signal(event):
    text = event.raw_text or ""

    # Check for spam
    if is_spam(text):
        print("🚫 Blocked spam:", text[:80])
        return

    # Check for legit signal keywords
    if any(k in text.lower() for k in keywords):
        if event.message.media:
            await client.send_file(target_channel, event.message.media, caption=(event.message.message or "") + signature)
        else:
            await client.send_message(target_channel, event.message.message + signature)
        print("✅ Signal Forwarded")

# Keep bot alive + start
keep_alive()
client.start()
client.run_until_disconnected()
