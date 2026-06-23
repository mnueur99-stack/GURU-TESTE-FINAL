import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import os
import uuid
import asyncio
from datetime import datetime, timezone, timedelta

# ─── Caminhos ───────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "fifa_users.json")
IMAGES_PATH = os.path.join(BASE_DIR, "data", "images")

# ─── Classes e valores ──────────────────────────────────────────────────────────
CLASS_EMOJIS = {
    "D": "⚪", "C": "🟢", "B": "🔵", "B+": "🟡",
    "A": "🟠", "A+": "🔴", "X": "🟣",
}
CLASS_VALUES = {
    "D": 50_000, "C": 100_000, "B": 200_000, "B+": 250_000,
    "A": 500_000, "A+": 750_000, "X": 1_000_000,
}
CLASS_WEIGHTS = {
    "D": 40, "C": 25, "B": 15, "B+": 10, "A": 6, "A+": 3, "X": 1,
}
BUYABLE_CLASSES = ["D", "C", "B", "B+"]

# ─── Recompensas diárias (Dia 1 → Dia 7) ───────────────────────────────────────
DAILY_REWARDS = [50_000, 75_000, 100_000, 150_000, 200_000, 350_000, 500_000]

# ─── Formações 7v7 ──────────────────────────────────────────────────────────────
FORMATIONS = {
    "2-3-1": ["GK", "DEF1", "DEF2", "MID1", "MID2", "MID3", "ATK1"],
    "3-2-1": ["GK", "DEF1", "DEF2", "DEF3", "MID1", "MID2", "ATK1"],
    "2-2-2": ["GK", "DEF1", "DEF2", "MID1", "MID2", "ATK1", "ATK2"],
    "1-3-2": ["GK", "DEF1", "MID1", "MID2", "MID3", "ATK1", "ATK2"],
}
SLOT_LABELS = {
    "GK": "🥅 Goleiro", "DEF1": "🛡️ Zagueiro 1", "DEF2": "🛡️ Zagueiro 2", "DEF3": "🛡️ Zagueiro 3",
    "MID1": "⚙️ Meio Campo 1", "MID2": "⚙️ Meio Campo 2", "MID3": "⚙️ Meio Campo 3",
    "ATK1": "⚡ Atacante 1", "ATK2": "⚡ Atacante 2",
}

POSITION_NAMES = {
    "GK": "Goleiro",
    "CB": "Zagueiro",
    "CDM": "Volante",
    "CM": "Meio Campo",
    "CAM": "Meio Ofensivo",
    "RW": "Ponta Direita",
    "LW": "Ponta Esquerda",
    "ST": "Atacante",
}

# ─── Banco de jogadores ─────────────────────────────────────────────────────────
PLAYERS_DB = {
    "scar": {
        "id": "scar",
        "name": "Scar",
        "class": "X",
        "positions": ["CB"],
        "value": 1_000_000,
        "image": "https://i.imgur.com/ZwsmNV5.jpeg",
        "ovr": 90,
        "is_plus": False,
    },
    "daviseiji": {
        "id": "daviseiji",
        "name": "Davi Seiji",
        "class": "X",
        "positions": ["GK"],
        "value": 1_000_000,
        "image": "https://i.imgur.com/H1lO2lw.jpeg",
        "ovr": 90,
        "is_plus": False,
    },
    "rapha": {
        "id": "rapha",
        "name": "Rapha",
        "class": "A+",
        "positions": ["RW", "ST"],
        "value": 750_000,
        "image": "https://i.imgur.com/lcsuTFd.jpeg",
        "ovr": 89,
        "is_plus": False,
    },
    "dudu": {
        "id": "dudu",
        "name": "Dudu",
        "class": "A+",
        "positions": ["LW", "ST", "RW"],
        "value": 750_000,
        "image": "https://i.imgur.com/qc07O7B.jpeg",
        "ovr": 89,
        "is_plus": False,
    },
    "danilo": {
        "id": "danilo",
        "name": "Danilo",
        "class": "A+",
        "positions": ["CB"],
        "value": 750_000,
        "image": "https://i.imgur.com/44uRBRe.jpeg",
        "ovr": 88,
        "is_plus": False,
    },
    "kaka": {
        "id": "kaka",
        "name": "Kaka",
        "class": "A+",
        "positions": ["ST", "CM", "CB"],
        "value": 750_000,
        "image": "https://i.imgur.com/cF6Quv6.jpeg",
        "ovr": 88,
        "is_plus": False,
    },
    "pao": {
        "id": "pao",
        "name": "Pão",
        "class": "A",
        "positions": ["GK", "CB"],
        "value": 500_000,
        "image": "https://i.imgur.com/zBg7MKK.jpeg",
        "ovr": 87,
        "is_plus": False,
    },
    "sanga": {
        "id": "sanga",
        "name": "Sanga",
        "class": "A",
        "positions": ["LW", "CM"],
        "value": 500_000,
        "image": "https://i.imgur.com/2ZYmqAm.jpeg",
        "ovr": 87,
        "is_plus": False,
    },
    "espanhol": {
        "id": "espanhol",
        "name": "Espanhol",
        "class": "A",
        "positions": ["ST", "CAM", "CM", "CB"],
        "value": 500_000,
        "image": "https://i.imgur.com/zNRLpjC.jpeg",
        "ovr": 87,
        "is_plus": False,
    },
    "felipe": {
        "id": "felipe",
        "name": "Felipe",
        "class": "A",
        "positions": ["GK"],
        "value": 500_000,
        "image": "https://i.imgur.com/tD9OOKE.jpeg",
        "ovr": 87,
        "is_plus": False,
    },
    "arti": {
        "id": "arti",
        "name": "Arti",
        "class": "A",
        "positions": ["ST", "CM"],
        "value": 500_000,
        "image": "https://i.imgur.com/MtJVCZk.jpeg",
        "ovr": 86,
        "is_plus": False,
    },
    "rick": {
        "id": "rick",
        "name": "Rick",
        "class": "A",
        "positions": ["CDM", "CB", "CM"],
        "value": 500_000,
        "image": "https://i.imgur.com/WXQ0hMW.jpeg",
        "ovr": 86,
        "is_plus": False,
    },
    "amond": {
        "id": "amond",
        "name": "Amond",
        "class": "A",
        "positions": ["GK"],
        "value": 500_000,
        "image": "https://i.imgur.com/O7d35ly.jpeg",
        "ovr": 86,
        "is_plus": False,
    },
    "rafinhaxii": {
        "id": "rafinhaxii",
        "name": "Rafinhaxii",
        "class": "A",
        "positions": ["ST", "CAM", "CM", "CB"],
        "value": 500_000,
        "image": "https://i.imgur.com/t08c7d5.jpeg",
        "ovr": 86,
        "is_plus": False,
    },
    "top": {
        "id": "top",
        "name": "Top",
        "class": "A",
        "positions": ["CDM", "CB", "CM"],
        "value": 500_000,
        "image": "https://i.imgur.com/VB3QvwB.jpeg",
        "ovr": 86,
        "is_plus": False,
    },
    "gabriel": {
        "id": "gabriel",
        "name": "Gabriel Cremonez",
        "class": "B+",
        "positions": ["CAM", "CM", "CB"],
        "value": 250_000,
        "image": "https://i.imgur.com/KZG7JIg.jpeg",
        "ovr": 85,
        "is_plus": False,
    },
    "vini": {
        "id": "vini",
        "name": "Vini",
        "class": "B+",
        "positions": ["CB"],
        "value": 250_000,
        "image": "https://i.imgur.com/guO5shN.jpeg",
        "ovr": 85,
        "is_plus": False,
    },
    "arthur": {
        "id": "arthur",
        "name": "Arthur",
        "class": "B+",
        "positions": ["ST", "CDM", "CM", "CB"],
        "value": 250_000,
        "image": "https://i.imgur.com/KNg0Jlx.jpeg",
        "ovr": 85,
        "is_plus": False,
    },
    "mobsx": {
        "id": "mobsx",
        "name": "Mobsx",
        "class": "B+",
        "positions": ["CB", "CM"],
        "value": 250_000,
        "image": "https://i.imgur.com/uzJllwp.jpeg",
        "ovr": 84,
        "is_plus": False,
    },
    "bungaz": {
        "id": "bungaz",
        "name": "Bungaz",
        "class": "B+",
        "positions": ["CB"],
        "value": 250_000,
        "image": "https://i.imgur.com/E4SwRdv.jpeg",
        "ovr": 84,
        "is_plus": False,
    },
}

