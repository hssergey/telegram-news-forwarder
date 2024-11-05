from telethon import TelegramClient, events
import asyncio
import settings

# API credentials (you need to create an application on https://my.telegram.org to get these)
api_id = settings.api_id
api_hash = settings.api_hash

# Phone number associated with your Telegram account
phone_number = settings.phone_number

# Replace these with the channel usernames and the target chat username or ID
channels = settings.channels  # Example channel usernames
target_chat = settings.target_chat  # Target chat username or ID

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

# Convert channel usernames to channel IDs
async def get_channel_ids(client, channels):
    channel_ids = []
    for channel in channels:
        chat = await client.get_entity(channel)
        channel_ids.append(chat.id)
        print(f"Resolved channel {channel} to ID {chat.id}")
    return channel_ids

@client.on(events.NewMessage)
async def handler(event):
    message = event.message
    chat = await event.get_chat()
    
    if chat.id in channel_ids:
        await client.forward_messages(target_chat, message)
        # if message.media:
        #     await client.send_file(target_chat, message.media, caption=message.text)
        # else:
        #     await client.send_message(target_chat, message.text)
        print(f"Forwarded message from {chat.username} to {target_chat}")

async def main():
    await client.start(phone=phone_number)
    global channel_ids
    channel_ids = await get_channel_ids(client, channels)
    print("Client Created and Started")

    async with client:
        # Run the client until Ctrl+C is pressed
        await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
