import nextcord
from nextcord.ext import commands
import os
import json
from keepAlive import keepalive

intents = nextcord.Intents.default()
intents.voice_states = True
intents.message_content = True

# ห้ามใส่โทเค่นกับ log_channel_id ในนี้
def load_config():
    if not os.path.exists('config.json'):
        default_config = {
            "token": "YOUR_BOT_TOKEN_HERE",
            "log_channel_id": 0
        }
        with open('config.json', 'w') as file:
            json.dump(default_config, file, indent=4)
        print("Config file created. Please update 'config.json' with your bot token.")
        exit()

    with open('config.json', 'r') as file:
        return json.load(file)

bot = commands.Bot(command_prefix='!', intents=intents)

config = load_config()

@bot.event
async def on_voice_state_update(member, before, after):
    channel = bot.get_channel(config['log_channel_id'])

    if before.channel != after.channel:
        embed = nextcord.Embed()

        if before.channel is None:
            embed.description = f'{member.mention} `เข้าห้องคุย` {after.channel.mention}'
            embed.color = 0x00ff00
            embed.set_footer(text='เข้าออกมากไปโดนต่อย')
        elif after.channel is None:
            embed.description = f'{member.mention} `ออกจากห้องคุย` {before.channel.mention}'
            embed.color = 0xff0000
            embed.set_footer(text='เข้าออกมากไปโดนต่อย')
        else:
            embed.description = f'{member.mention} `ย้ายจากห้อง` {before.channel.mention} `ไปยัง` {after.channel.mention}'
            embed.color = 0xffa500
            embed.set_footer(text='เข้าออกมากไปโดนต่อย')

        await channel.send(embed=embed)

os.system('cls')

@bot.event
async def on_ready():
    print('\033[1;33;40m' + '╔═══════════════════════════════════╗' + '\033[0m')
    print('\033[1;33;40m' + '║       Bot Information             ║' + '\033[0m')
    print('\033[1;33;40m' + '╠═══════════════════════════════════╣' + '\033[0m')
    print('\033[1;33;40m' + '║  Logged in as: {}     ║'.format(bot.user) + '\033[0m')
    print('\033[1;33;40m' + '║  nextcord Version: {}          ║'.format(nextcord.__version__) + '\033[0m')
    print('\033[1;33;40m' + '║  Connected to Guilds: {}           ║'.format(len(bot.guilds)) + '\033[0m')
    print('\033[1;33;40m' + '╚═══════════════════════════════════╝' + '\033[0m')
    print('Bot is Ready to working now...')
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Discord"))

keep_alive()
bot.run(config['token'])
