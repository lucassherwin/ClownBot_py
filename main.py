from logging import debug
from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session, Unauthorized, requires_authorization
import os
from dotenv import load_dotenv


load_dotenv()

app = Quart(__name__)
# app.config['SECRET_KEY'] = 'test123'
app.secret_key = b'random string'
app.config['DISCORD_CLIENT_ID'] = 789975160517689374
app.config['DISCORD_CLIENT_SECRET'] = os.getenv('DISCORD_CLIENT_SECRET')
app.config['DISCORD_REDIRECT_URI'] = 'http://127.0.0.1:5000/callback'
app.config["DISCORD_BOT_TOKEN"] = "Nzg5OTc1MTYwNTE3Njg5Mzc0.X953sw.qWA1Xm0TKBlG7jIpbgDEWlCRxy8"

discord = DiscordOAuth2Session(app)

@app.route('/') # define our route
async def home():
  return await render_template('index.html') # renders index.html file from templates folder

@app.route('/login')
async def login():
  return await discord.create_session()

@app.route('/callback')
async def callback():
  await discord.callback()
  # return redirect(url_for('home'))
  # try:
  #   print('in try')
  #   await discord.callback()
  # except:
  #   print('in except')
  #   return redirect(url_for('login'))

  user = await discord.fetch_user()
  return f'{user.name}#{user.discriminator}'









if __name__ == '__main__': # only run if we are running the code
  app.run(debug=True) # allows code updates