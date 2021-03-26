import requests

import os

class Oauth:
  client_id = '789975160517689374'
  client_secret = os.getenv('DISCORD_SECRET')
  redirect_uri = 'http://127.0.0.1:5000/login'
  scope = 'identify%20email%20guilds'
  discord_login_url = 'https://discord.com/api/oauth2/authorize?client_id=789975160517689374&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Flogin&response_type=code&scope=identify%20email%20guilds'
  discord_token_url = 'https://discord.com/api/oauth2/token'
  discord_api_url = 'https://discord.com/api'