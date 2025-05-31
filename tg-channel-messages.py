import asyncio
from telethon.sync import TelegramClient

# --- Configuration ---
# Replace with your actual API ID and API Hash from my.telegram.org

# Replace with the public channel's username (e.g., 'telegram')
# You can also use the full link 'https://t.me/telegram' or the channel's numerical ID.
CHANNEL_USERNAME = 'audio_angrybuddhist' # e.g., 'durov' or 'telegram'

# Number of recent messages to retrieve
LIMIT = 10

# --- Main Logic ---
async def get_recent_channel_messages():
    # 'session_name' is used to store your session data (e.g., login info)
    # This prevents you from logging in every time you run the script.
    client = TelegramClient('my_session', API_ID, API_HASH)

    print("Connecting to Telegram...")
    await client.start()
    print("Connected!")

    try:
        # Get the channel entity
        # This will convert the username to a channel object
        channel_entity = await client.get_entity(CHANNEL_USERNAME)
        print(f"Retrieving messages from channel: {channel_entity.title}")

        messages = []
        async for message in client.iter_messages(channel_entity, limit=LIMIT):
            messages.append(message)
            # You can process the message here directly if you don't need to store all
            # print(f"Message ID: {message.id}")
            # print(f"Date: {message.date}")
            # print(f"Sender: {message.sender.username if message.sender else 'Unknown'}")
            # print(f"Text: {message.text[:100]}..." if message.text else "No text")
            # print("-" * 30)

        if messages:
            print(f"\nSuccessfully retrieved {len(messages)} recent messages from '{CHANNEL_USERNAME}':\n")
            for msg in reversed(messages): # Display in chronological order (oldest first if you want)
                print(f"--- Message ID: {msg.id} ---")
                print(f"Date: {msg.date}")
                if msg.sender:
                    print(f"Sender: {msg.sender.username or msg.sender.first_name}")
                else:
                    print("Sender: Channel (Anonymous)")
                print(f"Text: {msg.text if msg.text else '[No text content]'}")
                if msg.views:
                    print(f"Views: {msg.views}")
                #  Download media if available
                # if msg.media and hasattr(msg.media, 'document') and msg.media.document:
                #     if msg.media.document.mime_type == 'audio/mpeg':
                #         file_name = msg.media.document.attributes[1].file_name if len(msg.media.document.attributes) > 1 else 'audio.mp3'
                #         print(f"Audio File: {file_name}")
                #         await client.download_media(msg.media, file_name)
                print("-" * 40)
        else:
            print(f"No messages found in '{CHANNEL_USERNAME}' or channel is empty.")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Possible reasons:")
        print("1. The channel username might be incorrect.")
        print("2. You might not have access to the channel (e.g., it's private or restricted).")
        print("3. Your API_ID/API_HASH are incorrect or session is invalid.")
    finally:
        print("Disconnecting from Telegram...")
        await client.disconnect()
        print("Disconnected.")

if __name__ == '__main__':
    asyncio.run(get_recent_channel_messages())