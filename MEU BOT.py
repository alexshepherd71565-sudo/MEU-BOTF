import requests
import asyncio
from datetime import datetime
from telegram import Bot

# --- CONFIGURAÇÕES ---
TOKEN_BOT = "7780715716:AAGSMCe5MpnCf7lf5gi8x40oaClcfdkKkOo"
CHAT_ID = "-1002592505897"
API_KEY = "aca8f12e1b6335fca710a3d42c5b1452"

async def enviar_relatorio_diario():
    bot = Bot(token=TOKEN_BOT)
    hoje = datetime.now().strftime('%Y-%m-%d')
    
    # URL da API-Sports (API-Football)
    url = f"https://v3.football.api-sports.io/fixtures?date={hoje}"
    headers = {'x-apisports-key': API_KEY}

    try:
        print(f"Iniciando busca de jogos para {hoje}...")
        response = requests.get(url, headers=headers)
        dados = response.json()
        jogos = dados.get('response', [])

        if not jogos:
            await bot.send_message(chat_id=CHAT_ID, text="⚠️ Nenhum jogo mapeado para hoje.")
            return

        mensagem = f"🚀 **LAY 0x1 ZEBRA - {datetime.now().strftime('%d/%m')}**\n"
        mensagem += "📊 *Estratégia: Full Trader / Sherlook*\n"
        mensagem += "--------------------------------------\n\n"

        contador = 0
        for item in jogos:
            # Filtramos jogos que ainda não começaram
            if item['fixture']['status']['short'] == 'NS':
                home = item['teams']['home']['name']
                away = item['teams']['away']['name']
                liga = item['league']['name']
                hora = item['fixture']['date'][11:16]

                mensagem += f"⏰ {hora} | 🏆 {liga}\n"
                mensagem += f"⚽ **{home}** vs {away}\n"
                mensagem += "🎯 Sugestão: Analisar Lay 0x1\n"
                mensagem += "--------------------------------------\n"
                contador += 1
            
            # Limite para não estourar o tamanho da mensagem do Telegram
            if contador >= 15:
                break

        await bot.send_message(chat_id=CHAT_ID, text=mensagem, parse_mode='Markdown')
        print("Relatório enviado com sucesso para o Telegram!")

    except Exception as e:
        print(f"Erro durante a execução: {e}")

# ESSA PARTE É A QUE O GITHUB USA PARA RODAR O SCRIPT
if __name__ == "__main__":
    asyncio.run(enviar_relatorio_diario())
