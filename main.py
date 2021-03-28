from logging import debug
from quart import Quart, render_template, request, session
from quart_discord import DiscordOAuth2Session
import os

app = Quart(__name__)
app.config['SECRET_KEY'] = 'test123'
app.config['DISCORD_CLIENT_ID'] = 789975160517689374
app.config['DISCORD_CLIENT_SECRET'] = os.getenv('DISCORD_CLIENT_SECRET')
app.config['DISCORD_REDIRECT_URI'] = 'http://127.0.0.1:5000/callback'

discord = DiscordOAuth2Session(app)

@app.route('/') # define our route
async def home():
  return render_template('index.html', discord_url=Oauth.discord_login_url) # renders index.html file from templates folder

@ app.route('/login')
async def login():
  code = request.args.get('code')

  at = Oauth.get_access_token(code)

  session['token'] = at

  user = Oauth.get_user_json(at)
  user_name, user_id = user.get('username'), user.get('discriminator')

  return f'Success, logged in as {user_name}#{user_id}'









if __name__ == '__main__': # only run if we are running the code
  app.run(debug=True) # allows code updates