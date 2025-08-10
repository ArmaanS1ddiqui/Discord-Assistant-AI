from discord import Message

async def handle_announce_command(message:Message):
    """
    Handles the entire logic for the $announce command.
    Parses mentions, sends DMs, and posts a confirmation.
    """

    if not message.mentions:
        await message.channel.send("❌ You need to tag at least one person to announce to! \n> Usage: `$announce @User1 @User2 Your message here`")
        return 
    
    content = message.content
    text_to_announce = content[len("$announce"):].strip()
    for user in message.mentions:
        text_to_announce = text_to_announce.replace(user.mention, "").strip() #stripping away any access

    if not text_to_announce:
        await message.channel.send("❌ You need to include a message to announce!")
        return 
    
    success_count = 0
    fail_count = 0

    for user in message.mentions:
        try:
            await user.send(f"📣 **Announcement from {message.author.display_name} in '{message.guild.name}':**\n>>> {text_to_announce}")
            success_count += 1
        except Exception as e:
            fail_count += 1
            print(f"Failed to send DM to {user.name}. Reason: {e}")

    confirmation_message = f"✅ Announcement sent to **{success_count}** member(s)."
    if fail_count > 0:
        confirmation_message += f"\n> (Failed to send to **{fail_count}** member(s), they may have DMs disabled.)"

    await message.channel.send(confirmation_message)