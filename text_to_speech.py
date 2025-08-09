import os 
import asyncio
from discord import FFmpegPCMAudio,Message
from gtts import gTTS

# Convert text to speech (TTS) and save as MP3
async def tts_to_mp3(text: str, filename: str) -> None:
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(filename)
    except Exception as e:
        print(f"Error generating TTS: {e}")

async def handle_speak_command(message:Message):
        content_to_say = message.content[len("$speak"):].strip()
        if not content_to_say:
            await message.channel.send('You need to write something after "$Speak"')
            return 

        if not message.guild:
            await message.channel.send("❌ The `$speak` command only works in servers.")
            return

        voice_state = message.author.voice
        if not voice_state or not voice_state.channel:
            await message.channel.send("🔇 Join a voice channel first, then use `$speak …`.")
            return

        # Attempt to connect to voice
        vc = message.guild.voice_client
        try:
            if vc is None or not vc.is_connected():
                vc = await voice_state.channel.connect()
        except Exception as e:
            print(f"Voice connection error: {e}")
            await message.channel.send("❌ Failed to connect to the voice channel.")
            return

        try:
            # Generate and play the MP3 file
            tmp_mp3 = f"/tmp/tts_{message.id}.mp3"
            await tts_to_mp3(content_to_say or "I have nothing to say.", tmp_mp3)
            audio_source = FFmpegPCMAudio(executable="ffmpeg", source=tmp_mp3)
            if not vc.is_playing():
                vc.play(audio_source)
                await message.channel.send("🔈 Speaking now…")
            else:
                await message.channel.send("⏳ Currently busy speaking; try again shortly.")
                return
            
            

            # Wait for the playback to complete
            while vc.is_playing():
                await asyncio.sleep(0.5)

            # Disconnect after playback
            await vc.disconnect()
            os.remove(tmp_mp3)
        except Exception as e:
            print(f"Playback error: {e}")
            await message.channel.send("❌ Error during playback.")
            await vc.disconnect()
        return
