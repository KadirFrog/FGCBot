import discord
from discord.ext import commands
from private_data import TOKEN, GUILD_ID
from countries import alphabet_emojis
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    #await bot.wait_until_ready()
    print(await bot.tree.sync(guild=discord.Object(GUILD_ID)))
    print(f"Logged in as {bot.user.name}")

@bot.tree.command(name="country",description="Get the role of your country", guild=discord.Object(GUILD_ID))
async def country(interaction:discord.Interaction,role:discord.Role):
    for letter in alphabet_emojis:
        if role.name[0] == letter:
            for r in interaction.user.roles:
                if r.name[0] in alphabet_emojis:
                    await interaction.user.remove_roles(r)
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Added role {role.name} to @{interaction.user.name}")
            return
    await interaction.response.send_message(f"Role {role.name} not found / not allowed")
bot.run(TOKEN)
