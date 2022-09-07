import sqlite3
import requests
import json
from dotenv import dotenv_values
from apscheduler.schedulers.blocking import BlockingScheduler

def readConfig():
    '''
    reading environment variables
    '''
    return dotenv_values(".env") 

def init(latitude, longitude):
    '''
    (ab)using the default, and open GraphQL endpoint on ah.nl to extract important information about stores and their whereabouts.
    gql_body is a long graphql string tailored for getting the stores
    '''
    url = "https://www.ah.nl/gql" #open gql endpoint for anonymous requests
    headers = {'Client-Name': 'ah-stores','Client-Version':'0.230.0'} #Missing client identification. Requests should include \"client-name\" and \"client-version\" headers
    gql_body = """query stores($filter: StoreFilterInput, $size: PageSize!, $start: Int) {stores(filter: $filter, size: $size, start: $start) { result { ...storeList __typename} page { total hasNextPage __typename} __typename }}fragment storeList on Store { id name  storeType  phone distance address { ...storeAddress __typename } geoLocation { latitude longitude __typename} openingDays { ...openingDaysInfo __typename } __typename}fragment storeAddress on StoreAddress { city street houseNumber houseNumberExtra postalCode countryCode __typename}fragment openingDaysInfo on StoreOpeningDay { dayName type date openingHour { ...storeOpeningHour __typename } }fragment storeOpeningHour on StoreOpeningHour { date openFrom openUntil  __typename}"""
    json_data = {"operationName":"stores","variables":{"filter":{"location":{"latitude":latitude,"longitude":longitude}},"start":0,"size":100},"query": gql_body} #tweak size: number of albert heijns this variable is for filtering
    response = requests.post(url=url, headers=headers, json=json_data, ) #simple post request putting it all together

    if response.status_code == 200:
        storedict = {}
        templist = []
        jsonformatting = json.loads(response.text)
        for x in (jsonformatting["data"]["stores"]["result"]): #json filters for grabbing a couple of important variables
            templist.append(x['name'])
            templist.append(x['address'])
            templist.append(x['distance'])
            for y in (x['openingDays']):
                if y['type'] == "CURRENT":
                    templist.append(y['openingHour'])
            storedict[x['id']] = templist
            templist = []
    else:
        print("shit went wrong " + str(response.status_code)) #stop the program when this fails, something is definitely wrong
        print("Error: " + str(response.text))
        quit()
    return storedict

def initDB():
    '''
    initlialize the local sqldatabase appie.db for storing the current boxes
    '''
    sqliteConnection = sqlite3.connect('appie.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("DROP TABLE IF EXISTS APPIE_OFFERS")

    table = """ CREATE TABLE APPIE_OFFERS (
                StoreId INT NOT NULL,
                Amount INT NOT NULL,
                BoxCat VARCHAR(255) NOT NULL,
                BoxOldPrice FLOAT NOT NULL,
                BoxNewPrice FLOAT NOT NULL
    );"""
    cursor.execute(table)
    sqliteConnection.close()

def requestToken():
    '''
    anonymous authentication endpoint for mobile, this allows us to use "authenticated" parts of the mobile API
    '''
    authRequest = requests.post("https://api.ah.nl/mobile-auth/v1/auth/token/anonymous",json={'clientId':'appie'}) 
    global accessToken
    accessToken = json.loads(authRequest.content)["access_token"]
    refreshToken = json.loads(authRequest.content)["refresh_token"]
    return accessToken,refreshToken

def refreshToken():
    '''
    refreshing the anonymous accesstoken at the correct endpoint
    '''
    refreshRequest = requests.post("https://api.ah.nl/mobile-auth/v1/auth/token/refresh",json={'refreshToken':f'{requestToken()[1]}','clientId':'appie'})
    global accessToken
    accessToken = json.loads(refreshRequest.content)["access_token"]
    refreshToken = json.loads(refreshRequest.content)["refresh_token"]
    tokenTtl = json.loads(refreshRequest.content)["expires_in"] # token expires in 7199
    return accessToken

def telegramConnection(appieNotification):
    '''
    setting up api connection for sending Telegram messages
    '''
    bot_token = readConfig().get('telegram_bot_token')
    bot_chatID = readConfig().get('telegram_chat_id')
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + appieNotification
    response = requests.get(send_text)
    print(response.json())

def boxRequests():
    '''
    function where the magic happens: it connects to the local sqlite db, connects authenticated to the surprise-boxes api and executes queries on the database
    '''
    results = init(float(readConfig().get('latitude')),float(readConfig().get('longitude'))) #Don't forget to make this a variable / cli parameter
    sqliteConnection = sqlite3.connect('appie.db')
    cursor = sqliteConnection.cursor()
    for key,value in results.items():
        a = requests.get(f"https://api.ah.nl/ms/mobile-services/leftovers/v2/surprise-boxes/available/stores/{key}", headers={"Authorization": "Bearer " + accessToken})
        if a.text != "[]":
            for offer in json.loads(a.text):
                cursor.execute('SELECT * FROM APPIE_OFFERS WHERE (StoreId=? AND Amount=? AND BoxCat=? AND BoxOldPrice=? AND BoxNewPrice=?)', (offer["storeId"],offer['amount'],offer['boxCategory'],offer['boxOldPrice'],offer['boxNewPrice']))
                entry = cursor.fetchone()
                if entry is None:
                    cursor.execute('INSERT INTO APPIE_OFFERS (StoreId,Amount,BoxCat,BoxOldPrice,BoxNewPrice) VALUES (?,?,?,?,?)', (offer["storeId"],offer['amount'],offer['boxCategory'],offer['boxOldPrice'],offer['boxNewPrice']))
                    sqliteConnection.commit()
                    telegramConnection(f"📦 {offer['boxCategory']}, Available: {offer['amount']}\n🏢 {value[1]['street']} {value[1]['houseNumber']}, {value[1]['city']}\n🏃‍♂️ {value[2]} meters distance\n💰 €{offer['boxNewPrice']}\n🔔 Pickup {offer['pickupFrom']} until {offer['pickupTill']}\n🕢 Open {value[3]['openFrom']} until {value[3]['openUntil']}")
                else:
                    print("entry already inside")
                

def main():
    '''
    main function to keep alive forever and this starts multiple functions above and schedules the api calls for token refreshing and the box requests
    '''
    try:
        readConfig()
        initDB()
        requestToken()
        boxRequests()
        scheduler = BlockingScheduler()
        scheduler.configure(timezone='Europe/Amsterdam')
        scheduler.add_job(refreshToken, 'interval', minutes=90)
        scheduler.add_job(boxRequests, 'interval', minutes=30) #30 min interval for api requests to keep things chill
        scheduler.start()
    except KeyboardInterrupt:
        exit()


if __name__ == '__main__':
    main()

'''
https://nick.bouwhuis.io/2022/01/22/automating-any-app/

curl "https://api.ah.nl/ms/mobile-services/leftovers/v2/surprise-boxes/member" -H "Authorization: Bearer xxxxxxxxxxxxxx "

curl "https://api.ah.nl/ms/mobile-services/leftovers/v2/surprise-boxes/available/stores/[store nr.]" -H "Authorization: Bearer xxxxxxxxxxx"

curl -X POST https://api.ah.nl/mobile-auth/v1/auth/token/anonymous -H "Content-Type: Application/json" --data '{"clientId":"appie"}'

curl -X POST https://api.ah.nl/mobile-auth/v1/auth/token/refresh -H "Content-Type: Application/json" --data '{"refreshToken":"xxxxxxxxxxxxxxxxxxxxx","clientId":"appie"}

'''