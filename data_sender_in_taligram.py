

# it is simple code send sms in talegram
import requests

def send_data_taligram(message):

    try:
        token = "7994787431:AAGr9K23vbm5KV3yTxnB0RggtlCF_pK-5Sk"
        chat_id = "6375857077"
        # message = "🚀 Hello Pjpk! This is a test message from your Telegram bot."

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message
        }

        requests.post(url, data=payload)
    except Exception as a:
        print(a)


