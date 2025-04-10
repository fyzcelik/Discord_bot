import discord
from discord.ext import commands
import bot_database

bot_database.init_db()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptı!')

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

@bot.command()
async def add_task(ctx, *, description):
    bot_database.add_task(description)
    tasks = bot_database.show_tasks()
    formatted = "\n".join([
        f"{i+1}. {desc} - {'✅' if done else '❌'}"
        for i, (id, desc, done) in enumerate(tasks)
    ])
    await ctx.send(f"Görev eklendi!\nEklenen görev: `{description}`")

@bot.command()
async def delete_task(ctx, index: str):
    try:
        index = int(index)
        tasks = bot_database.show_tasks()
        if index < 1 or index > len(tasks):
            await ctx.send("Bu sırada bir görev yok!")
            return
        task_id, desc, done = tasks[index - 1] 
        bot_database.delete_task(task_id)
        await ctx.send(f"Görev silindi! \nSilinen görev: `{desc}`")
    except ValueError:
        await ctx.send("Lütfen bir sayı gir. Örneğin:`!delete_task 2` gibi.")

@bot.command()
async def show_tasks(ctx):
    tasks = bot_database.show_tasks()
    if not tasks:
        await ctx.send("Şu anda hiç görev yok.")
    else:
        formatted = "\n".join([
            f"{i+1}. {desc} - {'✅' if done else '❌'} "
            for i, (id, desc, done) in enumerate(tasks)
        ])
        await ctx.send(f"Mevcut görevler:\n{formatted}")

@bot.command()
async def complete_task(ctx, index: str):
    try:
        index = int(index)
        tasks = bot_database.show_tasks()
        if index < 1 or index > len(tasks):
            await ctx.send("Bu sırada bir görev yok!")
            return
        task_id, desc, done = tasks[index - 1]
        bot_database.complete_task(task_id)
        await ctx.send(f"Görev tamamlandı! \nTamamlanan görev: `{desc}`")
    except ValueError:
        await ctx.send("Lütfen bir sayı gir. Örneğin:`!complete_task 1` gibi.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Böyle bir komut yok. Lütfen geçerli bir komut gir.")
    else:
        raise error 

bot.run("MTM1OTk0NTEwNTUxMDg5NTcyOQ.GpzXOW.h2s-q9f-mRGEEzw50yZPtuxF-z2s-tcHI-2G4A")
