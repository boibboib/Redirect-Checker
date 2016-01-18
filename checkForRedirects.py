#!/usr/bin/python

import praw
import re
import requests
import sys
import socket
import time
import datetime



# IDs, secrets, uris, tokens, etc for OAuth2
# (https://redd.it/3cm1p8  OAuth2 instructions from /u/GoldenSights.  Thanks!)
#----------------------------------------------------------------------------
app_id = ''
app_secret = ''
app_refresh = ''
app_uri = 'https://127.0.0.1:65010/authorize_callback'

domainWhiteList = ["cnn.com", "yahoo.com", "youtube.com"]

# init praw and log in
#----------------------
def login ():
    r=praw.Reddit("/u/boib url shortner detector")

    r.set_oauth_app_info(app_id, app_secret, app_uri)
    r.refresh_access_information(app_refresh)

    return r



#==============================================================
if __name__=='__main__':

    SUB_TO_CHECK = 'books' # your sub goes here

    r = login ()

    while True:

        try:
            print ("=========================new loop")
            for post in praw.helpers.submission_stream(r, SUB_TO_CHECK, limit = 300, verbosity=0):

                # skip self posts
                if post.domain.startswith('self.'):
                    continue

                if post.domain in domainWhiteList:
                    continue

                if any(post.domain.endswith("." + item) for item in domainWhiteList):
                    continue

                if post.url.lower().endswith(".gif") or \
                    post.url.lower().endswith(".jpg") or \
                    post.url.lower().endswith(".gifv") or \
                    post.url.lower().endswith(".png"):
                    continue

                now=datetime.datetime.now()
                print("%02d:%02d %s %s -- %s" % (now.hour, now.minute, post.short_link, post.domain, post.subreddit.display_name))

                ua = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; Microsoft; Lumia 640 XL) '
                headers = {'user-agent': ua}
                try:
                    print("____________ checking %s" % post.short_link)
                    reqs = requests.get(post.url, headers=headers, allow_redirects=False, timeout=3)

                    if reqs.status_code == 200:
                        print("____________ valid    %s" % post.short_link)

                        # todo: check for <meta http-equiv="refresh"

                    if reqs.status_code == 301 or reqs.status_code == 302:
                        print("DETECTED REDIRECT:  %s" % post.short_link)

                        # remove post?
                        # post.remove()

                except Exception as e:
                    print ("Exception: %s " % e)



        except Exception as e:
            print ("Exception in outer loop: "),
            print (e.args)



