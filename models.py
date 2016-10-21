from google.appengine.ext import ndb


class Musics(ndb.Model):
    ky_number = ndb.StringProperty(indexed=True)
    tj_number = ndb.StringProperty(indexed=True)
    title = ndb.StringProperty(indexed=True)
    singer = ndb.StringProperty(indexed=True)
    composer = ndb.StringProperty()
    lyrics = ndb.StringProperty()
    updated = ndb.DateProperty(indexed=True)