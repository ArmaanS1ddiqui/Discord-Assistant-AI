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
    

    if user_message.startswith("$announce"):
        # 1. Check for mentions
        if not message.mentions:
            await message.channel.send("❌ You need to tag at least one person to announce to! \n> Usage: `$announce @User1 @User2 Your message here`")
            return

        # 2. Isolate the announcement message text
        content = message.content
        text_to_announce = content[len("$announce"):].strip()
        for user in message.mentions:
            text_to_announce = text_to_announce.replace(user.mention, "").strip()

        if not text_to_announce:
            await message.channel.send("❌ You need to include a message to announce!")
            return

        # 3. Loop through mentioned users and send DMs
        success_count = 0
        fail_count = 0
        for user in message.mentions:
            try:
                await user.send(f"📣 **Announcement from {message.author.display_name} in '{message.guild.name}':**\n>>> {text_to_announce}")
                success_count += 1
            except Exception as e:
                fail_count += 1
                print(f"Failed to send DM to {user.name}. Reason: {e}")
        
        # 4. Send a confirmation back to the channel
        confirmation_message = f"✅ Announcement sent to **{success_count}** member(s)."
        if fail_count > 0:
            confirmation_message += f"\n> (Failed to send to **{fail_count}** member(s), they may have DMs disabled.)"
        
        await message.channel.send(confirmation_message)
        return

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
    clean_command = user_message
    if user_message.startswith(("?","$")):
        clean_command = user_message[1:].strip()
    try:
        response = get_response(clean_command)
        if response:
            target = message.author if is_private else message.channel
            await target.send(response)
    except Exception as e:
        print(f"Error in get_response: {e}")

# Handle bot startup
@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running!")

# Handle incoming messages / Bouncer that send the code to the function
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    if message.content.startswith(("$","?")) or not message.guild:
        print(f"[{message.channel}] {message.author} : '{message.content}'")    
        await send_message(message, message.content.strip()) #this makes it more user friendly like " $Hi" to "$hi"

# Run the bot
if __name__ == '__main__':
    client.run(TOKEN)
