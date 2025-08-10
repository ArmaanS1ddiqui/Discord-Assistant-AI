from discord import Message

async def help_Command(message:Message):
    """
    Sends a detailed help message to the channel where the command was used.
    """
    # Using a triple-quoted string for the multi-line message
    help_text = """
Hello! I'm the Discord AI Assistant. Here are all the commands you can use:

**🤖 AI Commands (Powered by Google Gemini)**
• `$ask <your question>` - Get a quick, concise answer.
• `$explain <your topic>` - Get a more detailed explanation.
• `$summarize <text>` - Provide text to get a summary.
• `$news` - Get a summary of major world events.

**📣 Server & Voice Commands**
• `$announce @User1 @User2 <message>` - Sends a private DM to all tagged users.
• `$speak <message>` - Joins your voice channel to say your message.

**🎲 Fun & Utility**
• `$roll dice` - Rolls a standard six-sided die.
• `$flip a coin` - Flips a coin.
• `$what time is it` - Shows the current time.

**🤫 Private Replies**
• Start any command with a `?` instead of a `$` to have me send the reply sent to your DMs.
  *Example: `?ask What is the weather like?`*
"""
    try:
        await message.channel.send(help_text)
    except Exception as e:
        print(f"Error sending help message: {e}")    