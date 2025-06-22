from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os
from keep_alive import keep_alive
from datetime import datetime
import asyncio
import requests
import random
import pytz

# Nigeria timezone
nigeria_tz = pytz.timezone('Africa/Lagos')

# Load credentials from environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
session_string = os.environ['SESSION_STRING']

client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Source and target channels
source_channels = [
    'firepipsignals',
    'Forex_Top_Premium_Signals',
    'forexsignals01_trade',
    'forexgdp0',
    'Goldforexsignalfx11',
    'habbyforex',
    'kojoforextrades',
    'HONG-SOCIETY'
]
target_channel = '@DonwiseVault'

# Keywords and blocked content
keywords = ['buy', 'sell', 'tp', 'sl', 'xauusd', 'gold', 'nas100', 'eurusd', 'gbpusd']
signature = "\n\nBy @RealDonwise\nDonwise Copytrade Vault"

blocked_phrases = [
    'weekly performance result',
    'see you on monday',
    'celebrate',
    'instagram.com',
    'go check and comment to win',
    'By @RealDonwise 🔥 | Donwise Copytrade Vault',
    'tp1', 'tp2', 'running', 'easy hit', 'smassshedd',
    'closed another', 'set breakeven', 'tp 1', 'tp 2', 'tp3'
]

motivational_quotes = [
    "Start your day with clarity and conviction. The pips you seek are on the other side of fear. Take the shot. 🧠📈",
    "Every pip is a step closer to freedom. Trade smart, stay disciplined, and keep building your edge. 💪💹",
    "The market doesn’t care about excuses—only execution. Stick to the plan and grow your account. 🚀📈",
    "Let your strategy speak louder than your emotions today. Risk little. Win big. 👊🔥",
    "There’s no growth in the comfort zone. Make smart moves today. Don’t chase—calculate. 📉📈",
    "No one became great by guessing. Analyze. Execute. Elevate. Today’s another shot. 🎯📈",
    "The charts don’t lie. Your discipline defines your destiny. Let’s get to work. 📈🔐"
]

motivational_images = [
    'https://i.ibb.co/g7Zwqft/motivation1.jpg',
    'https://i.ibb.co/LNRXJjJ/motivation2.jpg',
    'https://i.ibb.co/0ncsCK5/motivation3.jpg',
    'https://i.ibb.co/QJQPDKT/motivation4.jpg',
    'https://i.ibb.co/MfGmMLy/motivation5.jpg'
]

forwarded_today = set()
daily_count = 0
last_reset_date = datetime.now(nigeria_tz).date()
morning_posted = False

# ========== GOOD MORNING POST ==========
async def morning_intro():
    global morning_posted
    if not morning_posted:
        quote = random.choice(motivational_quotes)
        image = random.choice(motivational_images)
        await client.send_file(target_channel, image, caption=f"🌄 Good morning traders!\n\n{quote}\n\n— Donwise")
        await asyncio.sleep(2)
        await client.send_message(target_channel, "📢 Are you ready for today's signal of the day? Stay sharp. First one drops soon! 🚀")
        morning_posted = True

# ========== SIGNAL FILTER AND FORWARDING ==========
@client.on(events.NewMessage(chats=source_channels))
async def forward_signal(event):
    global daily_count, last_reset_date, morning_posted
    now = datetime.now(nigeria_tz).date()

    # Reset daily
    if now != last_reset_date:
        daily_count = 0
        forwarded_today.clear()
        morning_posted = False
        last_reset_date = now

    if not morning_posted:
        await morning_intro()

    msg_id = (event.chat_id, event.message.id)
    if msg_id in forwarded_today or daily_count >= 7:
        return

    text = event.raw_text.lower()

    # Skip blocked messages or those with media
    if any(bad in text for bad in blocked_phrases):
        return
    if event.message.media:
        return

    if any(k in text for k in keywords):
        await client.send_message(target_channel, event.message.message + signature)
        forwarded_today.add(msg_id)
        daily_count += 1
        print(f"✅ Signal Forwarded | {daily_count}/7 for {now}")

# ========== WEEKLY SUMMARY POST ==========
async def post_weekly_summary():
    message = f"\n\n📊 Weekly Summary Report\nDate: {datetime.now(nigeria_tz).strftime('%A %d %B %Y')}\n\nTotal Signals: 34\nTotal Wins: 27\nTotal Losses: 5\nPending: 2\nWin Rate: 84.3%\n\nStay focused for next week. Consistency builds equity."
    await client.send_message(target_channel, message)

# ========== WEEKLY SCHEDULER ==========
def schedule_weekly_summary():
    async def job():
        while True:
            now = datetime.now(nigeria_tz)
            if now.weekday() == 5 and now.hour == 9 and now.minute == 0:  # Saturday 9 AM
                await post_weekly_summary()
                await asyncio.sleep(60)
            await asyncio.sleep(30)
    client.loop.create_task(job())

# ========== DEPLOY ==========
keep_alive()
schedule_weekly_summary()
client.start()
client.run_until_disconnected()
