import requests
import schedule
import time
import asyncio
from datetime import datetime
from telegram import Bot

# --- CONFIGURAÇÕES TÉCNICAS ---
TOKEN_BOT = "7780715716:AAGSMCe5MpnCf7lf5gi8x40oaClcfdkKkOo"
CHAT_ID = "-1002592505897"
API_KEY = "aca8f12e1b6335fca710a3d42c5b1452"

async def analise_diaria_mercado():
    bot = Bot(token=TOKEN_BOT)
    hoje = datetime.now().strftime('%Y-%m-%d')
    
    # Conectando à API-Sports (Dados globais)
    url = f"https://v3.football.api-sports.io/fixtures?date={hoje}"
    headers = {
        'x-apisports-key': API_KEY
    }

    try:
        print(f"[{datetime.now()}] Iniciando busca de jogos...")
        response = requests.get(url, headers=headers)
        dados = response.json()
        jogos = dados.get('response', [])

        if not jogos:
            await bot.send_message(chat_id=CHAT_ID, text="⚠️ Sem jogos mapeados para hoje.")
            return

        mensagem = f"🚀 **LAY 0x1 ZEBRA - {datetime.now().strftime('%d/%m')}**\n"
        mensagem += "📊 *Estratégia: Normalização (Full Trader)*\n"
        mensagem += "--------------------------------------\n\n"

        contador = 0
        for item in jogos:
            home = item['teams']['home']['name']
            away = item['teams']['away']['name']
            liga = item['league']['name']
            hora = item['fixture']['date'][11:16]

            # Filtro básico: Vamos focar em jogos com status 'Not Started' (NS)
            if item['fixture']['status']['short'] == 'NS':
                mensagem += f"⏰ {hora} | 🏆 {liga}\n"
                mensagem += f"⚽ **{home}** vs {away}\n"
                mensagem += "🎯 Sugestão: Monitorar Lay 0x1 Zebra\n"
                mensagem += "--------------------------------------\n"
                contador += 1
            
            # Limite de 15 jogos para a mensagem não ficar gigante no Telegram
            if contador >= 15:
                break

        await bot.send_message(chat_id=CHAT_ID, text=mensagem, parse_mode='Markdown')
        print(f"[{datetime.now()}] Lista enviada com sucesso!")

    except Exception as e:
        print(f"Erro ao processar: {e}")

def agendamento():
    asyncio.run(analise_diaria_mercado())

# --- PROGRAMAÇÃO ---
# Define o envio para as 08:00 da manhã
schedule.every().day.at("08:00").do(agendamento)

# Envio de teste imediato ao abrir o bot (opcional)
# agendamento() 

print("✅ Bot de Elite iniciado!")
print(f"📅 Aguardando para enviar a lista às 08:00 no canal {CHAT_ID}")

while True:
    schedule.run_pending()
    time.sleep(60)