from typing import Final
import os, asyncio
from dotenv import load_dotenv
from discord import Intents, Client, Message, FFmpegPCMAudio
from responses import get_response
from ask_ai import ask_gemini
from ask_ai import handle_ai_messages
from text_to_speech import handle_speak_command
# Load Discord Bot Token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot setup with required intents
intents: Intents = Intents.default()
intents.message_content = True
intents.dm_messages = True
intents.voice_states = True
client: Client = Client(intents=intents)

AI_Commands = ("$ask","$explain","$news","$summarize")

# Send message with support for TTS and announcements
async def send_message(message: Message, user_message: str) -> None:
    if not user_message.strip():
        print('(Message was empty, likely due to missing intents)')
        return

    # Private message detection
    is_private = user_message.startswith('?')
    if is_private:
        user_message = user_message[1:].strip()

    #Gemini Ask Functionality
    if user_message.startswith(AI_Commands):
        thinking_message = await message.channel.send("🤔 Thinking...")
        response = await handle_ai_messages(user_message)
        await thinking_message.edit(content=response)
        return 

    
    # TTS functionality
    if user_message.startswith("$speak"):
        await handle_speak_command(message)
        return 
    # Fallback for regular messages
    try:
        response = get_response(user_message)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(f"Response error: {e}")

# Handle bot startup
@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running!")

# Handle incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    print(f"[{message.channel}] {message.author} : '{message.content}'")    
    await send_message(message, message.content.strip())

# Run the bot
if __name__ == '__main__':
    client.run(TOKEN)
