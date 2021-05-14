# feeds2mail

Most people seem to have forgotten about email, unfortunately. It still is a
great PIM (personal information management) tool.

email is a nice way to keep track of your reading queues, whether daily
newspapers or monthly magazines or yearly journals or your favorite news
channels or youtube feeds etc. With email you get a familiar interface, ability
to (auto) classify contents into different folders as per your own taste and
priorities, share them with someone, thread them, keep status as read or
unread, trim your reading queue by deleting unwanted or read articles etc.

If you are like me and use a text based client like mutt, even nicer if you use
procmail to classify your email (you can, of course, use 'filters' facility of
your mail provider also) above conveniences are all the more empowering. But it
will be a digression to get into the details of that.

feeds2mail (f2m for short) is inspired by rss2email, but with a more
generalized notion of feeds, that includes RSS but adds more to it.

If you use email classification wisely, f2m can become a highly customizable
feed aggregator, with highly organized contents. For example, different feeds
for the same topic (say, feed for your city in different newspapers) can be
brought together into one email folder. For this, there is a builtin support
for generating +<tag> suffix in the email address to which the articles are
mailed, which makes it easy to classify emails for procmail or any other
filters.

Following are the feed types supprted by f2m. More detailed usage description
of each type follows in later subsections.

## rss

Basic good old RSS feed is supported by f2m

## metarss

Most publishers have a page called 'RSS Feeds' on which they list several of
their feeds dedicated to different topics. metarss feed type in f2m is like a
feed of feeds, where you specify the URL of feeds page and regular expressions
to pick individual feeds by their topics.

A very handy feature you get with this is, the state of the feed is tracked at
the metarss level. It helps eliminate duplicate items from various feeds, or
items that appear today in one feed and tomorrow in another.

## youtube (channels and playlists)

youtube itself provides an rss interface to its channels and playlists. In f2m
by merely specifying the channel or playlist id, the feed can be activated.

Better organized publishers create specific channels or playlists for their
popular shows. Sometimes they aren't easy to find. Do use the FILTERS widget on
youtube search and restrict your search to channels or playlists (in two
separate search queries). If you are lucky you might get a precise channel or
playlist for the contents you want to track.

But if you do not find one. You can subscribe to the default channel of the
publisher, which will typically have all the content it ever publishes - only a
small fraction of which you are interested in. You can achieve the filtering by
specifying txtregex property to filter a busy feed to retain only the articles
of your interest. (All properties are described in the later sections below.)

# System Requirements:

- python3 is required

Following python packages are required

- py-filelock
- py-feedparser

# Setting up feeds

Feed settings reside in $HOME/.f2mrc.json. A sample settings file
sample.f2mrc.json is included in the package.

# Running f2m

Make sure that you have $HOME/.f2mrc.json in place, as described above.

You might want to create a script such as with name f2m with contents like
below in a directory in your PATH, typically in $HOME/bin or /usr/local/bin

    exec <f2m_install_dir>/feeds2mail/f2m.py

## Running manually

Typing just f2m will process the feeds and generate email as per your
specification. As of now there are no command line arguments.

## Running as a cron job

Most typically way to run f2m is to place it in cron jobs. The cron daemon
would be typically set to email you the stdout contents.

It's typical to run it once or twice a day. Be aware that some feeds change
annoyingly fast, for example - if it is of a youtube feed of a news channel. Yo
might want to adjust your cron frequency accordingly.

# f2m standard output and diagnostic information

On stdout, f2m prints the feed url and number of new items for which it has
generated email. Under this line with an indent, it may report one or more of
the following diagnostics if applicable:

duplicates: Count of duplicate items (appearing more than once to be precise)
in metarss feeds. This typically happens with newspaper feeds. For example some
items may appear under a 'city' feed as well as 'nation' feed. f2m sends them
only once and attributes them to the first feed specification they match with
in the subfeeds list.

feed too old: Feeds with latest item being 365 days or more older than today.
May be this feed has stopped adding articles and you might want to remove it
from your feeds list.

feed blank: This happens to some feeds over time. Instead of retaining the last
updated state, publisher's system might keep them blank, or the URL might just
get invalidated. But note that this message would occur even if for some
transient technical reasons the feed could not be accessed. So do verify things
before removing this feed from your feed list.

# Locking to avoid concurrent runs

f2m uses py-filelock to lock the feeds' state to avoid the file getting
corrupted due to concurrent runs. Check if another process is running if you
get an error suggesting so.

# Access to state of the feeds

Usually you should not require doing this. f2m stores lists of 'seen' articles
in $HOME/.f2mdb/feedstat.json, to filter the already emailed articles from the
mails. Preferably do not tinker with this file manually unless you know what
you are doing.

# Wish list

- May add More feed types such as more arbitrary url patterns in future

- Multithreading to speed up the run

- Make a proper python package, include pre-requisites, include the launch
  script

- Purge history of removed feeds
