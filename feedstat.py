from conf import *
from filelock import FileLock
import sys
import json

class FeedStat:
    def seen(self,url): return set(self.stat.get(url,[]))
    def updstat(self,k,v): self.stat[k] = v
    def __init__(self):
        self.lock = FileLock(f2mdblock)
        try: self.lock.acquire(timeout=0)
        except:
            print('another instance is running')
            sys.exit(1)
        self.stat = json.load(f2mdb.open())
    def savestat(self):
        print('updating feedstat')
        with f2mdb.open('w') as fp: json.dump(self.stat,fp,indent=4)

fs = FeedStat()
