
from telethon import TelegramClient, events
import os
from keep_alive import keep_alive

api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
session_name = 'donwise_session'

source_channels = [
    'https://t.me/firepipsignals',
    'https://t.me/Forex_Top_Premium_Signals',
    'https://t.me/forexsignals01_trade',
    'https://t.me/forexgdp0',
    'https://t.me/Goldforexsignalfx11',
    'https://t.me/habbyforex',
    'https://t.me/kojoforextrades'
]

target_channel = 'https://t.me/+LWjMM6W7LtdjOTM0'

keywords = ['buy', 'sell', 'tp', 'sl', 'xauusd', 'gold', 'nas100', 'eurusd', 'gbpusd']
signature = "\n\nForwarded by @RealDonwise 🔥 | Donwise Copytrade Vault"

acdfe825ab951d9e10b1ac93632e0fdc
1BJWap1wBu1Qn2Io7Yvo_v5ryaKXGr0qZ6bpIM9kyBZSgJy11CKo54fhq1IjhtWJQJOw_GXtaqIfYOS8R771do8RYbCO40_ap7LY3PmqqDRrjPdfzg_5vSBx9w-24KygqKRdpBPJKUnrkwM8VI5ai9muYILetpjE0o-YVPKJEMqy30tcQOut2ratfei6VAsvzu9R0tSduVHBzliMlm1QYbNaIOTtZZ9IZ_OvirrwsGssWEg6UnYTlaY6ZofsuUXucETz2guleXwDMVDzbifocoUHf4LTRnjRkjteKMmnQxG0PXhxe2c4fhRRFjg6feWBf0pODFgHJzCTynufEseKq_i2VWNBRO-g=
@client.on(events.NewMessage(chats=source_channels))
async def forward_signal(event):
    text = event.raw_text.lower()
    if any(k in text for k in keywords):
        if event.message.media:
            await client.send_file(target_channel, event.message.media, caption=(event.message.message or "") + signature)
        else:
            await client.send_message(target_channel, event.message.message + signature)
        print("✅ Signal Forwarded")

keep_alive()
client.start()
client.run_until_disconnected()
