#!/usr/bin/env python3
from f2mrc import frc
from feedstat import fs

for feed in frc.feeds:
    feed.run()
    if frc.dryrun: break
if not frc.dryrun: fs.savestat()
