from telethon import TelegramClient, events from telethon.sessions import StringSession import os from keep_alive import keep_alive from datetime import datetime, timedelta import asyncio import json import requests import random import pytz

Nigeria timezone

nigeria_tz = pytz.timezone('Africa/Lagos')

Hardcoded credentials (Use with caution if public)

api_id = 24361556 api_hash = 'acdfe825ab951d9e10b1ac93632e0fdc' session_string = '1BJWap1wBu1Qn2Io7Yvo_v5ryaKXGr0qZ6bpIM9kyBZSgJy11CKo54fhq1IjhtWJQJOw_GXtaqIfYOS8R771do8RYbCO40_ap7LY3PmqqDRrjPdfzg_5vSBx9w-24KygqKRdpBPJKUnrkwM8VI5ai9muYILetpjE0o-YVPKJEMqy30tcQOut2ratfei6VAsvzu9R0tSduVHBzliMlm1QYbNaIOTtZZ9IZ_OvirrwsGssWEg6UnYTlaY6ZofsuUXucETz2guleXwDMVDzbifocoUHf4LTRnjRkjteKMmnQxG0PXhxe2c4fhRRFjg6feWBf0pODFgHJzCTynufEseKq_i2VWNBRO-g='

client = TelegramClient(StringSession(session_string), api_id, api_hash)

Channels

source_channels = [ 'firepipsignals', 'Forex_Top_Premium_Signals', 'forexsignals01_trade', 'forexgdp0', 'Goldforexsignalfx11', 'habbyforex', 'kojoforextrades' ] target_channel = '@DonwiseVault'

Signal keywords and tracking

keywords = ['buy', 'sell', 'tp', 'sl', 'xauusd', 'gold', 'nas100', 'eurusd', 'gbpusd'] signature = "\n\nBy @RealDonwise\nDonwise Copytrade Vault" forwarded_today = set() daily_count = 0 last_reset_date = datetime.now(nigeria_tz).date() morning_posted = False signal_log = []

Motivation setup

motivational_quotes = [ "Start your day with clarity and conviction. The pips you seek are on the other side of fear. Take the shot. 🧠📊", "Every pip is a step closer to freedom. Trade smart, stay disciplined, and keep building your edge. 💪📉", "The market doesn’t care about excuses—only execution. Stick to the plan and grow your account. 🚀📈", "Let your strategy speak louder than your emotions today. Risk little. Win big. 👊🔥", "There’s no growth in the comfort zone. Make smart moves today. Don’t chase—calculate. 📉📈", "No one became great by guessing. Analyze. Execute. Elevate. Today’s another shot. 🎯📈", "The charts don’t lie. Your discipline defines your destiny. Let’s get to work. 📈🔐" ] motivational_images = [ 'https://i.ibb.co/g7Zwqft/motivation1.jpg', 'https://i.ibb.co/LNRXJjJ/motivation2.jpg', 'https://i.ibb.co/0ncsCK5/motivation3.jpg', 'https://i.ibb.co/QJQPDKT/motivation4.jpg', 'https://i.ibb.co/MfGmMLy/motivation5.jpg' ]

async def morning_intro(): global morning_posted if not morning_posted: quote = random.choice(motivational_quotes) image = random.choice(motivational_images) await client.send_file(target_channel, image, caption=f"🌄 Good morning traders!\n\n{quote}\n\n— Donwise") await asyncio.sleep(3) await client.send_message(target_channel, "📢 Are you ready for today's signal of the day? Stay sharp. First one drops soon! 🚀") morning_posted = True

async def get_price(symbol): symbol_map = { 'xauusd': 'XAUUSD=X', 'nas100': '^NDX', 'eurusd': 'EURUSD=X', 'gbpusd': 'GBPUSD=X' } yf_symbol = symbol_map.get(symbol.lower()) if not yf_symbol: return None try: r = requests.get(f'https://query1.finance.yahoo.com/v7/finance/quote?symbols={yf_symbol}') data = r.json() return float(data['quoteResponse']['result'][0]['regularMarketPrice']) except: return None

async def end_of_day_summary(): wins = losses = pending = 0 for entry in signal_log: current_price = await get_price(entry['pair']) if current_price is None: pending += 1 continue if entry['action'] == 'buy': if current_price >= entry['tp']: wins += 1 elif current_price <= entry['sl']: losses += 1 else: pending += 1 elif entry['action'] == 'sell': if current_price <= entry['tp']: wins += 1 elif current_price >= entry['sl']: losses += 1 else: pending += 1

total = wins + losses + pending
if total == 0:
    return await client.send_message(target_channel, "📊 No valid signals to summarize today.")
win_rate = round((wins / (wins + losses)) * 100, 1) if (wins + losses) > 0 else 0
summary = f"📊 Signal Summary:\n- Total Signals: {total}\n- Wins: {wins} ✅\n- Losses: {losses} ❌\n- Pending: {pending} ⏳\n\n🔥 Win Rate: {win_rate}%"
await client.send_message(target_channel, summary)

@client.on(events.NewMessage(chats=source_channels)) async def forward_signal(event): global daily_count, last_reset_date, morning_posted now = datetime.now(nigeria_tz).date()

if now != last_reset_date:
    daily_count = 0
    forwarded_today.clear()
    morning_posted = False
    last_reset_date = now
    signal_log.clear()

if not morning_posted:
    await morning_intro()

msg_id = (event.chat_id, event.message.id)
if msg_id in forwarded_today or daily_count >= 7:
    return

text = event.raw_text.lower()
if any(skip in text for skip in ['performance', 'celebrate', 'see you on monday', 'motivational post', 'crypto', 'btc', 'bitcoin']):
    return

if not any(k in text for k in keywords):
    return

action = 'buy' if 'buy' in text else 'sell' if 'sell' in text else None
pair = next((k for k in ['xauusd', 'nas100', 'eurusd', 'gbpusd'] if k in text), None)
tp = sl = None
for line in text.splitlines():
    if 'tp' in line:
        tp = ''.join([c for c in line if c.isdigit() or c == '.'])
    if 'sl' in line:
        sl = ''.join([c for c in line if c.isdigit() or c == '.'])

if pair and action and tp and sl:
    try:
        signal_log.append({ 'pair': pair, 'action': action, 'tp': float(tp), 'sl': float(sl) })
    except:
        pass

if event.message.media:
    await client.send_file(target_channel, event.message.media, caption=(event.message.message or '') + signature)
else:
    await client.send_message(target_channel, event.message.message + signature)

forwarded_today.add(msg_id)
daily_count += 1
print(f"✅ Signal Forwarded | {daily_count}/7 for {now}")

def schedule_end_of_day(): async def job(): while True: now = datetime.now(nigeria_tz) if now.hour == 21 and now.minute == 0: await end_of_day_summary() await asyncio.sleep(60) await asyncio.sleep(30) client.loop.create_task(job())

keep_alive() schedule_end_of_day() client.start() client.run_until_disconnected()

