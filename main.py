from logging import debug
from flask import Flask, render_template, request
from oauth import Oauth

app = Flask(__name__)

@app.route('/') # define our route
def home():
  return render_template('index.html', discord_url=Oauth.discord_login_url) # renders index.html file from templates folder

@ app.route('/login')
def login():
  code = request.args.get('code') # gets the 
  return 'Success'









if __name__ == '__main__': # only run if we are running the code
  app.run(debug=True) # allows code updates