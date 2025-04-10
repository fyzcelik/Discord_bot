import discord
from discord.ext import commands
import bot_database

bot_database.init_db()

intents = discord.Intents.default()
intents.message_content = True  
intents.guilds = True           
intents.members = True         

bot = commands.Bot(command_prefix='!', intents=intents)
@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(
                    "**👋 Merhaba! Ben Görev Takip Botuyum.**\n"
                    "Komutları görmek için `!commands` yazabilirsin ✨"
                )
                break


@bot.command(name="commands")
async def show_commands(ctx):
    help_text = (
        "**🛠️ Kullanabileceğiniz Komutlar:**\n"
        "```\n"
        "!add_task <açıklama> → Yeni görev ekler\n"
        "!delete_task <id> → Görevi siler\n"
        "!show_tasks → Tüm görevleri listeler\n"
        "!complete_task <id> → Görevi tamamlandı olarak işaretler\n"
        "!commands → Komut listesini gösterir\n"
        "```"
    )
    await ctx.send(help_text)
@bot.event
async def on_ready():
    print(f'{bot.user} hazır!')

@bot.command()
async def add_task(ctx, *, description):
    bot_database.add_task(description)
    await ctx.send("✅ Görev eklendi!")

@bot.command()
async def delete_task(ctx, task_id: int):
    bot_database.delete_task(task_id)
    await ctx.send("🗑️ Görev silindi!")

@bot.command()
async def show_tasks(ctx):
    tasks = bot_database.get_tasks()
    if not tasks:
        await ctx.send("📭 Hiç görev yok!")
    else:
        message = "\n".join([f"{id}. {desc} - {'✅' if done else '❌'}" for id, desc, done in tasks])
        await ctx.send(f"📋 Görevler:\n{message}")

@bot.command()
async def complete_task(ctx, task_id: int):
    bot_database.complete_task(task_id)
    await ctx.send("🏁 Görev tamamlandı!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("🤖 Böyle bir komut yok. Lütfen geçerli bir komut gir.")
    else:
        raise error 


bot.run("MTM1OTk0NTEwNTUxMDg5NTcyOQ.GpzXOW.h2s-q9f-mRGEEzw50yZPtuxF-z2s-tcHI-2G4A")
