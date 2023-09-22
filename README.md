# Fibers
A small flask/python test web-app for Helsinki Uni project course "Database and web-programming"

Fibers is a web-app that allows its users to communicate in discussion-threads called fibers. 
A fiber is a communication space that is bound by a topic and is also tagged with useful labels 
that describe the contents of the fiber.

Users can follow different fibers based on their interests. The fibers a user is following 
are found on the front page of the application. User can browse for fibers to follow or visit through 
a search feature where one can search for fibers based on their tags or by word matches in its topic.

Discussion inside a fiber progresses in a time-linear fashion. Newest posts are found at the top of 
the page, and they get older when scrolling down. User can create and attach a text-based post to the 
thread, and it will take its place on it based on the time it has been attached to it.

If there is is time, I would love to try to make some extra features too:
  - I would like to make adding photos to the posts in addition to text 
    content possible too
  - Make it possible for users to at least delete, or even modify posts
    that they have attached to the fiber
  - Try making some sort of feed-feature to the front page. Either 
    just a cronological list of individual posts from the fibers a user
    is following, or maybe a peak hole to the fibers that has most recent 
    activity in it. Let's see

# Current State of Project
There is a crude layout for the UI that has no sign in functionality yet, so only one user locally. 
There is only one fiber at the moment, and it is open when the app is initialized. You can send 
text-only messages in this local fiber, and they will get inserted into a running PostgreSQL database. 
Messages persist in the database and get loaded on the screen when the main page is loaded.

# How to run the app on your Computer
The application runs on python 3, so it will run on different operating systems, but this 
install guide will show you the process on Ubuntu-linux with superuser.

You can dowload and uncompress the zip-file directly, or you can use Git download the package.

If you choose to use Git, you must install Git first
~~~sudo apt-get update && sudo apt-get install git~~~

Next clone the Fibers repository to a suitable location on your machine using Git
~~~git clone https://github.com/xTanzu/Fibers.git~~~

Now we need to install Python3
~~~sudo apt update && sudo apt install python3~~~

And in the root of our package right inside the "Fibers" folder, lets create a virtual environment with venv
~~~Python3 -m venv .venv~~~

From same location, we'll activate the virtual environment
~~~source .venv/bin/activate~~~

We now have an active virtual environment. From the same location, install all the required dependencies listed in .venv_requirements.txt
~~~pip install -r .venv_requirements.txt

Now we have to install and setup PostgreSQL database, and there is a small script for that (using superuser privileges). Run it from the same location.
~~~./database_setup.sh~~~

If you have PostgreSQL already installed, you need to still run the script so it will create the user and database with the required tables that the application will use.
There is a file in the root called postgresql_quide.txt to help you start and stop the postgreSQL service and remove it from your system when you dont need it anymore.

No we have everything we need and we can start the flask development server from the same location, which is the root of the package right in the "Fibers" folder.
~~~flask --app src/app.py run~~~

Now the application is running on localhost port 5000. You can view it in the browser by typing in "http://localhost:5000/"
