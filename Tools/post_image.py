import requests

data = {
        "bot_id": "638f64d07ce7f83bdee814c31d",
        "text": "Hello world",
        "attachments": [
            {
                "type": "image",
                "url": "https://i.groupme.com/4032x3024.jpeg.37f296d676e5423cac6d59eef546541e"
                }
            ]
        }

print requests.post('https://api.groupme.com/v3/bots/post', json=data)
