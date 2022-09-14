<div align="center" id="top"> 
  <img src="https://user-images.githubusercontent.com/46230851/190220948-4d11bff5-6278-4420-b328-5d06879db352.png" alt="AppieSniper" width="300" height="300" />

  &#xa0;

</div>

<h1 align="center">AppieSniper</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/TobiasS1402/appiesniper?color=56BEB8">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/TobiasS1402/appiesniper?color=56BEB8">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/TobiasS1402/appiesniper?color=56BEB8">

  <img alt="License" src="https://img.shields.io/github/license/{{YOUR_GITHUB_USERNAME}}/appiesniper?color=56BEB8">

  <!-- <img alt="Github issues" src="https://img.shields.io/github/issues/{{YOUR_GITHUB_USERNAME}}/appiesniper?color=56BEB8" /> -->

  <!-- <img alt="Github forks" src="https://img.shields.io/github/forks/{{YOUR_GITHUB_USERNAME}}/appiesniper?color=56BEB8" /> -->

  <!-- <img alt="Github stars" src="https://img.shields.io/github/stars/{{YOUR_GITHUB_USERNAME}}/appiesniper?color=56BEB8" /> -->
</p>

<Status>

<h4 align="center"> 
	🚧  AppieSniper 🚀 Under construction...  🚧
</h4> 

<hr>

<br>

## :dart: About ##

A simple Python program for polling the Albert Heijn REST and Graph API's to get updates on new ["Overblijver"](https://www.ah.nl/over-ah/beter-eten/overblijvers) boxes.

The program works by grabbing the nearest x (default 5) number of Albert Heijn stores based on your latitude and longitude. After this it keeps a record of stores with boxes available and it will send you a Telegram notification when something's changed. e.g. boxes are available, a box is gone, everything is gone.

## ☸ Running inside a container ##

### 🚢 pulling from ghcr.io ###
```bash
# Clone this project
$ docker pull ghcr.io/tobiass1402/appiesniper:v0.1.2

# Run the project with env file
$ docker run --env-file ./.env -d ghcr.io/tobiass1402/appiesniper:v0.1.2r

# Run the project with docker env variables
$ docker run -d ghcr.io/tobiass1402/appiesniper:v0.1.2 -e longitude=5.1331746 -e latitude=51.5868726 -e telegram_bot_token='xxxxxxxx:xxxxxxxxxxxxxxxxxxxx' -e telegram_chat_id='xxxxxxxx' -e number_of_stores=5
```

### 🔨 Building it yourself ###
```bash
# Clone this project
$ git clone https://github.com/TobiasS1402/appiesniper

# Access
$ cd appiesniper

# Build the container environment
$ docker build . -t tobiass1402/appiesniper

# Run the project with env file
$ docker run --env-file ./.env -d tobiass1402/appiesniper

# Run the project with docker env variables
$ docker run -d tobiass1402/appiesniper -e longitude=5.1331746 -e latitude=51.5868726 -e telegram_bot_token='xxxxxxxx:xxxxxxxxxxxxxxxxxxxx' -e telegram_chat_id='xxxxxxxx' -e number_of_stores=5
```

## ☸ Running standalone ##

```bash
# Clone this project
$ git clone https://github.com/TobiasS1402/appiesniper

# Access
$ cd appiesniper

# Install dependencies
$ pip -r install requirements.txt

# Customise environment variables
$ cp .env.example .env

# Run the project
$ python3 main.py

```
## 🤖 Telegram bot screenshot
Telegram bot features:
- 📦 Type of box and amount
- 🏢 Location streetname, number & city
- 🏃‍♂️ Meters distance from set up longitude & latitude
- 💰 Discounted price down from "original"
- 🔔 Pickup time window
- 🕢 Store opening time window
<div align="left" id="top"> 
  <img src="https://user-images.githubusercontent.com/46230851/190221028-976d68be-8ace-45b4-be18-ddcc43cce262.png" alt="AppieSniper" width="300" height="500" />
</div>
	
## Interesting / used endpoints
- `https://api.ah.nl/ms/mobile-services/leftovers/v2/surprise-boxes/member`
- `https://api.ah.nl/ms/mobile-services/leftovers/v2/surprise-boxes/available/stores/[store nr.]` #acquired from strore browser at https://www.ah.nl/winkels?storeId=2268 
- `https://api.ah.nl/mobile-auth/v1/auth/token/anonymous`
- `https://api.ah.nl/mobile-auth/v1/auth/token/refresh`
