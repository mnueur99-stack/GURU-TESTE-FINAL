import discord
from discord.ext import commands
import os
import sys
import logging
import asyncio

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("discord-bot")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


@bot.event
async def on_ready():
    logger.info(f"Bot conectado como {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        logger.info(f"{len(synced)} comando(s) sincronizado(s)")
    except Exception as e:
        logger.error(f"Erro ao sincronizar comandos: {e}")


@bot.tree.command(name="ajuda", description="Ver todos os comandos do bot")
async def ajuda(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(
        title="📖 Comandos — Cruz Maltino FIFA",
        color=0x00B4FF,
    )
    embed.add_field(
        name="⚽ FIFA",
        value=(
            "`/pack` — Abrir um pack\n"
            "`/inventario` — Ver seus jogadores\n"
            "`/escalacao` — Ver sua escalação\n"
            "`/escalarjogador` — Escalar um jogador\n"
            "`/removerjogador` — Remover da escalação\n"
            "`/escolhercapitao` — Escolher capitão\n"
            "`/vender` — Vender um jogador\n"
            "`/venderdupli` — Vender duplicatas\n"
            "`/comprar` — Comprar um jogador\n"
            "`/daily` — Recompensa diária\n"
            "`/cofre` — Ver seu saldo\n"
            "`/nomedotime` — Definir nome do time\n"
            "`/nomedoestadio` — Definir nome do estádio\n"
            "`/mudarformacao` — Mudar formação\n"
            "`/jogar` — Desafiar outro usuário (PvP)\n"
            "`/jogarcomia` — Jogar contra a IA\n"
            "`/ranking` — Ver o ranking do servidor"
        ),
        inline=False,
    )
    embed.set_footer(text="Cruz Maltino • Vasco da Gama")
    await interaction.followup.send(embed=embed)


async def main():
    token = os.environ.get("DISCORD_BOT_TOKEN", "")
    if not token:
        logger.error("DISCORD_BOT_TOKEN nao esta definido. Adicione nos variaveis de ambiente.")
        sys.exit(1)

    await bot.load_extension("fifa")
    logger.info("Cog FIFA carregado com sucesso.")

    async with bot:
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
