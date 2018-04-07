from flask import Flask, request
import json
import requests
import mysql.connector

# ตรง YOURSECRETKEY ต้องนำมาใส่เองครับจะกล่าวถึงในขั้นตอนต่อๆ ไป
global LINE_API_KEY
LINE_API_KEY = 'Bearer Ic7C4amybrY/6I6lkMssHnGSK3vVz95ZMrSYPqjcRt+Sf+VxzcYDVAy8507sOMd+sP3XZPUyugknLV56oNMg3woZGXOsjUDclHB/E9r+2Og2VczR3137EvthFQjkz2fg34JJxhaX7RDMhN6C840V5gdB04t89/1O/w1cDnyilFU='

app = Flask(__name__)
con = mysql.connector.connect(user='bdb2c368d1a6ad',
                            password='09b374bf',
                            host='us-cdbr-iron-east-05.cleardb.net',
                            database='heroku_056efb00ca70c61',
                            ssl_ca = './cleardb-ca.pem',
                            ssl_key = './bdb2c368d1a6ad-key.pem',
                            ssl_cert = './bdb2c368d1a6ad-cert.pem'
                              )

@app.route('/')
def index():
    return 'This is chatbot server.'

@app.route('/bot', methods=['POST'])

def bot():
    # ข้อความที่ต้องการส่งกลับ
    replyStack = list()
   
    # ข้อความที่ได้รับมา
    msg_in_json = request.get_json()
    msg_in_string = json.dumps(msg_in_json)
    
    # Token สำหรับตอบกลับ (จำเป็นต้องใช้ในการตอบกลับ)
    replyToken = msg_in_json["events"][0]['replyToken']

    # ทดลอง Echo ข้อความกลับไปในรูปแบบที่ส่งไป-มา (แบบ json)
    replyStack.append(msg_in_string)
    reply(replyToken, replyStack[:5])
    
    return 'OK',200
 
def reply(replyToken, textList):
    # Method สำหรับตอบกลับข้อความประเภท text กลับครับ เขียนแบบนี้เลยก็ได้ครับ
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': LINE_API_KEY
    }
    msgs = []
    for text in textList:
        msgs.append({
            "type":"text",
            "text":text
        })
    data = json.dumps({
        "replyToken":replyToken,
        "messages":msgs
    })
    requests.post(LINE_API, headers=headers, data=data)
    return

if __name__ == '__main__':
    app.run()
