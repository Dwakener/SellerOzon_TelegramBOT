import telebot
import os.path
import requests 
import json

bot = telebot.TeleBot("", parse_mode=None)
OzonAPIKey=''
ClientIdOzon=''
bot.remove_webhook()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
info_path = os.path.join(BASE_DIR, "info.txt")

#статус импорта товара 
@bot.message_handler(commands=['simport'])  
def mess(message):
    headers = {
    "Client-Id":ClientIdOzon,
    "Api-Key":OzonAPIKey,
    }
    body = {
            "task_id":0
            }
    body = json.dumps(body)
    r = requests.post('https://api-seller.ozon.ru/v1/product/import/info', data=body, headers=headers)
    js = json.loads(r.text)   
    bot.send_message(message.from_user.id,js['message'])

#список товаров
@bot.message_handler(commands=['pinfo']) 
def mess(message):
    msg = bot.send_message(message.chat.id, 'Пришлите идентификатор товара в системе продавца — артикул.')
    bot.register_next_step_handler(msg,pinfo) 
    
def pinfo(message):
    offer_id = message.text
    headers = {
    "Client-Id":ClientIdOzon,
    "Api-Key":OzonAPIKey,
    }
    body = {
            "offer_id": str(offer_id),
            "product_id": 0,
            "sku": 0
            }
    body = json.dumps(body)
    r = requests.post('https://api-seller.ozon.ru/v2/product/info', data=body, headers=headers)
    js = json.loads(r.text)   
    bot.send_message(message.from_user.id,js['result']['name']+'\n'+js['result']['price'])
    response=requests.get(js['result']['primary_image'])
    if response.status_code==200:
        with open(js['result']['offer_id']+'.jpg','wb') as imgfile:
            imgfile.write(response.content)
    bot.send_photo(message.from_user.id, photo=open(js['result']['offer_id']+'.jpg', 'rb'))
    
@bot.message_handler(content_types=['text'])   
def mess(message):
    f = open(info_path)
    info = f.read()
    bot.send_message(message.from_user.id,info)
    f.close

if __name__ == '__main__':
    bot.polling(none_stop=True)