# django-reeds
A collection of useful functions.

## /

### - shortcuts.py
- render\_with\_context: Adds RequestContext to render\_to\_response
    
## templatetags

### - assets.py
- Change querystring on assets based on the hash of the current Git commit (Inspiration: [Matt Langer](http://blog.mattlanger.com/post/3200453164))

### - timeago.py
- Builds `<abbr>` tags for use with Yarp's [Timeago](http://timeago.yarp.com/) javascript library

### - twittilize.py
- Detect usernames, hashtags, and links in tweets (Source: [Six Apart's typepad-motion](https://github.com/sixapart/typepad-motion/blob/master/motion/templatetags/twittilize.py))

### - verbatim.py
- Ignores "{{" and "}}" characters in a section of code. Useful for [Mustache](https://github.com/janl/mustache.js)/[jQuery-style](http://api.jquery.com/category/plugins/templates/) templates. (Source: [Eric Florenzano](https://gist.github.com/629508))