# OVR padrão por classe (usado quando jogador não tem ovr definido)
CLASS_DEFAULT_OVR = {
    "D": 60, "C": 69, "B": 76, "B+": 81, "A": 85, "A+": 90, "X": 96,
}

# ─── Dificuldades da IA ──────────────────────────────────────────────────────────
AI_DIFFICULTIES = {
    "facil":    {"name": "Fácil",    "emoji": "🟢", "ovr": 54,  "min_reward": 5_000,   "max_reward": 20_000},
    "medio":    {"name": "Médio",    "emoji": "🟡", "ovr": 65,  "min_reward": 25_000,  "max_reward": 60_000},
    "dificil":  {"name": "Difícil",  "emoji": "🟠", "ovr": 75,  "min_reward": 70_000,  "max_reward": 130_000},
    "expert":   {"name": "Expert",   "emoji": "🔴", "ovr": 84,  "min_reward": 150_000, "max_reward": 280_000},
    "lendario": {"name": "Lendário", "emoji": "🟣", "ovr": 92,  "min_reward": 300_000, "max_reward": 600_000},
}

# Nomes genéricos para jogadores da IA
AI_NAMES = [
    "Silva", "Costa", "Ferreira", "Santos", "Oliveira", "Lima",
    "Pereira", "Alves", "Rodrigues", "Martins", "Barbosa", "Souza",
    "Carvalho", "Araújo", "Nascimento", "Mendes", "Gomes", "Rocha",
]

PACK_COOLDOWN_SECONDS = 60
MATCH_COOLDOWN_SECONDS = 30
PLUS_WEIGHT_MULTIPLIER = 0.25  # Cartas PLUS são 75% mais raras dentro da sua classe


# ─── Helpers de dados ────────────────────────────────────────────────────────────
def load_data():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_user(data: dict, user_id: str) -> dict:
    if user_id not in data:
        data[user_id] = {
            "balance": 0,
            "team_name": "Sem Nome",
            "stadium_name": "Sem Nome",
            "inventory": [],
            "formation": "2-3-1",
            "lineup": {},
            "captain": None,
            "daily": {
                "streak": 0,
                "last_claimed": None,
                "strikes": 0,
            },
        }
    return data[user_id]


def format_money(amount: int) -> str:
    if amount >= 1_000_000:
        v = amount / 1_000_000
        return f"{v:.1f}M".replace(".0M", "M")
    if amount >= 1_000:
        return f"{amount // 1_000}k"
    return str(amount)


def get_player(player_id: str) -> dict | None:
    return PLAYERS_DB.get(player_id)


def pick_random_player() -> dict:
    """Sorteia um jogador aleatório ponderado pela raridade da classe. Cartas PLUS são ainda mais raras."""
    all_players = list(PLAYERS_DB.values())
    weights = []
    for p in all_players:
        base = CLASS_WEIGHTS[p["class"]]
        weights.append(base * PLUS_WEIGHT_MULTIPLIER if p.get("is_plus") else base)
    return random.choices(all_players, weights=weights, k=1)[0]


def player_ovr(player_id: str) -> int:
    p = get_player(player_id)
    if not p:
        return 50
    return p.get("ovr", CLASS_DEFAULT_OVR.get(p["class"], 60))


def get_team_ovr(user: dict) -> int:
    """Calcula OVR médio do time. Posições vazias contam como 50."""
    formation = user.get("formation", "2-3-1")
    slots = FORMATIONS[formation]
    lineup = user.get("lineup", {})
    total = 0
    for slot in slots:
        iid = lineup.get(slot)
        if iid:
            item = next((i for i in user["inventory"] if i["instance_id"] == iid), None)
            total += player_ovr(item["player_id"]) if item else 50
        else:
            total += 50
    return round(total / len(slots))


def get_lineup_player_names(user: dict) -> dict[str, str]:
    """Retorna {slot: nome_do_jogador} para exibição na partida."""
    result = {}
    formation = user.get("formation", "2-3-1")
    slots = FORMATIONS[formation]
    lineup = user.get("lineup", {})
    for slot in slots:
        iid = lineup.get(slot)
        if iid:
            item = next((i for i in user["inventory"] if i["instance_id"] == iid), None)
            if item:
                p = get_player(item["player_id"])
                result[slot] = p["name"] if p else "?"
            else:
                result[slot] = "?"
        else:
            result[slot] = "*Vazio*"
    return result


def simulate_match(user_ovr: int, opp_ovr: int) -> tuple[int, int, list[dict]]:
    """
    Simula uma partida. Retorna (gols_user, gols_opp, eventos).
    eventos = [{"minuto": int, "time": "user"|"opp", "tipo": "gol"}]
    """
    total = user_ovr + opp_ovr
    user_chance = user_ovr / total  # probabilidade de marcar em cada tentativa

    # Número de eventos de gol na partida (4-10)
    num_events = random.randint(4, 10)
    user_goals = 0
    opp_goals = 0
    events = []
    used_minutes: set[int] = set()

    for _ in range(num_events):
        # Sorteia minuto único
        minute = random.randint(1, 90)
        while minute in used_minutes:
            minute = random.randint(1, 90)
        used_minutes.add(minute)

        if random.random() < user_chance:
            user_goals += 1
            events.append({"minuto": minute, "time": "user"})
        else:
            opp_goals += 1
            events.append({"minuto": minute, "time": "opp"})

    events.sort(key=lambda e: e["minuto"])
    return user_goals, opp_goals, events


