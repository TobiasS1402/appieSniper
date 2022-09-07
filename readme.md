<div align="center" id="top"> 
  <img src="/appieSniper.png" alt="AppieSniper" width="300" height="300" />

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

## :checkered_flag: Starting ##

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

## Intersting/used endpoints
- https://api.ah.nl/ms/mobile-services/leftovers/v2/surprise-boxes/member
- https://api.ah.nl/ms/mobile-services/leftovers/v2/surprise-boxes/available/stores/[store nr.]
- https://api.ah.nl/mobile-auth/v1/auth/token/anonymous
- https://api.ah.nl/mobile-auth/v1/auth/token/refresh