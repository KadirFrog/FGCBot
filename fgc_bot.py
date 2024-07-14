import discord
from discord.ext import commands
from private_data import *


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

alphabet_emojis = [
    '🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯',
    '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹',
    '🇺', '🇻', '🇼', '🇽', '🇾', '🇿'
]

@bot.event
async def on_ready():
    print(await bot.tree.sync(guild=discord.Object(GUILD_ID)))
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_member_join(member):
    print("Someone joined")
    server_rules_c = member.guild.get_channel(rules_cID)
    team_assignment_c = member.guild.get_channel(ta_ID)
    await member.guild.get_channel(ta_ID).send(f"Hey {member.mention}, welcome to FIRST® Global Challenge:tada:! Don't forget to read rules in {server_rules_c.mention} and use /country in {team_assignment_c.mention}!")


@bot.tree.command(name="country", description="Get the role of your country", guild=discord.Object(GUILD_ID))
async def country(interaction: discord.Interaction, role: discord.Role):
    for letter in alphabet_emojis:
        if role.name[0] == letter:
            for r in interaction.user.roles:
                if r.name[0] in alphabet_emojis:
                    await interaction.user.remove_roles(r)
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Added role {role.name} to {interaction.user.mention}")
            return
    await interaction.response.send_message(f"Role {role.name} not found / not allowed")


@bot.tree.command(name="meet", description="Create a meeting room", guild=discord.Object(GUILD_ID))
async def meet(interaction: discord.Interaction, meeting_name: str):
    for r in interaction.user.roles:
        if r.name[0] in alphabet_emojis:
            user_country_role = r
            break
    else:
        await interaction.response.send_message("You must have a country role to create a meeting room")
        return
    overwrites = {
        interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user_country_role: discord.PermissionOverwrite(view_channel=True, connect=True, speak=True, mute_members=True,
                                                       deafen_members=True, move_members=True,
                                                       use_voice_activation=True)
    }
    category = discord.utils.get(interaction.guild.categories, name="Meeting Rooms")
    await interaction.guild.create_voice_channel(meeting_name, overwrites=overwrites,
                                                 category=category)
    await interaction.response.send_message(f"Created meeting room {meeting_name}")


@bot.tree.command(name="add", description="Add a role to meeting room", guild=discord.Object(GUILD_ID))
async def add(interaction: discord.Interaction, role: discord.Role, vc: discord.VoiceChannel):
    for r in interaction.user.roles:
        if r.name[0] in alphabet_emojis:
            user_country_role = r
            break
    else:
        await interaction.response.send_message("You must have a country role to add a role to a meeting room")
        return
    try:
        if vc.overwrites[user_country_role].mute_members:
            await vc.set_permissions(role, view_channel=True)
            await interaction.response.send_message(f"Added country {role.mention} to {vc.mention}")
            await interaction.guild.get_channel(mn_cID).send(f"{role.mention}, your country has been invited to the meeting: {vc.mention}, by team {user_country_role.mention}.\n({interaction.user.mention} added country {role.mention} to {vc.mention})")
            return
        else:
            await interaction.response.send_message(f"You don't have permission to add roles to {vc.name}")
    except:
        pass
    await interaction.response.send_message(
        f"Meeting room {vc.name} not found or you don't have permission to add roles to it")

@bot.tree.command(name="end", description="End all your meetings", guild=discord.Object(GUILD_ID))
async def end(interaction: discord.Interaction):
    for r in interaction.user.roles:
        if r.name[0] in alphabet_emojis:
            user_country_role = r
            break
    else:
        await interaction.response.send_message("You must have a country role to end your meetings")
        return
    for vc in discord.utils.get(interaction.guild.categories, name="Meeting Rooms").voice_channels:
        try:
            if vc.overwrites[user_country_role].mute_members:
                await vc.delete()
        except:
            pass
    await interaction.response.send_message("Ended all your meetings")


bot.run(TOKEN)
