# import logging
import telegram
from telegram.ext import Updater, CommandHandler
import requests
import json
import datetime

# logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Replace 'YOUR_BOT_TOKEN' with your actual bot token obtained from BotFather

def hi_command(update, context):
    chat_id = update.effective_chat.id
    message_text = update.message.text
    url = message_text.split('/hi ')[1]
    print(url)
    d = datetime.datetime.now()
    unixtime = int(datetime.datetime.timestamp(d)*1000)
    print(unixtime)

    try:
        headers = {'Accept': 'application/json',
                   'Method': 'GET'}
        payload = {'timestamp': unixtime,
                   'product_url': url}
        response = requests.get('https://apiv3.beecost.vn/search/product?' , headers=headers, params=payload)  
        # Replace with your desired URL
        data = response.json()
        json_str = json.dumps(data)
        # load the json to a string
        resp = json.loads(json_str)
        # print the resp
        print(resp)

        # extract an element in the response
        name = data['data']['product_base']['name']
        pID = data['data']['product_base']['product_base_id']
        mess = "Tên<b>: " + name + "</b>" + pID

        hand = context.bot.send_message(chat_id=chat_id, text=mess, parse_mode=telegram.ParseMode.HTML)

    except:
        context.bot.send_message(chat_id=chat_id, text='Error fetching URL')
        

updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('hi', hi_command))

updater.start_polling()

