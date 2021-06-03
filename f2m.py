#!/usr/bin/env python3
from f2mrc import frc
from feedstat import fs

for feed in frc.feeds:
    try: feed.run()
    except Exception as e: print('','There was an error running this feed')
    if frc.dryrun: break
if not frc.dryrun: fs.savestat()
