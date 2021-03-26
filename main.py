from logging import debug
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/') # define our route
def home():
  return render_template('index.html') # renders index.html file from templates folder

if __name__ == '__main__': # only run if we are running the code
  app.run(debug=True) # allows code updates