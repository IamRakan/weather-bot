import requests
import os
import sys
from telegram import Update, Message
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
import conf

# Replace 'YOUR_API_KEY' with your WeatherAPI key
WEATHER_API_KEY = conf.WEATHER_API_KEY
# Replace 'YOUR_BOT_TOKEN' with your Telegram bot token
TELEGRAM_BOT_TOKEN = conf.TELEGRAM_BOT_TOKEN

async def get_weather(city):
    url = f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}'
    response = requests.get(url)
    return response.json()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Received /start command")
    await update.message.reply_text('Hello! Send me a city name to get the weather update.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Received city name")
    city = update.message.text

    weather_data = await get_weather(city)
    print(weather_data)  # Debug print

    if 'error' in weather_data:
        await update.message.reply_text('City not found.')
        return

    location = weather_data['location']['name']
    country = weather_data['location']['country']
    temp = weather_data['current']['temp_c']
    condition = weather_data['current']['condition']['text']
    feels_like = weather_data['current']['feelslike_c']
    localtime = weather_data['location']['localtime']

    # Convert localtime to the desired format
    localtime_dt = datetime.strptime(localtime, '%Y-%m-%d %H:%M')
    formatted_time = localtime_dt.strftime('%d/%m/%Y %I:%M %p')

    await update.message.reply_text(
        f'Weather in {location}, {country}:\n'
        f'Temperature: {temp}°C\n'
        f'Condition: {condition}\n'
        f'Feels Like: {feels_like}°C\n'
        f'Date and Time: {formatted_time}'
    )

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Received /restart command")
    await update.message.reply_text('Restarting the bot...')
    os.execl(sys.executable, sys.executable, *sys.argv)

def main():
    print("Bot is starting...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler('restart', restart))

    app.run_polling()
    print("Bot is running...")

if __name__ == '__main__':
    main()
