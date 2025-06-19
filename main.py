from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
import os
from keep_alive import keep_alive

# Load API credentials from environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
session_string = os.environ['SESSION_STRING']

# Create the Telegram client using StringSession
client = TelegramClient(StringSession(session_string), api_id, api_hash)

# List of signal source groups or channels
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

# Keywords to filter signal messages
keywords = ['buy', 'sell', 'tp', 'sl', 'xauusd', 'gold', 'nas100', 'eurusd', 'gbpusd']

# Signature to be added to each forwarded message
signature = "\n\nForwarded by @RealDonwise 🔥 | Donwise Copytrade Vault"

# Auto-forwarding logic
@client.on(events.NewMessage(chats=source_channels))
async def forward_signal(event):
    text = event.raw_text.lower()
    if any(k in text for k in keywords):
        if event.message.media:
            await client.send_file(target_channel, event.message.media, caption=(event.message.message or "") + signature)
        else:
            await client.send_message(target_channel, event.message.message + signature)
        print("✅ Signal Forwarded")

# Keep the web app alive + start the bot
keep_alive()
client.start()
client.run_until_disconnected()
