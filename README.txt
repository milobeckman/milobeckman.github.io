MILOBECKMAN.COM
website design and upkeep


milobeckman.com is set up like a blog, with text-oriented posts organized by
date and tags. This document describes the structure of the website and outlines
the process for adding new content.

There are five folders in the milobeckman home directory:

 * /style - contains CSS stylesheets and HTML templates, which all user-facing
   pages reference

 * /assets - further subdivided by year and month, e.g. /assets/2016/10. Images,
   interactives, and other resources embedded in user-facing pages

 * /content - further subdivided by year and month, e.g. /content/2016/10. For
   each post, contains:
	(1) my_post.txt, the content in plaintext (with HTML markup)
	(2) my_post.xml, metadata about the post incl date and tags
	(3) my_post.html, the user-facing webpage displaying the post

 * /tags - for each tag, contains:
	(1) my_tag.xml, a list of all posts with this tag
	(2) my_tag.html, a user-facing webpage displaying the 10 most recent
	    posts with this tag
	(3+) my_tag_2.html, displaying items 11-20 if necessary, etc.

 * /workspace - contains python scripts used to update all other files when a
   new post is added or other changes are made; new posts are moved here

To add a new post, new_post.txt, move it to /workspace and run the script
/scripts/add_post.py as follows:



