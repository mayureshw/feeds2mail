#!/usr/bin/env python3
from f2mrc import frc
from feedstat import fs

# monkey patch https://stackoverflow.com/questions/9772691/feedparser-with-timeout
# A timeout was supposed to come in feedparser https://github.com/kurtmckee/feedparser/pull/77
import socket
socket.setdefaulttimeout(30)


# monkey patch https://stackoverflow.com/questions/28282797/feedparser-parse-ssl-certificate-verify-failed
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
# monkey ends

for feed in frc.feeds:
    try: feed.run()
    except Exception as e: print('','There was an error running this feed:',e)
    if frc.dryrun: break
if not frc.dryrun: fs.savestat()
