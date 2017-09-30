import bottle

from bottle import route

@route('/')
def hello():
    return "Hello World!"

@route('/greet')
def hello2():
    return "Greeting!"

# from website: https://community.runabove.com/kb/en/development/how-to-run-bottle-uwsgi-nginx.html
# Run bottle internal test server when invoked directly ie: non-uxsgi mode
if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=8080)
# Run bottle in application mode. Required in order to get the application working with uWSGI!
else:
    app = application = bottle.default_app()
