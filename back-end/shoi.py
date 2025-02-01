import json
import requests

response = requests.request(
    "POST",
    url="http://127.0.0.1:8080/api/write",
    data=json.dumps({
        "to": "Katie",
        "from": "John",
        "text": "I can't help but smile every time I think of you. You've brought so much light into my life that I often wonder how I got so lucky. Your presence makes the simplest moments feel extraordinary, and being with you has shown me a love I didn't know was possible.\nI adore everything about you—the way you laugh, the way you listen, the way you make even the hardest days feel manageable. You have a warmth that draws me in, a kindness that inspires me, and a strength that amazes me. With you, I feel safe, seen, and understood in a way I've never felt before."
    }),
    headers={
        "Authorization": "Bearer foo",
        "Content-type": "application/json"
    }
)

print(response.status_code)