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
