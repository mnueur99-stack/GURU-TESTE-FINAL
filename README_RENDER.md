# Cruz Maltino FIFA Bot — Deploy no Render

## Estrutura de arquivos

```
/
├── __init__.py
├── bot.py
├── fifa.py
├── README_RENDER.md
└── requirements.txt
```

## Como fazer o deploy no Render

### 1. Crie uma conta no Render
Acesse https://render.com e crie sua conta gratuita.

### 2. Crie um novo serviço
- Clique em **New → Background Worker**
- Conecte seu repositório GitHub com esses arquivos

### 3. Configure o serviço
| Campo | Valor |
|---|---|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python bot.py` |

### 4. Adicione a variável de ambiente
- Vá em **Environment → Add Environment Variable**
- Chave: `DISCORD_BOT_TOKEN`
- Valor: o token do seu bot (obtido no Discord Developer Portal)

### 5. Faça o deploy
- Clique em **Deploy**
- Aguarde o build terminar
- O bot vai conectar automaticamente

## Dados salvos

Os dados dos usuários ficam em `data/fifa_users.json`.
As imagens dos jogadores ficam em `data/images/`.

> **Atenção:** No plano gratuito do Render, o serviço pode ser pausado
> após inatividade. Use um serviço de uptime (ex: UptimeRobot)
> apontando para a URL do seu worker para mantê-lo ativo.