def build_match_embed(
    user_name: str,
    opp_name: str,
    user_team_name: str,
    opp_team_name: str,
    user_ovr: int,
    opp_ovr: int,
    user_slots: dict[str, str],
    opp_slots: dict[str, str],
    user_goals: int,
    opp_goals: int,
    events: list[dict],
    reward: int | None,
    formation: str,
    opp_formation: str,
) -> discord.Embed:
    won = user_goals > opp_goals
    draw = user_goals == opp_goals
    color = 0x00C851 if won else (0xFFD700 if draw else 0xFF4444)
    result_emoji = "🏆" if won else ("🤝" if draw else "💔")

    embed = discord.Embed(
        title=f"🏟️ SIMULAÇÃO DE PARTIDA",
        color=color,
    )

    # Times
    embed.add_field(
        name="👤 Seu Time",
        value=f"**{user_team_name}** ({user_name})\nOVR: `{user_ovr}` | {formation}",
        inline=True,
    )
    embed.add_field(
        name="⚔️ vs",
        value="​",
        inline=True,
    )
    embed.add_field(
        name="👤 Adversário",
        value=f"**{opp_team_name}** ({opp_name})\nOVR: `{opp_ovr}` | {opp_formation}",
        inline=True,
    )

    # Escalações lado a lado
    user_lines = "\n".join(
        f"{SLOT_LABELS.get(s, s)}: **{n}**" for s, n in user_slots.items()
    )
    opp_lines = "\n".join(
        f"{SLOT_LABELS.get(s, s)}: **{n}**" for s, n in opp_slots.items()
    )
    embed.add_field(name=f"📋 Escalação — {user_team_name}", value=user_lines, inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name=f"📋 Escalação — {opp_team_name}", value=opp_lines, inline=True)

    # Eventos
    event_lines = []
    user_scorer_names = [n for s, n in user_slots.items() if n != "*Vazio*"]
    opp_scorer_names = [n for s, n in opp_slots.items() if n != "*Vazio*"]

    for e in events:
        minute = e["minuto"]
        if e["time"] == "user":
            scorer = random.choice(user_scorer_names) if user_scorer_names else "Jogador"
            event_lines.append(f"`{minute:02d}'` ⚽ **{scorer}** — {user_team_name}")
        else:
            scorer = random.choice(opp_scorer_names) if opp_scorer_names else "Jogador"
            event_lines.append(f"`{minute:02d}'` ⚽ **{scorer}** — {opp_team_name}")

    if event_lines:
        # Dividir em 1° e 2° tempo
        first = [l for l, e in zip(event_lines, events) if e["minuto"] <= 45]
        second = [l for l, e in zip(event_lines, events) if e["minuto"] > 45]
        events_text = ""
        if first:
            events_text += "**1° Tempo**\n" + "\n".join(first)
        if second:
            events_text += ("\n\n" if first else "") + "**2° Tempo**\n" + "\n".join(second)
        embed.add_field(name="⚡ Eventos", value=events_text[:1024], inline=False)

    # Resultado
    score_text = f"**{user_team_name} {user_goals} × {opp_goals} {opp_team_name}**"
    result_text = "Vitória! 🏆" if won else ("Empate! 🤝" if draw else "Derrota 💔")
    embed.add_field(
        name=f"{result_emoji} Resultado Final",
        value=f"{score_text}\n{result_text}",
        inline=False,
    )

    if reward is not None:
        if won or draw:
            embed.add_field(name="💰 Prêmio Recebido", value=f"**{format_money(reward)}**", inline=True)
        else:
            embed.add_field(name="💸 Sem prêmio", value="Tente novamente!", inline=True)

    return embed


def translate_positions(positions: list) -> str:
    return " & ".join(POSITION_NAMES.get(pos, pos) for pos in positions)


def inv_display_name(item: dict) -> str:
    p = get_player(item["player_id"])
    if not p:
        return "?"
    cls = p["class"]
    return f"{CLASS_EMOJIS[cls]} {p['name']} ({translate_positions(p['positions'])})"


def lineup_player_name(instance_id: str, inventory: list) -> str | None:
    for item in inventory:
        if item["instance_id"] == instance_id:
            p = get_player(item["player_id"])
            return p["name"] if p else None
    return None


