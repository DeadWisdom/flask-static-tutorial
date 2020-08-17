Embracing JAMStack with Python: Generating a Static Website with Flask and Deploying to Netlify

### The Big Idea

JAMStack completely changes how individuals and entire organizations alike iterate on a web app. It decouples your
frontend and backend workflow, so you can focus on speed to your end-user, worry less about how
it's served, keep separate iteration cycles, and best of all, enable easy feature branching.

I'll show, step by step, how you can use the powerful, sophisticated tools of Flask and Python without
bothering with specialized static-site generators.

### Contents:

- [JAMStack: What it is and why it's awesome](#jamstack)
- [Generating Static Websites with Flask: A step-by-step tutorial](#generating-static-websites-with-flask)
- [Netlify: What it is and how to deploy your site](#netlify)
- [Connecting a Bundler: Use with Rollup, Webpack, Parcel, etc](#connecting-a-bundler)
- [Final Thoughts: Some tips and where to go from here](#final-thoughts)

### Important Links:

- [Github Repository for this Tutorial](https://github.com/DeadWisdom/flask-static-tutorial)
- [Project Example: Rare Pup Detective Agency](https://flask-static-tutorial.netlify.app/)
- [Netlify](https://netlify.com)
- [Flask](https://flask.palletsprojects.com/)

### Before We Begin

- Black lives matter.
- We need diversity and women in tech.
- Trans rights are human rights.
- Reminder that we are quickly destroying the earth.

All I ask for this content is that you are mindful about applying technology. It is not ours to fix
everything, nor must we take on every cause as an individual, but we are the modern day wizards and
we must remember that our actions _matter_.

And finally, if you struggle with this tutorial or the concepts herein, know that we all struggle.
Tech is a deep, long journey, we all (at every level) get frustrated and doubt ourselves constantly.
The best way is to keep going, ignore the haters, and reach out to others for help.

# JAMStack

JAMStack is a terrible name. It sounds like a local event for jarring preserves. But it's a great
concept: Focus on a separation of Javascript, API, and Markup.

The frontend and the backend decouple, with the Markup becoming a _static_ platform which the
JavaScript builds on. Dynamic data is delivered from the API to the client via JavaScript. You can
still do some dynamic Markup generation on the server, but that is now an edge-case and is done
through the API.

Since our client assets are now all static, it lends itself to serving directly from a Content
Delivery Network. This ensures your site is delivered as fast and efficiently as possible. This is
where Netlify comes in. It makes deploying from your repository to a website super slick. And a real
fire and forget solution. More on that later.

![A diagram showing JAMStack elements. JavaScript and Markup are static. JavaScript enhances Markup. API is dynamic. API and JavaScript send data to each other.](https://flask-static-tutorial.netlify.app/static/jamstack.webp)

Keeping your frontend and backend decoupled is an amazing thing once you set it up. It's easily
worth the price of admission. Backend often requires a lot of tests, analysis, optimization, and
generally way longer iteration cycles than frontend, which often wants to make changes and iterate
by the minute with immediate results. When you are changing the border radius of a button, you'd rather
not wait for a backend build that's often compiling a docker image, running tests, deploying, etc...

Testing frontend feature branches, without needing to create a whole new backend environment is game
changing. It revolutionizes everyone's experience, from the developer all the way to business
stakeholders. Netlify gives you a unique URL _for every deploy_ meaning you can try out new
features, review old deploys, and quickly test for production readiness.

Lastly, keeping things decoupled also makes it easy to slot in serverless endpoints or backendless
options like Firebase or AWS Amplify.

Modularity... Composition... Wow! Who knew it was so great?

### When not to use JAMStack

JAMStack has one place where classic markup generation is better, and that's when you need to
generate a lot of _dynamic content_, i.e. Markup that changes depending on the user viewing or some
other trip to the database.

With something like a stock-ticker, that's still doable, because it comes from an API. But for
something like a CMS, where the content often changes via a database, then classic Jinja rendering
is still where it's at.

Still, a lot of the promises of database-driven CMSs have yet to materialize, and people are
increasingly finding it easier to simply change the content in the source code and redeploy,
especially when it's done automatically and quickly.

Further it's simple to put some content generation behind an API endpoint, if you don't need a lot
of that.

# Generating Static Websites with Flask

This technique allows you to generate a static website in much the same way you'd make a classic
Flask app. And this example parallels examples shown by generators like 11ty, Gatsby, and Jekyll,
but in my opinion is better because it allows us to use Python, Flask and all the great tools that
come with.

Some benefits of using Flask instead of other static site generators:

- During development, we just get to use a Flask server, there's no compile step.
- No scaling problems when you get to lots of pages.
- We can use the same tools and mindset we use to build standard servers and API servers.
- No new domain-specific languages to do things like for-loops, and shoe-horn database querying into Markdown.
- We can still integrate with any database Flask can, any remote api, and generally do anything Python can do, which is a lot.

Now, we could easily use Django, FastAPI, Starlette, or any other framework for this,
but Flask has two extensions that make the process really easy: Frozen-Flask and Flask-FlatPages.

## Tutorial

We're going to break our endeavour into these goals:

1. [Setup / Install Our Dependencies and Setup Github](#goal-1-setup--install-our-dependencies-and-setup-github)
2. [Create Our Flask App](#goal-2-create-our-flask-app)
3. [Freeze It](#goal-3-freeze-it)
4. [Add Pages / Content with Markdown](#goal-4-add-pages--content-with-markdown)
5. [Add JavaScript and Connect to an API](#add-some-javascript-and-connect-to-an-api)

Then afterwards, I'll show you how to deploy with Netilify.

Now to it!

## Goal 1: Setup / Install our Dependencies and Setup Github

First we will setup our Git repository. Using _Github_ here, cause it's a big old standard.

Let's create [a new repository](https://github.com/new). I named it "flask-static-tutorial". I
checked "Initialize this repository with a README", added a gitignore (Python), and a license (MIT).
You do you.

Once it's made, clone the repository locally.

I'm going to assume you have Python 3.6+ on your system.
I like using [Pyenv](https://github.com/pyenv/pyenv) which manages the installation and selection of
multiple Python versions. A great tutorial [is available here](https://realpython.com/intro-to-pyenv/).

We're also going to use [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/) for this tutorial.
It will manage our Python dependencies. I'm using it mostly because Netlify supports `Pipfile` directly.
So go ahead and [install that](https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv).

Now that we have those installed, we'll install our requirements:

```bash
$ pipenv --python 3.7 install flask frozen-flask flask-flatpages
```

Pipenv nicely creates a virtual environment for us, a `Pipfile`, and `Pipfile.Lock`, and installs our
packages. We also tell it to use 3.7, because it is the default version for Netlify.

Now let's commit it, and move on:

```bash
$ git add .
$ git commit -m 'project setup'
$ git push
```

## Goal 2: Create Our Flask App

This part is basically just following the flask tutorial. The only little change is that we're using
Pipenv.

Let's make `app.py`:

```python
from flask import Flask

# Create our app object, use this page as our settings (will pick up DEBUG)
app = Flask(__name__)

# For settings, we just use this file itself, very easy to configure
app.config.from_object(__name__)

# We want Flask to allow no slashes after paths, because they get turned into flat files
app.url_map.strict_slashes = False

# Create a route to our index page at the root url, return a simple greeting
@app.route("/")
def index():
    return "Hello, Flask"
```

Basic Flask stuff. Of course, you can do anything here, even talk to a database, but you don't want
to add anything that is based on user interaction or state. Everything should respond
to a simple GET request. Accessing the `request` global is a red-flag here. It's _static_ content after all.

Now we run our server, and this is where using Flask is great, because we can develop our site as we
go, without having to rebuild or run some command to do so after changes. We just pretend we are
making any old Flask site. And really, we are.

First setup our environment, then run it with Pipenv.

```bash
$ export FLASK_DEBUG=True
$ export FLASK_APP=app.py
$ pipenv run flask run
```

We tell `pipenv` to `run flask` and `flask` to `run`. Hope you follow. Alternatively you can
create a [pipenv script](https://pipenv-fork.readthedocs.io/en/latest/advanced.html#custom-script-shortcuts).
But _[that's your bizzniss](https://twitter.com/iamtabithabrown)_.

Now we can open our browser to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) and be greeted.

Great work! But don't get arrogant, we have more to do.

## Goal 3: Freeze It

Did you know you can [make frozen ice cubes in the hot desert like the Persians thousands of years ago?](https://www.realclearscience.com/blog/2018/07/09/how_people_created_ice_in_the_desert_2000_years_ago.html)
Did you also know you can make a frozen Flask website in your computer? Even in the desert.

Earlier we installed [Frozen-Flask](https://pythonhosted.org/Frozen-Flask/). To get started,
all we need is another file `freeze.py`:

```python
from flask_frozen import Freezer
from app import app

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
```

And then run it:

```bash
$ pipenv run python freeze.py
```

You'll see that it makes a directory `build` and the file `index.html`. Open it up and you'll see
exactly what your browser gets when it goes to 'http://127.0.0.1:5000/' when our flask process is
running.

Frozen-Flask is really simple. It just runs your app, gets every root endpoint (ones without a path
variable), copies the Markup, and saves it to a corresponding file. To find other pages, it tracks
every response from `url_for()` and adds them to its queue.

To find pages that are outside of your root tree, [read more about how it finds urls here](https://pythonhosted.org/Frozen-Flask/#finding-urls).

We are really close. Now we just need, you know content.

## Goal 4: Add Pages / Content with Markdown

It is time. Time for you to look into your cold, frozen heart to see what kind of website you want
to make. For me, it's simple: A site for a pet detective agency. But you do you.

One of the things 11ty, Jekyll and basically every ~~blog creation framework~~ static site generator
does is easily let you create pages with markdown. We're going to do the same.

This is where Flask-FlatPages comes in. It lets us create pages in any format we want, process them,
and then deliver them as HTML.

### App.py Changes

Let's update our `app.py`:

```python
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
```

Note, that we could make other routes to do whatever we want, but currently we just have one that
works with Flask-FlatPages.

### Markdown Pages

We've got Flask-FlatPages looking for pages in a `pages` directory as default. So let's create some
pages. You can click on each one to copy them or make your own content. Any file you add here that
has an '.md' extension will turn into a page, provided you also link to it in another page with
`url_for()`.

[browse files](https://github.com/DeadWisdom/flask-static-tutorial/blob/master/pages/)

    pages/
      content.md
      index.md
      team.md

At the top of each page, you'll notice its "meta" section, which is YAML and looks something like
this:

```yaml
Title: Rare Pup Detective Agency
Description: We sniff out the clues.
```

Within the pages, you might notice some HTML. Don't forget, markdown lets us embed HTML! Use it.

### Jinja Template

Now let's create our Jinja template, that serves as the wrapper for our pages `templates/page.html`:

```html+jinja
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="/static/base.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
  </head>
  <body>
    <header>
      <nav>
        <a href="/" class="logo" aria-hidden="true"></a>
        <a href="/" {% if page.path == "index" %}active{% endif %}>Home</a>
        <a href="{{ url_for('page', path='team') }}" {% if page.path == "team" %}active{% endif %}>Team</a>
        <a href="{{ url_for('page', path='contact') }}" {% if page.path == "contact" %}active{% endif %}>Contact</a>
      </nav>
    </header>

    <main>
      <article>
      {% block content %}
          <h1>{{ page.meta.description }}</h1>
          {{ page.html|safe }}
      {% endblock content %}
      </article>
    </main>
  </body>
</html>
```

Mostly we have a basic page here. There are a few things to note:

```html+jinja
<a href="{{ url_for('page', path='team') }}" {% if page.path == "team" %}active{% endif %}>Team</a>
```

We use flask's `url_for()` method to get the final url of our "team" page, also we have add an
'active' attribute to the `<a>` tag when we are on that page, for styling purposes.

Also in our content block, we do:

```html+jinja
<h1>{{ page.meta.description }}</h1>
{{ page.html|safe }}
```

We add an `<h1>` with the description from the page meta. And finally, we grab the `page.html` and run
a `safe` filter on it because it includes HTML that we want to render unescaped.

### Static assets

Finally, any static assets like images, css, or js that we link to need to go into `/static`.
Frozen-Flask will automatically grab them if they are used. For this example, I'm only using a few,
but you might many more:

[browse files](https://github.com/DeadWisdom/flask-static-tutorial/blob/master/static/)

    static/
      images/
        logo.png
      base.css

### Develop & Freeze

Alright, alright. That was a lot. Let's check out how we did, make changes, etc. During development
we simply use the flask server, and it will auto-reload. We can pretend it's just a normal flask
site:

```bash
$ pipenv run flask run
```

When we're done, we can test the freeze, it should put all our pages and assets into the build
directory:

    build/
      static/
        images/
          logo.png
        base.css
      content.html
      index.html
      team.html

## Goal 5: Add JavaScript and Connect to an API

As a final step, we'll add some functionality to call an external API. In a real world
scenario, you'd create the API, and host it yourself, or use a serverless option. Here we are just
calling out to the wonderful service [Dog CEO, Dog Api](https://dog.ceo/dog-api/).

We'll add the script linked below:

[static/js/dogs.js](https://github.com/DeadWisdom/flask-static-tutorial/blob/master/static/js/dogs.js)

It defines a custom element "dog-picture" which we've already spread through the site. If the user
didn't have JavaScript, the browser just ignores all of the `<dog-picture>` elements. Once this
script is loaded, they spring to life. Custom Elements. Neat.

We link it in `templates/page.html` with a simple:

```html
<script type="module" src="/static/js/dogs.js"></script>
```

When we freeze, you'll see, it gets added to `build/`. If we need to compile our JavaScript with
rollup, parcel, or webpack it's simple enough to run that before we do freeze.

Only one more thing, let's deploy the thing...

# Netlify

Once we have the static content, we need somewhere to put it. Since it's all static, we can
basically put it anywhere: behind nginx, on an S3, whatever. But it's best to put it behind a Content
Delivery Network, where your data will live on multiple servers around the globe that are specially
designed to cache and serve content quickly. The only trouble is managing that deployment process.

And that's why we use Netlify. They have really figured out the process. Basically, it hooks into
your repo, listens for updates, then runs a build command, puts it on a CDN, and routes to it.

Every build gets served by a _unique url_. This is key. It means we can create feature branches of our frontend without a thought.

And, nicely, it's free for small projects like this.

## Create the Site

First we make our account: [https://app.netlify.com/](https://app.netlify.com/)

Next we make our first site: [https://app.netlify.com/start](https://app.netlify.com/start)

Connect it to Github, and select your repository. For the build options,
tell it the command "python freeze.py", and our build directory is "build".

Note: Netlify's basic build environment will look at our `Pipfile` to determine the python version,
and requirements. Since it configures the base python environment we don't have to actually run it
with pipenv.

![Screenshot of the "Basic build settings" section of the Netlify New Site options](https://flask-static-tutorial.netlify.app/static/build-settings.webp)

Now press "Deploy Site". You can watch the progress by clicking on the deploy item, it will give you a full output
and status. If you get a big old "Deploy Failed", go into the deploy and scroll down in the page
to see why.

![Screenshot of the logs for a failed deploy.](https://flask-static-tutorial.netlify.app/static/failed-logs.webp)

When it succeeds you will see "Published" at at the top of the 'Deploys' screen you'll see a link
like "https://infallible-beaver-cf7576.netlify.app". Click on it to view it.

![Screenshot of the deploy page for a successful deploy.](https://flask-static-tutorial.netlify.app/static/deploy-success.webp)

As awesome as "infallible-beaver-cf7576" is, you can rename your site by going to
Settings > Domain Management. You can also bring in a custom domain.

Now every time you commit, it will go live. You can also make it only publish a specific branch,
setup triggers, etc. There's a million different options, so play around.

## Some Netlify Extras

Netlify has a decent redirect feature, allowing you to remap a request like /api/\* to wherever you want, including a custom API endpoint. [Read about Redirects and Rewrites](https://docs.netlify.com/routing/redirects/).

Our `contact.md` page has a form that doesn't go anywhere, but it has a `data-netlify="true"` tag, which is automatically processed by Netlify. It gather all submissions, and you can read them in the site admin. Also, you can set up notifications for them. [Read about Netlify Forms](https://docs.netlify.com/forms/setup/).

Light authentication can be done pretty simply with [Netlify's Authentication System](https://docs.netlify.com/visitor-access/identity/).

# Connecting a Bundler

The great part about this approach is we don't need a build step, but sometimes you need JavaScript
to bundle, by running Rollup, Webpack, Parcel, etc. There are two places you need this. One is
during development when you make a change, and the other is during your publish step.

### Bundle For Publishing

One is to change your Netlify build command to something like this:

```bash
$ npm run build && python freeze.py
```

Have your package manager build right into your static folder like `/static/build`, and then have
your Flask template pickup the JavaScript file there. Flask-Freeze will then move it to the `/build`
directory for Netlify to use.

### Bundle For Development

I'll encourage you to use a resource like [open-wc.org](https://open-wc.org) or [Snowpack](https://www.snowpack.dev/) so that you _don't_ have to build anything for development. ES6 being what it is, you don't need to
anymore.

That said, sometimes we don't get to choose. In that case, we need to run our flask server and the
bundler in watch mode.

The simplest way is to just run two terminals:

```bash
    Terminal 1: $ pipenv run flask run
```

```bash
    Terminal 2: $ npm run webpack --watch
```

### Bundle with Webpack

If you're using Webpack, Andrew Montalenti ([@amontalenti](https://twitter.com/amontalenti)) wrote
a bridge between Webpack and Flask that leans on Flask-Static, check it out at his gist:

[https://gist.github.com/amontalenti/ffeca0dce10f29d42a82e80773804355](https://gist.github.com/amontalenti/ffeca0dce10f29d42a82e80773804355)

# Final Thoughts

I hope I've shown how JAMStack can be an amazing way to develop, and how we don't need to leave all
the glorious wealth we have from Python to get there. From here you can look into [Zappa for
serverless endpoints](https://github.com/Miserlou/Zappa), deploying containers to [AWS Fargate](https://aws.amazon.com/fargate/), or using good old [Google App Engine](https://cloud.google.com/appengine/), for your
API needs. I still prefer the latter for setting up quick Python APIs.

## Some Tips

Do remember that the JavaScript part of JAMStack should be your last resort. Too much these days
developers are pushing giant React bundles into clients, and our poor devices just can't handle
them.

Progressive enhancement is still, after all these years, the goal. Think as close to Markup as
possible, and then move outward as needed. So much of our time is spent implementing doomed features
that are overly complex and JavaScript nightmares. Meanwhile what the user really needs is just some
web form. JAMStack can help us here, but it can also lead us to Single Page React App nightmares.

A great way to organize your apps is authenticated vs unauthenticated. Think of Markup as always
anonymous, and then JavaScript adds functionality when they login. And think of your APIs as
private and public endpoints. That helps you a lot when you get to caching.

## Alternatives to Netlify

Netlify isn't really doing anything special here. There's nothing that necessitates it, and the adventurous might want to make their own deployment system. Static assets mean that you can put the hash in a filename and cache them indefinitely. Before Netlify I had a system that chunked my large JS bundles and placed them on S3 named by hash. When I made changes, clients only had to download the updated chunk files.

You can also publish right to [GitHub Pages](https://pages.github.com/).

Host it on an [NGinx](https://www.nginx.com/) server, and put [CloudFare](https://www.cloudflare.com/) in front of it.

## Alternatives to Flask

Django has [Django-Freeze](https://github.com/fabiocaccamo/django-freeze) to create static content in
much the same way you'd do it here.

[Pelican](https://blog.getpelican.com/) is a python based static site generator.

Use [11ty](https://11ty.dev) if you want a full-featured specialized static generator written in
Javascript.

## Communicate With Me!

If you spot any problems, have any questions, or want to request further tutorials create an issue
in the project repo: [https://github.com/DeadWisdom/flask-static-tutorial/issues](https://github.com/DeadWisdom/flask-static-tutorial/issues)

Or hit me up on twitter: [@deadwisdom](https://twitter.com/deadwisdom)

Also I am available as a consultant, primarily in helping organizations streamline their innovation
and development cycles, especially where product, design, and development need to communicate.

Thanks to those that helped me writing this, including [@matteasterday](https://twitter.com/matteasterday), [@DanielReesLewis](https://twitter.com/DanielReesLewis), and [@amontalenti](https://twitter.com/amontalenti).

And thank you!
