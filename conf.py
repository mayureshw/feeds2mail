from os import environ
from pathlib import Path

home = Path(environ['HOME'])
f2mrc = home.joinpath('.f2mrc.json')
f2mdbdir = home.joinpath('.f2mdb')
f2mdb = f2mdbdir.joinpath('feedstat.json')
f2mdblock = f2mdbdir.joinpath('.feeds.lock')

def bootstrapjson(p):
    if not p.exists():
        with p.open('w') as fp: fp.write('{}')

f2mdbdir.mkdir(exist_ok=True)
bootstrapjson(f2mdb)
bootstrapjson(f2mrc)
