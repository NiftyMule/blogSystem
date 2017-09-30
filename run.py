import bottle

from bottle import route

@bottle.route('/')
def hello():
    return "Hello World!"

app = application = bottle.default_app()
