from flask_restful import Resource
import pyshorteners

def short_link(link):
    short = pyshorteners.Shortener()
    return short.tinyurl.short(link)

class Link(Resource):
    def post(self):
        pass