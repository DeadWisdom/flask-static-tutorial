Embracing JAMStack with Python: Generating a Static Website with Flask and Deploying to Netlify

### Big Idea

JAMStack completely changes how entire organizations can iterate on a website. It decouples your
frontend and backend workflow, so you can focus on speed to your end-user, worry less about how
it's served, keep separate iteration cycles, and best of all, enable easy feature branching.

I'll show, step by step, how can use the powerful, established tools of Flask and Python without
bothering with specialized static-site generators.

### Before We Begin

- Black lives matter
- We need diversity and women in tech
- Trans rights are human rights
- We are destroying the earth

All I ask for this content is that you are mindful about applying technology. It is not ours to fix
everything, nor must we take on every cause as an individual, but we are the modern day wizards and
we must remember that our actions _matter_.

And finally, if you struggle with this tutorial or the concepts herein, know that we all struggle.
Tech is a deep, long journey, we all (at every level) get frustrated and doubt ourselves constantly.
The ones that do best keep going, ignore the haters, and reach out to others for help.

### Contents:

- JAMStack: What it is and why it's awesome.
- Generating Static Websites with Flask: A step-by-step tutorial
- Netlify: What it is and how to deploy your site

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

1. Setup / Install Our Dependencies and Setup Github
2. Create Our Flask App
3. Add Pages / Content
4. Give It Some Style
5. Freeze It

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

    $ pipenv install flask frozen-flask flask-flatpages

Pipenv nicely creates a virtual environment for us, a `Pipfile`, and `Pipfile.Lock`, and installs our
packages. Well that was easy.

Now let's commit it, and move on:

    $ git add .
    $ git commit -m 'project setup'
    $ git push
