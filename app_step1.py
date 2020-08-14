from flask import Flask

# Create our app object, use this page as our settings (will pick up DEBUG)
app = Flask(__name__)

# For our debug, we just use this file itself, easy to configure
app.config.from_object(__name__)

# We want Flask to allow no slashes after paths, because they get turned into flat files
app.url_map.strict_slashes = False

# Create a route to our index page at the root url, render the template "index.html"
@app.route("/")
def index():
    return "Hello, Flask"