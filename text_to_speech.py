# text_to_speech.py

import os
import asyncio
import tempfile # 1. Import the tempfile module
from discord import FFmpegPCMAudio, Message
from gtts import gTTS

async def _tts_to_mp3(text: str, filename: str) -> bool:
    """Converts text to speech and saves it as an MP3 file."""
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(filename)
        return True
    except Exception as e:
        print(f"❌ Error generating TTS audio: {e}")
        return False

async def handle_speak_command(message: Message):
    """Handles the entire process for the $speak command."""
    content_to_say = message.content[len("$speak"):].strip()
    if not content_to_say:
        await message.channel.send('You need to write something after "$speak".')
        return

    if not message.guild:
        await message.channel.send("❌ The `$speak` command only works in servers.")
        return

    voice_state = message.author.voice
    if not voice_state or not voice_state.channel:
        await message.channel.send("🔇 Join a voice channel first, then use `$speak`.")
        return

    vc = message.guild.voice_client
    try:
        if vc is None or not vc.is_connected():
            vc = await voice_state.channel.connect()
        elif vc.channel != voice_state.channel:
            await vc.move_to(voice_state.channel)
    except Exception as e:
        print(f"❌ Voice connection error: {e}")
        await message.channel.send("❌ Failed to connect to the voice channel.")
        return

    if vc.is_playing():
        await message.channel.send("⏳ I'm already speaking. Please wait a moment.")
        return

    # 2. Use tempfile to create a safe, cross-platform file path
    temp_dir = tempfile.gettempdir()
    tmp_mp3 = os.path.join(temp_dir, f"tts_{message.id}.mp3")
    
    if not await _tts_to_mp3(content_to_say, tmp_mp3):
        await message.channel.send("❌ Sorry, I couldn't generate the audio for that message.")
        return

    try:
        audio_source = FFmpegPCMAudio(executable="ffmpeg", source=tmp_mp3)
        vc.play(audio_source)
        await message.channel.send("🔈 Speaking now…")

        while vc.is_playing():
            await asyncio.sleep(0.5)

    except Exception as e:
        print(f"❌ Playback error: {e}")
        await message.channel.send("❌ An error occurred during playback.")
    finally:
        # 3. Clean up resources safely
        if vc and vc.is_connected():
            await vc.disconnect()
        if os.path.exists(tmp_mp3):
            os.remove(tmp_mp3)