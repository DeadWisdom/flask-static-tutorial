from flask import Flask, render_template
from flask_flatpages import FlatPages

# Tell Flatpages to auto reload when a page is changed, and look for .md files
FLATPAGES_AUTO_RELOAD = True
FLATPAGES_EXTENSION = '.md'

# Create our app object, use this page as our settings (will pick up DEBUG)
app = Flask(__name__)

# For settings, we just use this file itself, very easy to configure
app.config.from_object(__name__)

# We want Flask to allow no slashes after paths, because they get turned into flat files
app.url_map.strict_slashes = False

# Create an instance of our extension
pages = FlatPages(app)

# Route to FlatPages at our root, and route any path that ends in ".html"
@app.route("/")
@app.route("/<path:path>.html")
def page(path=None):
    # Look for the page with FlatPages, or find "index" if we have no path
    page = pages.get_or_404(path or 'index')

    # Render the template "page.html" with our page and title
    return render_template("page.html", page=page, title=page.meta['title'])