from conf import *
from feedstat import fs
import json
from urllib.request import urlopen, Request
from urllib.parse import urlparse, urljoin, quote, urlencode
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
from emailutils import uemail
from feedparser import parse as rssparse
from functools import reduce
import re

def subclassest(cls): return [ st for s in cls.__subclasses__() for st in [s]+subclassest(s) ]

class Feed:
    headers = {'User-agent':'ELinks/0.9.3 (textmode; Linux 2.6.9-kanotix-8 i686; 127x41)'}
    _defaults = {
        'mailtosuf':'', 'sendas':'nobody@localhost', 'subpref':'', 'remarks':'', 'txtregex':'.',
        'urlregex':'.', 'active':True,
        }
    toolddt = datetime.today() - timedelta(days=365)
    def qualifyurl(self,url):
        sch,base,_ = urlparse(url)[:3]
        return url if base and sch else urljoin(self.baseurl,quote(url,safe='=?&/'))
    def send(self,items):
        if self.rc.dryrun: return
        # (sendas,sendat,to,cc,bcc,subject,text,attachments)
        for i in items:
            try: uemail([(i.sendas,i.date,i.mailto,[],[],i.title,i.mailbody(),[])])
            except Exception as e: print('Error sending mail',i.title)
    def report(self): pass
    def run(self):
        if not self.active: return
        seen = fs.seen(self.url)
        txtre = re.compile(self.txtregex)
        items = [ i for i in self.items() if re.search(txtre,i.title) ]
        newitems = [ i for i in items if i.url not in seen ]
        print('f2m',self.url,':',len(newitems))
        self.report()
        self.send(newitems)
        # Conservatively, not updating if items were blank, it could temporary problem
        if len(items) > 0: fs.updstat(self.url,[i.url for i in items])
    def __init__(self,rc,fspec):
        self.rc = rc
        self.__dict__.update({**Feed._defaults,**self.rc.defaults,**fspec})
        if self.mailtosuf:
            basemail,domain = self.mailto.split('@')
            self.mailto = basemail + '+' + self.mailtosuf + '@' + domain
        self.baseurl = '://'.join(urlparse(self.url)[:2])
class item:
    def mailbody(self): return '\n\n'.join([self.descr,self.url]+self.morelinks)

class rssitem(item):
    def __init__(self,dom,f):
        self.sendas = f.sendas
        date = dom.get('published_parsed',dom.get('updated_parsed',None))
        #TODO: Meaning of trailing fields in the parsed date is not clear, we are losing TZ info
        self.date = datetime(*date[0:-3]) if date else datetime.today()
        self.mailto = f.mailto
        self.title = (('['+f.subpref+'] ') if f.subpref else '') + bs(
            dom['title'],features='html.parser').text
        self.url = dom['link']
        summary = dom['content'][0]['value'] if 'content' in dom else \
            dom['summary_detail']['value'] if 'summary_detail' in dom else dom['summary']
        self.morelinks = [ l['href'] for l in dom['links'] if l['href'] != self.url ] if 'links' in dom else []
        self.descr = bs(summary,features='html.parser').get_text(separator='\n\n')

class rss(Feed):
    def report(self):
        if self.feedtoold: print('','feed too old',self.url)
        if self.feedblank: print('','feed blank',self.url)
    def items(self):
        items = [ rssitem(i,self) for i in rssparse(self.url)['entries'] ]
        self.feedblank = len(items) == 0
        self.feedtoold = not self.feedblank and max(items,key=lambda i:i.date).date < self.toolddt
        return items

class metarss(Feed):
    def report(self):
        if self.duplcnt: print('','duplicates:',self.duplcnt)
        for f in self.feeds: f.report()
    def items(self):
        feedre = re.compile(self.feedregex)
        dom = bs(urlopen(Request(self.url,headers=self.headers)).read(),features='lxml')
        links = dom.findAll('a',href=feedre)
        sfs = [ { **sf, **{'txtre' : re.compile(sf['txtregex'])} } for sf in self.subfeeds ]
        self.feeds = [ f for f in [
            next(iter([
            rss(self.rc,{**sf,**{'subpref':self.subpref,'url':self.qualifyurl(l['href'])}})
            for sf in sfs if re.search(sf['txtre'],l.text) ]),None)  for l in links
            ] if f ]
        items = [ i for f in self.feeds if f for i in f.items() ]
        reditems = reduce( lambda cur,i: cur if i.url in cur[1] else (cur[0]+[i],cur[1].union({i.url})),
            items, ([],set()) )[0]
        self.duplcnt = len(items) - len(reditems)
        return reditems

class youtube(rss):
    ytrsspref = 'https://www.youtube.com/feeds/videos.xml?'
    def __init__(self,rc,fspec):
        urlargs = { 'channel_id' : fspec['channelid'] } if 'channelid' in fspec else {
            'playlist_id' : fspec['playlistid'] }
        url = self.ytrsspref + urlencode(urlargs)
        super().__init__(rc,{**fspec,**{'url':url}})

# TODO: Plan to do this for arbitrary url, but it's too vague, let a good use case come
#class url(Feed):
#    def items(self):
#        txtre = re.compile(self.txtregex)
#        urlre = re.compile(self.urlregex)
#        dom = bs(urlopen(Request(self.url,headers=self.headers)).read(),features='lxml')
#        links = dom.findAll('a',text=txtre,href=urlre)
#        for l in links: print(l.get('href',None))
#        return []

class FeedRC:
    def __init__(self):
        self.rc = json.load(f2mrc.open())
        self.defaults = self.rc.get('defaults',{})
        self.dryrun = self.defaults.get('dryrun',False)
        ftyps = { c.__name__:c for c in subclassest(Feed) }
        self.feeds = [ ftyps[f['typ']](self,f) for f in self.rc.get('feeds',[]) ]

frc = FeedRC()