class FIFA(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ────────────────────────────────────────────────────────────────────────────
    # /pack
    # ────────────────────────────────────────────────────────────────────────────
    @app_commands.command(name="pack", description="Abra um pack e receba um jogador aleatório! (cooldown: 1 min)")
    async def pack(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = load_data()
        user = get_user(data, str(interaction.user.id))

        # ── Cooldown de 1 minuto ──
        last_pack = user.get("last_pack")
        if last_pack:
            elapsed = (datetime.now(timezone.utc) - datetime.fromisoformat(last_pack)).total_seconds()
            if elapsed < PACK_COOLDOWN_SECONDS:
                remaining = int(PACK_COOLDOWN_SECONDS - elapsed)
                await interaction.followup.send(
                    f"⏳ Aguarde **{remaining}s** para abrir outro pack!", ephemeral=True
                )
                return

        await asyncio.sleep(1.5)

        user["last_pack"] = datetime.now(timezone.utc).isoformat()
        player = pick_random_player()
        instance_id = str(uuid.uuid4())
        user["inventory"].append({"instance_id": instance_id, "player_id": player["id"]})
        save_data(data)

        cls = player["class"]
        positions_str = translate_positions(player["positions"])
        ovr = player.get("ovr", CLASS_DEFAULT_OVR.get(cls, 60))
        is_plus = player.get("is_plus", False)
        plus_tag = " ✨" if is_plus else ""

        embed = discord.Embed(
            title=f"🔥 PACK ABERTO! 🔥",
            description=(
                f"🪪 **Nome do Jogador:** {player['name']}{plus_tag}\n"
                f"🏟️ **OVR:** {ovr} | {CLASS_EMOJIS[cls]} - Classe **{cls}**\n"
                f"⚽ **Posição:** {positions_str}\n"
                f"💶 **Valor:** {format_money(player['value'])}"
            ),
            color=0xFFD700,
        )
        embed.set_footer(text=f"Use /inventario para ver seus jogadores • {interaction.user.display_name}")

        if player.get("image"):
            embed.set_image(url=player["image"])
        
        await interaction.followup.send(embed=embed)

    # ────────────────────────────────────────────────────────────────────────────
    # /inventario
    # ────────────────────────────────────────────────────────────────────────────
    @app_commands.command(name="inventario", description="Veja todos os jogadores que você possui")
    async def inventario(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = load_data()
        user = get_user(data, str(interaction.user.id))
        inventory = user["inventory"]
        lineup = user["lineup"]
        captain = user["captain"]

        if not inventory:
            await interaction.followup.send(
                "📦 Seu inventário está vazio! Use `/pack` para abrir um pack.", ephemeral=True
            )
            return

        # Agrupar por player_id para exibir contagem
        counts: dict[str, list[str]] = {}
        for item in inventory:
            pid = item["player_id"]
            counts.setdefault(pid, []).append(item["instance_id"])

        embed = discord.Embed(
            title=f"📦 Inventário de {interaction.user.display_name}",
            color=0x5865F2,
        )
        embed.add_field(name="💳 Saldo", value=format_money(user["balance"]), inline=True)
        embed.add_field(name="👕 Time", value=user["team_name"], inline=True)
        embed.add_field(name="🏟️ Estádio", value=user["stadium_name"], inline=True)

        lines = []
        lined_up_ids = set(lineup.values())

        for pid, instances in counts.items():
            p = get_player(pid)
            if not p:
                continue
            cls = p["class"]
            name = p["name"]
            positions_str = "/".join(p["positions"])
            val = format_money(p["value"])
            count_str = f" x{len(instances)}" if len(instances) > 1 else ""
            status_parts = []
            for iid in instances:
                if iid in lined_up_ids:
                    slot = next(s for s, v in lineup.items() if v == iid)
                    status_parts.append(f"[{slot}]")
                if iid == captain:
                    status_parts.append("[👑]")
            status = " ".join(status_parts)
            lines.append(
                f"{CLASS_EMOJIS[cls]} **{name}**{count_str} • {positions_str} • {val} {status}"
            )

        embed.add_field(
            name=f"🎴 Jogadores ({len(inventory)})",
            value="\n".join(lines) or "Nenhum",
            inline=False,
        )
        embed.set_footer(text="Use /escalacao para ver sua escalação atual")
        await interaction.followup.send(embed=embed)

    # ────────────────────────────────────────────────────────────────────────────
    # /escalacao
    # ────────────────────────────────────────────────────────────────────────────
    @app_commands.command(name="escalacao", description="Veja sua escalação atual no 7v7")
    async def escalacao(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = load_data()
        user = get_user(data, str(interaction.user.id))
        lineup = user["lineup"]
        formation = user["formation"]
        slots = FORMATIONS[formation]
        captain = user["captain"]

        embed = discord.Embed(
            title=f"⚽ Escalação — {user['team_name']}",
            description=f"**Formação:** {formation} | **Estádio:** {user['stadium_name']}",
            color=0x00C851,
        )

        lines = []
        for slot in slots:
            label = SLOT_LABELS.get(slot, slot)
            iid = lineup.get(slot)
            if iid:
                pname = lineup_player_name(iid, user["inventory"])
                cap = " 👑" if iid == captain else ""
                lines.append(f"{label}: **{pname}**{cap}")
            else:
                lines.append(f"{label}: *Vazio*")

        filled = sum(1 for s in slots if s in lineup)
        embed.add_field(name="📋 Titulares", value="\n".join(lines), inline=False)
        embed.set_footer(text=f"{filled}/{len(slots)} posições preenchidas • /escalarjogador para escalar")
        await interaction.followup.send(embed=embed)

    # ────────────────────────────────────────────────────────────────────────────
    # Autocomplete helpers
    # ────────────────────────────────────────────────────────────────────────────
    async def _inventory_autocomplete(self, interaction: discord.Interaction, current: str):
        data = load_data()
        user = get_user(data, str(interaction.user.id))
        lineup_ids = set(user["lineup"].values())
        choices = []
        seen = set()
        for item in user["inventory"]:
            iid = item["instance_id"]
            pid = item["player_id"]
            p = get_player(pid)
            if not p:
                continue
            label = f"{CLASS_EMOJIS[p['class']]} {p['name']} ({translate_positions(p['positions'])})"
            if iid in lineup_ids:
                label += " [Escalado]"
            if current.lower() in label.lower() and label not in seen:
                seen.add(label)
                choices.append(app_commands.Choice(name=label[:100], value=iid))
            if len(choices) >= 25:
                break
        return choices

    async def _lined_up_autocomplete(self, interaction: discord.Interaction, current: str):
        data = load_data()
        user = get_user(data, str(interaction.user.id))
        choices = []
        for slot, iid in user["lineup"].items():
            p_name = lineup_player_name(iid, user["inventory"])
            label = f"{SLOT_LABELS.get(slot, slot)}: {p_name}"
            if current.lower() in label.lower():
                choices.append(app_commands.Choice(name=label[:100], value=iid))
        return choices

    async def _slot_autocomplete(self, interaction: discord.Interaction, current: str):
        data = load_data()
        user = get_user(data, str(interaction.user.id))
        formation = user["formation"]
        slots = FORMATIONS[formation]
        lineup = user["lineup"]
        choices = []
        for slot in slots:
            label = SLOT_LABELS.get(slot, slot)
            occupied = lineup.get(slot)
            if occupied:
                pname = lineup_player_name(occupied, user["inventory"])
                label += f" (atual: {pname})"
            if current.lower() in label.lower():
                choices.append(app_commands.Choice(name=label[:100], value=slot))
        return choices

    # ────────────────────────────────────────────────────────────────────────────
    # /escalarjogador
    # ────────────────────────────────────────────────────────────────────────────
    @app_commands.command(name="escalarjogador", description="Escale um jogador do seu inventário para a formação")
    @app_commands.describe(jogador="Escolha o jogador do inventário", posicao="Posição na formação")
    @app_commands.autocomplete(jogador=_inventory_autocomplete, posicao=_slot_autocomplete)
    async def escalar_jogador(self, interaction: discord.Interaction, jogador: str, posicao: str):
        await interaction.response.defer()
        data = load_data()
        user = get_user(data, str(interaction.user.id))

        # Verificar se instance_id existe no inventário
        inv_ids = [i["instance_id"] for i in user["inventory"]]
        if jogador not in inv_ids:
            await interaction.followup.send("❌ Jogador não encontrado no seu inventário.", ephemeral=True)
            return

        formation = user["formation"]
        if posicao not in FORMATIONS[formation]:
            await interaction.followup.send(
                f"❌ Posição inválida para a formação **{formation}**.", ephemeral=True
            )
            return

        # Verificar se o jogador já está escalado em outro slot
        for slot, iid in user["lineup"].items():
            if iid == jogador and slot != posicao:
                await interaction.followup.send(
                    f"❌ Este jogador já está escalado em **{SLOT_LABELS.get(slot, slot)}**. Remova-o primeiro.",
                    ephemeral=True,
                )
                return

        user["lineup"][posicao] = jogador
        save_data(data)

        item = next(i for i in user["inventory"] if i["instance_id"] == jogador)
        p = get_player(item["player_id"])
        slot_label = SLOT_LABELS.get(posicao, posicao)

        await interaction.followup.send(
            f"✅ **{p['name']}** escalado como **{slot_label}**!", ephemeral=False
        )

    # ────────────────────────────────────────────────────────────────────────────
    # /removerjogador
    # ────────────────────────────────────────────────────────────────────────────
    @app_commands.command(name="removerjogador", description="Remova um jogador da escalação")
    @app_commands.describe(jogador="Jogador escalado para remover")
    @app_commands.autocomplete(jogador=_lined_up_autocomplete)
    async def remover_jogador(self, interaction: discord.Interaction, jogador: str):
        await interaction.response.defer()
        data = load_data()
        user = get_user(data, str(interaction.user.id))

        slot_to_remove = None
        for slot, iid in user["lineup"].items():
            if iid == jogador:
                slot_to_remove = slot
                break

        if not slot_to_remove:
            await interaction.followup.send("❌ Jogador não está na escalação.", ephemeral=True)
            return

        del user["lineup"][slot_to_remove]
        if user["captain"] == jogador:
            user["captain"] = None

        save_data(data)

        item = next((i for i in user["inventory"] if i["instance_id"] == jogador), None)
        pname = get_player(item["player_id"])["name"] if item else "Jogador"
        slot_label = SLOT_LABELS.get(slot_to_remove, slot_to_remove)

        await interaction.followup.send(
            f"✅ **{pname}** removido de **{slot_label}**.", ephemeral=False
        )

    # ────────────────────────────────────────────────────────────────────────────
    # /escolhercapitao
    # ────────────────────────────────────────────────────────────────────────────
    @app_commands.command(name="escolhercapitao", description="Escolha o capitão do time (deve estar escalado)")
    @app_commands.describe(jogador="Jogador escalado para ser capitão")
    @app_commands.autocomplete(jogador=_lined_up_autocomplete)
    async def escolher_capitao(self, interaction: discord.Interaction, jogador: str):
        await interaction.response.defer()
        data = load_data()
        user = get_user(data, str(interaction.user.id))

        if jogador not in user["lineup"].values():
            await interaction.followup.send(
                "❌ O capitão deve estar escalado. Use `/escalarjogador` primeiro.", ephemeral=True
            )
            return

        user["captain"] = jogador
        save_data(data)

        item = next((i for i in user["inventory"] if i["instance_id"] == jogador), None)
        pname = get_player(item["player_id"])["name"] if item else "Jogador"

        await interaction.followup.send(f"👑 **{pname}** é o novo capitão do time!", ephemeral=False)

    # ────────────────────────────────────────────────────────────────────────────
    # /vender
    # ────────────────────────────────────────────────────────────────────────────
    @app_commands.command(name="vender", description="Venda um jogador do inventário pelo valor fixo")
    @app_commands.describe(jogador="Jogador que deseja vender")
    @app_commands.autocomplete(jogador=_inventory_autocomplete)
    async def vender(self, interaction: discord.Interaction, jogador: str):
        await interaction.response.defer()
        data = load_data()
        user = get_user(data, str(interaction.user.id))

        inv_ids = [i["instance_id"] for i in user["inventory"]]
        if jogador not in inv_ids:
            await interaction.followup.send("❌ Jogador não encontrado no inventário.", ephemeral=True)
            return

        item = next(i for i in user["inventory"] if i["instance_id"] == jogador)
        p = get_player(item["player_id"])
        if not p:
            await interaction.followup.send("❌ Jogador inválido.", ephemeral=True)
            return

        value = p["value"]
        user["inventory"].remove(item)
        user["balance"] += value

        # Remover da escalação/capitão se necessário
        for slot, iid in list(user["lineup"].items()):
            if iid == jogador:
                del user["lineup"][slot]
        if user["captain"] == jogador:
            user["captain"] = None

        save_data(data)

        embed = discord.Embed(
            title="💸 Jogador Vendido!",
            color=0x2ECC71,
        )
        embed.add_field(name="🪪 Jogador", value=p["name"], inline=True)
        embed.add_field(name="💶 Recebido", value=format_money(value), inline=True)
        embed.add_field(name="💳 Novo Saldo", value=format_money(user["balance"]), inline=True)
        await interaction.followup.send(embed=embed)

    # ────────────────────────────────────────────────────────────────────────────
    # /venderdupli
    # ────────────────────────────────────────────────────────────────────────────
    async def _venderdupli_autocomplete(self, interaction: discord.Interaction, current: str):
        data = load_data()
        user = get_user(data, str(interaction.user.id))
        counts: dict[str, int] = {}
        for item in user["inventory"]:
            counts[item["player_id"]] = counts.get(item["player_id"], 0) + 1
        choices = []
        for pid, qty in counts.items():
            if qty <= 1:
                continue
            p = get_player(pid)
            if not p:
                continue
            label = f"{CLASS_EMOJIS[p['class']]} {p['name']} — {qty} cópias (vender {qty-1}x por {format_money(p['value']//2)} cada)"
            if current.lower() in label.lower():
                choices.append(app_commands.Choice(name=label[:100], value=pid))
        return choices[:25]

    @app_commands.command(name="venderdupli", description="Venda todas as cópias duplicadas de um jogador pela metade do preço")
    @app_commands.describe(jogador="Jogador do qual vender as duplicatas")
    @app_commands.autocomplete(jogador=_venderdupli_autocomplete)
    async def vender_dupli(self, interaction: discord.Interaction, jogador: str):
        await interaction.response.defer()
        data = load_data()
        user = get_user(data, str(interaction.user.id))

        # Contar instâncias por player_id
        counts: dict[str, list[str]] = {}
        for item in user["inventory"]:
            pid = item["player_id"]
            counts.setdefault(pid, []).append(item["instance_id"])

        # Autocompletar: aceita nome ou id do jogador
        matched_pid = None
        for pid, p in PLAYERS_DB.items():
            if jogador.lower() in (pid.lower(), p["name"].lower()):
                matched_pid = pid
                break

        if not matched_pid:
            # Tenta match parcial pelo nome
            for pid, p in PLAYERS_DB.items():
                if jogador.lower() in p["name"].lower():
                    matched_pid = pid
                    break

        if not matched_pid or matched_pid not in counts:
            await interaction.followup.send("❌ Você não possui esse jogador no inventário.", ephemeral=True)
            return

        instances = counts[matched_pid]
        if len(instances) <= 1:
            await interaction.followup.send(
                "❌ Você não tem duplicatas desse jogador. Precisa ter **2 ou mais** cópias.",
                ephemeral=True,
            )
            return

        p = get_player(matched_pid)
        lineup_ids = set(user["lineup"].values())
        captain = user["captain"]

        # Manter 1 cópia: priorizar a que está escalada ou é capitão
        keep_id = None
        for iid in instances:
            if iid in lineup_ids or iid == captain:
                keep_id = iid
                break
        if not keep_id:
            keep_id = instances[0]

        duplicates = [iid for iid in instances if iid != keep_id]
        half_price = p["value"] // 2
        total_earned = half_price * len(duplicates)

        # Remover duplicatas do inventário
        user["inventory"] = [
            item for item in user["inventory"]
            if not (item["player_id"] == matched_pid and item["instance_id"] in duplicates)
        ]
        user["balance"] += total_earned
        save_data(data)

        embed = discord.Embed(
            title="🔁 Duplicatas Vendidas!",
            color=0xE67E22,
        )
        embed.add_field(name="🪪 Jogador", value=p["name"], inline=True)
        embed.add_field(name="📦 Cópias Vendidas", value=str(len(duplicates)), inline=True)
        embed.add_field(name="💶 Valor por cópia", value=format_money(half_price), inline=True)
        embed.add_field(name="💰 Total Recebido", value=f"**{format_money(total_earned)}**", inline=True)
        embed.add_field(name="💳 Novo Saldo", value=format_money(user["balance"]), inline=True)
        embed.set_footer(text=f"1 cópia de {p['name']} mantida no inventário")
        await interaction.followup.send(embed=embed)

    # ────────────────────────────────────────────────────────────────────────────
    # /comprar
    # ────────────────────────────────────────────────────────────────────────────
    async def _buyable_autocomplete(self, interaction: discord.Interaction, current: str):
        choices = []
        for p in PLAYERS_DB.values():
            if p["class"] not in BUYABLE_CLASSES:
                continue
            label = f"{CLASS_EMOJIS[p['class']]} {p['name']} ({translate_positions(p['positions'])}) — {format_money(p['value'])}"
            if current.lower() in label.lower():
                choices.append(app_commands.Choice(name=label[:100], value=p["id"]))
        return choices[:25]

    @app_commands.command(name="comprar", description="Compre um jogador (disponível até classe B+)")
    @app_commands.describe(jogador="Jogador que deseja comprar")
    @app_commands.autocomplete(jogador=_buyable_autocomplete)
    async def comprar(self, interaction: discord.Interaction, jogador: str):
        await interaction.response.defer()
        data = load_data()
        user = get_user(data, str(interaction.user.id))

        p = get_player(jogador)
        if not p:
            await interaction.followup.send("❌ Jogador não encontrado.", ephemeral=True)
            return

        if p["class"] not in BUYABLE_CLASSES:
            await interaction.followup.send(
                f"❌ Jogadores de classe **{p['class']}** não podem ser comprados. "
                "Somente até **🟡 B+** está disponível na loja.",
                ephemeral=True,
            )
            return

        value = p["value"]
        if user["balance"] < value:
            falta = value - user["balance"]
            await interaction.followup.send(
                f"❌ Saldo insuficiente! Você precisa de mais **{format_money(falta)}**.\n"
                f"Seu saldo: **{format_money(user['balance'])}**",
                ephemeral=True,
            )
            return

        user["balance"] -= value
        instance_id = str(uuid.uuid4())
        user["inventory"].append({"instance_id": instance_id, "player_id": p["id"]})
        save_data(data)

        embed = discord.Embed(title="🛒 Compra Realizada!", color=0x3498DB)
        embed.add_field(name="🪪 Jogador", value=p["name"], inline=True)
        embed.add_field(name="💶 Pago", value=format_money(value), inline=True)
        embed.add_field(name="💳 Saldo Restante", value=format_money(user["balance"]), inline=True)
        await interaction.followup.send(embed=embed)

    # ────────────────────────────────────────────────────────────────────────────
    # /daily
    # ────────────────────────────────────────────────────────────────────────────
    @app_commands.command(name="daily", description="Resgate sua recompensa diária (7 dias de streak)")
    async def daily(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = load_data()
        user = get_user(data, str(interaction.user.id))
        daily_info = user["daily"]
        now = datetime.now(timezone.utc)

        last_str = daily_info.get("last_claimed")
        if last_str:
            last_dt = datetime.fromisoformat(last_str)
            time_since = now - last_dt

            # Cooldown de 24h
            if time_since < timedelta(hours=24):
                remaining = timedelta(hours=24) - time_since
                hrs = int(remaining.total_seconds() // 3600)
                mins = int((remaining.total_seconds() % 3600) // 60)
                await interaction.followup.send(
                    f"⏳ Você já resgatou hoje!\nPróximo daily em **{hrs}h {mins}min**.",
                    ephemeral=True,
                )
                return

            # Streak quebrado (mais de 48h sem resgatar)
            if time_since > timedelta(hours=48):
                daily_info["streak"] = 0

        streak = daily_info.get("streak", 0)

        # Após 7 dias: strike e reset
        if streak >= 7:
            daily_info["strikes"] = daily_info.get("strikes", 0) + 1
            daily_info["streak"] = 1
            daily_info["last_claimed"] = now.isoformat()
            reward = DAILY_REWARDS[0]
            user["balance"] += reward
            save_data(data)

            embed = discord.Embed(
                title="⚠️ STRIKE! Streak resetado",
                description=(
                    f"Você ultrapassou 7 dias consecutivos e recebeu um **strike** "
                    f"(total: {daily_info['strikes']}).\nSeu streak voltou para o Dia 1."
                ),
                color=0xFF6B00,
            )
            embed.add_field(name="💰 Recompensa", value=format_money(reward), inline=True)
            embed.add_field(name="💳 Saldo", value=format_money(user["balance"]), inline=True)
            await interaction.followup.send(embed=embed)
            return

        reward = DAILY_REWARDS[streak]
        daily_info["streak"] = streak + 1
        daily_info["last_claimed"] = now.isoformat()
        user["balance"] += reward
        save_data(data)

        day_num = streak + 1
        bar = "".join("🟩" if i < day_num else "⬜" for i in range(7))

        embed = discord.Embed(
            title=f"📅 Daily — Dia {day_num}/7",
            color=0x00D26A,
        )
        embed.add_field(name="💰 Recompensa", value=format_money(reward), inline=True)
        embed.add_field(name="💳 Saldo Total", value=format_money(user["balance"]), inline=True)
        embed.add_field(name="📊 Progresso da Semana", value=bar, inline=False)

        if day_num < 7:
            next_reward = DAILY_REWARDS[day_num]
            embed.set_footer(text=f"Próximo dia: {format_money(next_reward)} • Volte amanhã!")
        else:
            embed.set_footer(text="⚠️ Atenção: Se resgatar amanhã, receberá um STRIKE e o streak reseta!")

        await interaction.followup.send(embed=embed)

    # ────────────────────────────────────────────────────────────────────────────
    # /cofre
    # ────────────────────────────────────────────────────────────────────────────
    @app_commands.command(name="cofre", description="Veja seu saldo e informações do time")
    async def cofre(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = load_data()
        user = get_user(data, str(interaction.user.id))
        daily_info = user["daily"]

        embed = discord.Embed(
            title=f"🏦 Cofre — {interaction.user.display_name}",
            color=0xF1C40F,
        )
        embed.add_field(name="💳 Saldo", value=f"**{format_money(user['balance'])}**", inline=True)
        embed.add_field(name="🎴 Jogadores", value=str(len(user["inventory"])), inline=True)
        embed.add_field(name="👕 Time", value=user["team_name"], inline=True)
        embed.add_field(name="🏟️ Estádio", value=user["stadium_name"], inline=True)
        embed.add_field(name="📋 Formação", value=user["formation"], inline=True)

        streak = daily_info.get("streak", 0)
        strikes = daily_info.get("strikes", 0)
        bar = "".join("🟩" if i < streak else "⬜" for i in range(7))
        embed.add_field(name="📅 Streak Daily", value=f"{bar} (Dia {streak}/7)", inline=False)
        if strikes > 0:
            embed.add_field(name="⚠️ Strikes", value=str(strikes), inline=True)

        await interaction.followup.send(embed=embed)

    # ────────────────────────────────────────────────────────────────────────────
    # /nomedotime
    # ────────────────────────────────────────────────────────────────────────────
    @app_commands.command(name="nomedotime", description="Defina o nome do seu time")
    @app_commands.describe(nome="Novo nome do time")
    async def nome_do_time(self, interaction: discord.Interaction, nome: str):
        await interaction.response.defer()
        if len(nome) > 40:
            await interaction.followup.send("❌ Nome muito longo! Máximo 40 caracteres.", ephemeral=True)
            return

        data = load_data()
        user = get_user(data, str(interaction.user.id))
        old = user["team_name"]
        user["team_name"] = nome
        save_data(data)

        await interaction.followup.send(
            f"✅ Nome do time alterado de **{old}** para **{nome}**!"
        )

    # ────────────────────────────────────────────────────────────────────────────
    # /nomedoestadio
    # ────────────────────────────────────────────────────────────────────────────
    @app_commands.command(name="nomedoestadio", description="Defina o nome do seu estádio")
    @app_commands.describe(nome="Novo nome do estádio")
    async def nome_do_estadio(self, interaction: discord.Interaction, nome: str):
        await interaction.response.defer()
        if len(nome) > 40:
            await interaction.followup.send("❌ Nome muito longo! Máximo 40 caracteres.", ephemeral=True)
            return

        data = load_data()
        user = get_user(data, str(interaction.user.id))
        old = user["stadium_name"]
        user["stadium_name"] = nome
        save_data(data)

        await interaction.followup.send(
            f"✅ Nome do estádio alterado de **{old}** para **{nome}**!"
        )

    # ────────────────────────────────────────────────────────────────────────────
    # /mudarformacao
    # ────────────────────────────────────────────────────────────────────────────
    @app_commands.command(name="mudarformacao", description="Mude a formação do seu time (7v7)")
    @app_commands.describe(formacao="Nova formação")
    @app_commands.choices(formacao=[
        app_commands.Choice(name="2-3-1 (2 DEF, 3 MID, 1 ATK)", value="2-3-1"),
        app_commands.Choice(name="3-2-1 (3 DEF, 2 MID, 1 ATK)", value="3-2-1"),
        app_commands.Choice(name="2-2-2 (2 DEF, 2 MID, 2 ATK)", value="2-2-2"),
        app_commands.Choice(name="1-3-2 (1 DEF, 3 MID, 2 ATK)", value="1-3-2"),
    ])
    async def mudar_formacao(self, interaction: discord.Interaction, formacao: str):
        await interaction.response.defer()
        data = load_data()
        user = get_user(data, str(interaction.user.id))

        old = user["formation"]
        if old == formacao:
            await interaction.followup.send(f"⚠️ Você já usa a formação **{formacao}**.", ephemeral=True)
            return

        # Limpar escalação ao mudar formação
        user["formation"] = formacao
        user["lineup"] = {}
        user["captain"] = None
        save_data(data)

        await interaction.followup.send(
            f"✅ Formação alterada de **{old}** para **{formacao}**!\n"
            "⚠️ Sua escalação foi resetada. Use `/escalarjogador` para montar o time."
        )

    # ────────────────────────────────────────────────────────────────────────────
    # /jogarcomia
    # ────────────────────────────────────────────────────────────────────────────
    @app_commands.command(name="jogarcomia", description="Jogue contra a IA e ganhe dinheiro! (cooldown: 30s)")
    @app_commands.describe(dificuldade="Escolha a dificuldade do adversário")
    @app_commands.choices(dificuldade=[
        app_commands.Choice(name="🟢 Fácil    — Prêmio: 5k~20k",   value="facil"),
        app_commands.Choice(name="🟡 Médio    — Prêmio: 25k~60k",  value="medio"),
        app_commands.Choice(name="🟠 Difícil  — Prêmio: 70k~130k", value="dificil"),
        app_commands.Choice(name="🔴 Expert   — Prêmio: 150k~280k",value="expert"),
        app_commands.Choice(name="🟣 Lendário — Prêmio: 300k~600k",value="lendario"),
    ])
    async def jogar_com_ia(self, interaction: discord.Interaction, dificuldade: str):
        await interaction.response.defer()
        data = load_data()
        user = get_user(data, str(interaction.user.id))

        # ── Cooldown de 30s ──
        last_match = user.get("last_match")
        if last_match:
            elapsed = (datetime.now(timezone.utc) - datetime.fromisoformat(last_match)).total_seconds()
            if elapsed < MATCH_COOLDOWN_SECONDS:
                remaining = int(MATCH_COOLDOWN_SECONDS - elapsed)
                await interaction.followup.send(
                    f"⏳ Aguarde **{remaining}s** antes de jogar outra partida!", ephemeral=True
                )
                return

        diff = AI_DIFFICULTIES[dificuldade]
        user_ovr = get_team_ovr(user)
        opp_ovr = diff["ovr"]
        user_slots = get_lineup_player_names(user)

        # Gerar escalação da IA com nomes aleatórios
        formation = user.get("formation", "2-3-1")
        slots = FORMATIONS[formation]
        opp_slots = {slot: random.choice(AI_NAMES) for slot in slots}

        await asyncio.sleep(2)

        user_goals, opp_goals, events = simulate_match(user_ovr, opp_ovr)

        won = user_goals > opp_goals
        draw = user_goals == opp_goals
        reward = 0
        if won:
            reward = random.randint(diff["min_reward"], diff["max_reward"])
            user["balance"] += reward
        elif draw:
            reward = diff["min_reward"] // 2
            user["balance"] += reward

        user["last_match"] = datetime.now(timezone.utc).isoformat()
        save_data(data)

        opp_team_name = f"IA {diff['name']}"
        embed = build_match_embed(
            user_name=interaction.user.display_name,
            opp_name=f"🤖 IA {diff['emoji']}",
            user_team_name=user["team_name"],
            opp_team_name=opp_team_name,
            user_ovr=user_ovr,
            opp_ovr=opp_ovr,
            user_slots=user_slots,
            opp_slots=opp_slots,
            user_goals=user_goals,
            opp_goals=opp_goals,
            events=events,
            reward=reward if (won or draw) else None,
            formation=formation,
            opp_formation=formation,
        )
        embed.set_footer(text=f"Saldo atual: {format_money(user['balance'])} • Cooldown: 30s")
        await interaction.followup.send(embed=embed)

    # ────────────────────────────────────────────────────────────────────────────
    # /jogar (PvP)
    # ────────────────────────────────────────────────────────────────────────────
    @app_commands.command(name="jogar", description="Desafie outro usuário para uma partida! (cooldown: 30s)")
    @app_commands.describe(adversario="Mencione o usuário que deseja desafiar")
    async def jogar(self, interaction: discord.Interaction, adversario: discord.Member):
        await interaction.response.defer()
        if adversario.bot:
            await interaction.followup.send("❌ Não dá para jogar contra um bot! Use `/jogarcomia`.", ephemeral=True)
            return
        if adversario.id == interaction.user.id:
            await interaction.followup.send("❌ Você não pode jogar contra si mesmo!", ephemeral=True)
            return

        data = load_data()
        user = get_user(data, str(interaction.user.id))

        # ── Cooldown de 30s ──
        last_match = user.get("last_match")
        if last_match:
            elapsed = (datetime.now(timezone.utc) - datetime.fromisoformat(last_match)).total_seconds()
            if elapsed < MATCH_COOLDOWN_SECONDS:
                remaining = int(MATCH_COOLDOWN_SECONDS - elapsed)
                await interaction.followup.send(
                    f"⏳ Aguarde **{remaining}s** antes de jogar outra partida!", ephemeral=True
                )
                return

        opp_data_user = get_user(data, str(adversario.id))

        user_ovr = get_team_ovr(user)
        opp_ovr = get_team_ovr(opp_data_user)
        user_slots = get_lineup_player_names(user)
        opp_slots = get_lineup_player_names(opp_data_user)
        formation = user.get("formation", "2-3-1")
        opp_formation = opp_data_user.get("formation", "2-3-1")

        await asyncio.sleep(2)

        user_goals, opp_goals, events = simulate_match(user_ovr, opp_ovr)

        won = user_goals > opp_goals
        draw = user_goals == opp_goals

        # Prêmio PvP: ganhador recebe baseado na diferença de OVR
        reward = 0
        if won:
            base = max(10_000, opp_ovr * 1_000)
            reward = random.randint(base // 2, base)
            user["balance"] += reward
        elif draw:
            reward = 5_000
            user["balance"] += reward

        user["last_match"] = datetime.now(timezone.utc).isoformat()
        save_data(data)

        embed = build_match_embed(
            user_name=interaction.user.display_name,
            opp_name=adversario.display_name,
            user_team_name=user["team_name"],
            opp_team_name=opp_data_user["team_name"],
            user_ovr=user_ovr,
            opp_ovr=opp_ovr,
            user_slots=user_slots,
            opp_slots=opp_slots,
            user_goals=user_goals,
            opp_goals=opp_goals,
            events=events,
            reward=reward if (won or draw) else None,
            formation=formation,
            opp_formation=opp_formation,
        )
        embed.set_footer(text=f"Saldo de {interaction.user.display_name}: {format_money(user['balance'])} • Cooldown: 30s")
        await interaction.followup.send(embed=embed)


    # ────────────────────────────────────────────────────────────────────────────
    # /ranking
    # ────────────────────────────────────────────────────────────────────────────
    @app_commands.command(name="ranking", description="Ver o ranking global do servidor")
    @app_commands.describe(tipo="Tipo de ranking")
    @app_commands.choices(tipo=[
        app_commands.Choice(name="🏆 Maior OVR do time", value="ovr"),
        app_commands.Choice(name="💰 Maior saldo", value="saldo"),
        app_commands.Choice(name="🎴 Mais jogadores", value="cartas"),
    ])
    async def ranking(self, interaction: discord.Interaction, tipo: str = "ovr"):
        await interaction.response.defer()
        data = load_data()

        if not data:
            await interaction.followup.send("📭 Nenhum dado encontrado ainda.", ephemeral=True)
            return

        entries = []
        for uid, user in data.items():
            team_name = user.get("team_name", "Sem Nome")
            balance = user.get("balance", 0)
            inventory_count = len(user.get("inventory", []))
            ovr = get_team_ovr(user)
            entries.append({
                "uid": uid,
                "team_name": team_name,
                "balance": balance,
                "inventory_count": inventory_count,
                "ovr": ovr,
            })

        if tipo == "ovr":
            entries.sort(key=lambda x: x["ovr"], reverse=True)
            title = "🏆 Ranking — Maior OVR do Time"
            color = 0x00C851
            def fmt(e):
                return f"**{e['team_name']}** — OVR `{e['ovr']}`"
        elif tipo == "saldo":
            entries.sort(key=lambda x: x["balance"], reverse=True)
            title = "💰 Ranking — Maior Saldo"
            color = 0xF1C40F
            def fmt(e):
                return f"**{e['team_name']}** — {format_money(e['balance'])}"
        else:
            entries.sort(key=lambda x: x["inventory_count"], reverse=True)
            title = "🎴 Ranking — Mais Jogadores"
            color = 0x5865F2
            def fmt(e):
                return f"**{e['team_name']}** — {e['inventory_count']} carta(s)"

        top10 = entries[:10]
        medals = ["🥇", "🥈", "🥉"] + [f"**{i}.**" for i in range(4, 11)]

        lines = []
        for i, e in enumerate(top10):
            try:
                member = interaction.guild.get_member(int(e["uid"]))
                mention = member.mention if member else f"<@{e['uid']}>"
            except Exception:
                mention = f"<@{e['uid']}>"
            lines.append(f"{medals[i]} {mention} — {fmt(e)}")

        embed = discord.Embed(
            title=title,
            description="\n".join(lines) if lines else "Nenhum jogador encontrado.",
            color=color,
        )
        embed.set_footer(text=f"Top {len(top10)} jogadores • Use /cofre para ver seu saldo")
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(FIFA(bot))
