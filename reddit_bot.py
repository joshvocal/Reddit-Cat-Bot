# =============================================================================
# IMPORTS
# =============================================================================
import praw
import time
import sys
import os


# =============================================================================
# FUNCTIONS
# =============================================================================

def authenticate():
    print("Authenticating...")

    # Try to successfully authenticate our bot, else exit.
    try:
        reddit = praw.Reddit(
            'SFU_Admission_Bot',
            user_agent="Cat Bot v-1.01")
        print("Authenticated as {}".format(reddit.user.me()))
    except Exception as e:
        print(e)
        sys.exit(1)

    return reddit


def run_bot(reddit, submissions_replied_to):
    print("Obtaining {} submissions from the subreddit r/{}...".format(
        SEARCH_LIMIT, SUBREDDIT))

    # Search the subreddit for the newest post.
    for submission in reddit.subreddit(SUBREDDIT).new(limit=SEARCH_LIMIT):
        # Check if we have not commented on it before.
        if submission.id not in submissions_replied_to:
            submission.reply(SUBMISSION_POST_MESSAGE)
            print("Commented on a submission: " + submission.id)

            # Add the submission id to our list of submissions we have
            # commented on.
            submissions_replied_to.append(submission.id)

            # Open the .txt file with all the submissions we have commented on
            # and add the submission id we just commented on so we don't
            # comment on it again.
            with open("submissions_replied_to.txt", "a") as file:
                file.write(submission.id + "\n")

    # Sleep so we don't spam the subreddit we are commenting on.
    print("Sleeping for {} seconds.".format(WAIT_TIME_IN_SECONDS))
    time.sleep(WAIT_TIME_IN_SECONDS)


def get_saved_comments():
    # Check if the .txt file exists in the current directory and create
    # it if it does not exist.
    if not os.path.isfile("submissions_replied_to.txt"):
        submissions_replied_to = []
    else:
        with open("submissions_replied_to.txt", "r") as file:
            submissions_replied_to = file.read()
            submissions_replied_to = submissions_replied_to.split("\n")

    return submissions_replied_to


def main():
    while True:
        run_bot(reddit, submissions_replied_to)


# =============================================================================
# GLOBALS
# =============================================================================


submissions_replied_to = get_saved_comments()
reddit = authenticate()

USER_AGENT = "Cat Bot v-1.01"
SUBREDDIT = "CatsStandingUp"
SEARCH_LIMIT = 1
WAIT_TIME_IN_SECONDS = 10
SUBMISSION_POST_MESSAGE = "Cat."

# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == '__main__':
    main()
