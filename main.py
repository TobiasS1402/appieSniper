import requests
import json

r = requests.post("https://api.ah.nl/mobile-auth/v1/auth/token/anonymous",json={'clientId':'appie'})
accessToken = json.loads(r.content)["access_token"]
refreshToken = json.loads(r.content)["refresh_token"]

a = requests.get("https://api.ah.nl/ms/mobile-services/leftovers/v2/surprise-boxes/available/stores/1180", headers={"Authorization": "Bearer " + accessToken})

print(json.loads(a.content)['amount'])

for offer in json.loads(a.content):
    print(offer)

'''
https://nick.bouwhuis.io/2022/01/22/automating-any-app/

curl "https://api.ah.nl/ms/mobile-services/leftovers/v2/surprise-boxes/member" -H "Authorization: Bearer xxxxxxxxxxxxxx "

curl "https://api.ah.nl/ms/mobile-services/leftovers/v2/surprise-boxes/available/stores/[store nr.]" -H "Authorization: Bearer xxxxxxxxxxx"

curl -X POST https://api.ah.nl/mobile-auth/v1/auth/token/anonymous -H "Content-Type: Application/json" --data '{"clientId":"appie"}'

curl -X POST https://api.ah.nl/mobile-auth/v1/auth/token/refresh -H "Content-Type: Application/json" --data '{"refreshToken":"xxxxxxxxxxxxxxxxxxxxx","clientId":"appie"}

'''