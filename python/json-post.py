from urllib import request
import json

request_data = {
    "name": "Alice",
}
headers = {
    "content-type": "application/json"
}
req = request.Request(url="http://localhost:8888/getJsonResult",
                      headers=headers,
                      data=json.dumps(request_data).encode("utf-8"))
reps = request.urlopen(req).read().decode("utf-8")
jo = json.loads(reps)
data = jo['data']
print(data)
for oneData in data:
    print(oneData)
print(len(data))
