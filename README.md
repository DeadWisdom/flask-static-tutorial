Embracing JAMStack with Python: Generating a Static Website with Flask and Deploying to Netlify

### Big Idea

JAMStack completely changes how an entire organization can iterate on a web app. It decouples your
frontend and backend workflow, so you can focus on speed to your end-user, worry less about how
it's served, keep separate iteration cycles, and best of all, enable easy feature branching.

I'll show, step by step, how can use the powerful, established tools of Flask and Python without
bothering with specialized static-site generators.

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
The ones that do best keep going, ignore the haters, and reach out to others for help.

### Contents:

- [JAMStack: What it is and why it's awesome.](#jamstack)
- [Generating Static Websites with Flask: A step-by-step tutorial](#generating-static-websites-with-flask)
- Netlify: What it is and how to deploy your site
- Final Thoughts: Some tips and where to go from here.

# JAMStack

JAMStack is a terrible name. It sounds like a local event for jarring preserves. But it's a great
concept: Focus on a separation of Javascript, API, and Markup. It will completely change how

The frontend and the backend decouple, with the Markup becoming a _static_ platform which the
JavaScript builds on. Data is delivered from the API to the JavaScript. You can still do some
generating Markup on the server, but that is now an edge-case and is done through the API.

Since our Markup (and JavaScript) is now static, it lends itself to serving directly from a \*[CDN]: Content Delivery Network, which ensures your site is delivered as fast as possible. This is
where Netlify comes in. It makes deploying from your repository to a website super slick. And a real
fire and forget sort of process. More on that later.

Now, keeping your frontend and backend decoupled is such an amazing thing once you set it up, that
it's easily worth the price of admission. Backend often requires a lot of tests, analysis,
optimization, and generally way longer iteration cycles than frontend, which often wants to make
changes and iterate by the hour, and want to see results immediately, rather than waiting for a
backend build that's often compiling a docker image, running tests, etc and can take a long time.

Also testing feature branches in only your frontend, without needing to create a whole new backend
environment is simply amazing, and revolutionizes the experience from the developer all the way to
business stakeholders. Netlify gives you a unique URL _for every deploy_ meaning you can try out new
features, review old deploys, and quickly test for production readiness.

Lastly, keeping things decoupled also makes it easy to slot in serverless endpoints or backendless
options like Firebase or AWS Amplify. Modularity, composition, wow! Who knew it was so great?

### When to not use JAMStack

JAMStack only has one place where classic markup generation is better, and that's when you need
to generate a lot of _content_, i.e. Markup, depending on the user viewing it or based on dynamic
data.

With something like a stock-ticker, that's fine because it comes from an API. But for
something like a CMS, where the content often changes based on changes from a database, then classic
Jinja rendering is still where it's at.

Still a lot of the promises of database-driven CMS's have yet to materialize, and people are
increasingly finding it easier to simply change the content in the source code and redeploy,
especially when it's done automatically and quickly.

Further it's simple to put content generation behind an API endpoint, maybe even a serverless one.

# Generating Static Websites with Flask

This technique allows you to generate a static website in much the same way you'd make a classic
Flask app. And this example parallels examples shown by generators like 11ty and Jekyll, but in my
opinion is better because it allows us to use Python, Flask and all the great tools that come with.
Now, we could easily use Django, FastAPI, Starlette, or any other framework for this, but Flask
has two extensions that make the process really easy: Frozen-Flask and Flask-Pages.

We're going to break our endeavour into these goals:

1. [Setup / Install Our Dependencies and Setup Github](#goal-1-setup--install-our-dependencies-and-setup-github)
2. Create Our Flask App
3. Freeze It
4. Add Pages / Content with Markdown
5. Add Some JavaScript and Connect to an API

Then afterwards, I'll show you how to deploy with Netilify.

Now to it!

## Goal 1: Setup / Install our Dependencies and Setup Github

First we will setup our Git repository. Using _Github_ here, which I'm not happy about because of their
work with ICE, but it's by far the most used and accessible source repo to hook into Netlify, so we're
balancing that requirement.

Let's create [a new repository](https://github.com/new). I named it "flask-static-tutorial". I checked "Initialize this repository with a README", added a gitignore (Python), and a license (MIT). You do you.

Then, once it's made, clone the repository locally.

I'm going to assume you have Python 3.6+ on your system.
I like using [Pyenv](https://github.com/pyenv/pyenv).
A great tutorial for which, [is available here](https://realpython.com/intro-to-pyenv/).

We're also going to use [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/) for this tutorial.
It will manage our Python dependencies. Using it because it's pretty cool, but mostly because
Netlify supports it directly.
So go ahead and [install that](https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv).

Now that we have those installed, we're going to install our requirements:

    ```bash
    $ pipenv --python 3.7 install flask frozen-flask flask-flatpages
    ```

Pipenv nicely creates a virtual environment for us, a `Pipfile`, and `Pipfile.Lock`, and installs our
packages. We also tell it to use 3.7, because it is the default version for Netlify. Well that was easy.

Now let's commit it, and move on:

    ```bash
    $ git add .
    $ git commit -m 'project setup'
    $ git push
    ```

## Goal 2: Create Our Flask App

This part is basically just following the flask tutorial. The only little hiccup is that we're using
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
to put anything in that would be based on user interaction or state. Everything should be responding
to simple GET requests, not looking at `request` or anything. It's _static_ content after all.

Now we run our server, and this is where using Flask is great, because we can develop our site as we
go, without having to rebuild or run some command to do so after changes. We just pretend we are
making any old Flask site. And really, we are.

First setup our environment, then run it with pipenv.

    ```bash
    $ export FLASK_DEBUG=True
    $ export FLASK_APP=app.py
    $ pipenv run flask run
    ```

We tell `pipenv` to `run flask` and `flask` to `run`. I know a bit confusing. Alternatively you can
create a [pipenv script](https://pipenv-fork.readthedocs.io/en/latest/advanced.html#custom-script-shortcuts). But _[that's your bizzniss](https://twitter.com/iamtabithabrown)_.

Now we can open our browser to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) and be greeted.

Good job! But don't get arrogant, we have more to do.

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

Frozen-Flask is actually really simple. It just runs your app, goes to your root, copies the Markup,
and saves it to a corresponding file. To find other pages, it tracks every response from `url_for()`
and adds them to its queue.

To find other pages that are outside of your root tree, [read more about how it finds urls here](https://pythonhosted.org/Frozen-Flask/#finding-urls).

We are really close. Now we just need, you know content.

## Goal 4: Add Pages / Content with Markdown

Now you need to look into your cold, frozen heart to see what kind of website you want to make. For
me, it's simple: A site for a pet detective agency. But you do you.

One of the things 11ty, Jekyll and basically every ~~blog creation framework~~ static site generator
does is easily let you create pages with markdown. So we're going to do the same.

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
pages. You can click on each one, to copy them or make your own content. Any file you add here that
has an '.md' extension will turn into a page, provided you also link to it with `url_for()`.

    pages/
      content.md
      index.md
      team.md
      work.md

At the top of each page, you'll notice it's "meta" section, which is yaml and looks something like
this:

    ```yaml
    Title: Pet Shop Detective Agency
    Description: We sniff out the clues.

    ...
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
      </head>
      <body>
        <header>
          <a href="/" class="logo" aria-hidden="true"></a>

          <nav>
            <a href="/" {% if page.path == "index" %}active{% endif %}>Home</a>
            <a href="{{ url_for('page', path='team') }}" {% if page.path == "team" %}active{% endif %}>Team</a>
            <a href="{{ url_for('page', path='work') }}" {% if page.path == "work" %}active{% endif %}>Work</a>
            <a href="{{ url_for('page', path='contact') }}" {% if page.path == "contact" %}active{% endif %}>Contact</a>
          </nav>
        </header>

        <main>
          {% block content %}
              <h1>{{ page.meta.description }}</h1>
              {{ page.html|safe }}
          {% endblock content %}
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

We add an `h1` with the description from the page meta. And finally, we grab the `page.html` and run
a `safe` filter on it because it includes HTML that we want to render unescaped.

### Static assets

Finally, any static assets like images, css, or js that we link to need to go into `/static`.
Frozen-Flask will automatically grab them if they are used. For this example, I'm only using a few,
but you might many more:

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
      work.html

## Add Some JavaScript and Connect to an API

As a final step, we'll add some functionality to call an external API. Likely in a real world
scenario, you'd create the API, and host it yourself, or use a serverless option.

Alternatively, it's easy to use the very same repo, deploy it in a container somewhere, and now the API endpoints go there, whereas the Markup and JavaScript are served from Netlify.

For this example, we're going to connect to an existing API,
specifically [Dog CEO, Dog Api](https://dog.ceo/dog-api/).

We'll add the script linked below:

    static/js/dogs.js

And link it in `templates/page.html` with a simple:

    <script src="/static/js/dogs.js"></script>

When we freeze, you'll see, it gets added to `build/`. If we need to compile our JavaScript with
rollup, parcel, or webpack it's simple enough to run that before we do freeze.

And there we go, our site is ready to go. The last step is to deploy the thing...

# Netlify

Netlify isn't really doing anything special here. There's nothing that necessitates it, and the adventurous might want to make their own deployment system. Static assets mean that you can put the hash in a filename and cache them indefinitely. Before Netlify I had a system that chunked my large JS bundles and placed them on S3 named by hash. When I made changes, clients only had to download the updated files.

But using Netlify is a dream. They have really figured out the process. Basically, it hooks into your repo, listens for updates, then runs a build command, puts it on a CDN, and routes to it.

Every build gets saved to a _unique url_. This is key. It means we can create feature branches without
a thought. Since they talk to the same APIs we can only branch on the frontend, but that is usually
a fine trade-off.

Oh and by the way, it's free for small projects.

## Create the Site

First we make our account: [https://app.netlify.com/](https://app.netlify.com/)

Next we make our first site: [https://app.netlify.com/start](https://app.netlify.com/start)

Connect it to Github, and select your repository. For the build options,
tell it the command "python freeze.py", and our build directory is "build".

Note: Netlify's basic build environment will look at our `Pipfile` to determine the python version,
and requirements. Since it configures the base python environment we don't have to actually run it
with pipenv.

![Screenshot of the "Basic build settings" section of the Netlify New Site options](https://octodex.github.com/images/yaktocat.png)

Now press deploy. You can watch the progress by clicking on the deploy item, it will give you a full output
and status. If you get a big old "Deploy Failed", go into the deploy and scroll down in the page
to see why.

When it succeeds you will see "Published" at at the top of the 'Deploys' screen you'll see a link
like "https://infallible-beaver-cf7576.netlify.app". Click on it to view it.

As awesome as "infallible-beaver-cf7576" is, you can rename your site by going to
Settings > Domain Management. You can also bring in a custom domain.

Now every time you commit, it will go live. You can also make it only publish a specific branch,
setup triggers, etc. There's a million different options, so play around.

One important thing to know about Netlify is it has a decent redirect feature, allowing you to remap
a request like /api/dogs to wherever you want, including an API server.

And there you have it, dead simple.

# Final Thoughts

I hope I've shown how JAMStack can be an amazing way to develop, and how we don't need to leave all
the glorious wealth we have from Python to get there.

## Some Tips

Do remember that the JavaScript part of JAMStack should be your last resort. Too much these days
developers are pushing giant React bundles into clients, and our poor devices just can't handle
them.

Progressive enhancement is still, after all these years, the goal. Think as close to Markup as
possible, and then move outward as needed. So much of our time is spent implementing doomed features
that are overly complex and JavaScript nightmares, when what the user really needs is just some web
form. JAMStack can help us here, but it can also lead us to Single Page React App nightmares.

A great way to organize your apps is authenticated vs unauthenticated. Think of Markup as always
anonymous, and then JavaScript adds functionality when they login. And think of your APIs as
private and public endpoints. That helps you a lot when you get to caching.

## Communication

If you spot any problems, have any questions, or want to request further tutorials create an issue
in the project repo: [https://github.com/DeadWisdom/flask-static-tutorial/issues](https://github.com/DeadWisdom/flask-static-tutorial/issues) or hit me up on twitter: [@htmlbrantley](https://twitter.com/htmlbrantley)

Also I am available as a consultant, primarily in helping organizations streamline their innovation
and development cycles, especially where product, design, and development teams are struggling to
communicate.

Thanks!
