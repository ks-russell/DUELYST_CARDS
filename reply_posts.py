import praw
import pdb
import re
import os
from config_bot import *

# Check that the file that contains our username exists
if not os.path.isfile("config_bot.py"):
    print("You must create a config file with your username and password.")
    print("Please see config_skel.py")
    exit(1)

# Create the Reddit instance
user_agent = ("practic 0.1")
r = praw.Reddit(user_agent=user_agent)

# and login
r.login(REDDIT_USERNAME, REDDIT_PASS,disable_warning=True)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = set()

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = filter(None, posts_replied_to)

# Get the top 5 values from our subreddit
subreddit = r.get_subreddit('pythonforengineers')
for submission in subreddit.get_hot(limit=5):
    # print submission.title

    for comment in praw.helpers.flatten_tree(submission.comments):

        # If we haven't replied to this post before
        if comment.id not in posts_replied_to:

            # Do a case insensitive search
            if re.search("pizza", comment.body, re.IGNORECASE):
                # Reply to the post
                comment.reply("pie")
                print("Bot replying to : ", comment.body)

                # Store the current id into our list
                posts_replied_to.append(comment.id)

# Write our updated list back to the file
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
