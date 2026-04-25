import requests
ip= input("")
url = f"http://ip-api.com/json/{ip}"

dist = requests.get(url)

print(dist.text)