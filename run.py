#coding=utf-8
from bottle import route, get, run, post, request, redirect, static_file, response, request
import bottle
import requests
import pymysql
import os
import re
import time

abs_path = os.path.dirname(os.path.abspath(__file__))

#---------------------------------------------------------------------------
# load and render web pages

def load_template(filename):
    path = "templates/" + filename + ".html"
    file = open(path, 'r')
    text = ""
    for line in file:
        text+= line
    file.close()
    return text

def render(template, **kwargs):
    template = template.format(**kwargs)
    return template

def load_and_render(template, **kwargs):
    loaded_template = load_template(template)
    rendered_template = render(loaded_template, **kwargs)
    return rendered_template

#---------------------------------------------------------------------------
# API for database sql execution

def execute_sql(sql_str):
    ppp(sql_str)
    db = pymysql.connect('localhost', 'root', 'password', 'blog', charset = 'utf8')
    cursor = db.cursor()
    try:
        cursor.execute(sql_str)
        db.commit()
    except:
        db.rollback()
    db.close()

def sql_with_result(sql_str):
    db = pymysql.connect('localhost', 'root', 'password', 'blog', charset = 'utf8')
    cursor = db.cursor()
    try:
        cursor.execute(sql_str)
        results = cursor.fetchall()
    except:
        print ("Error: unable to fetch data")
    db.close()
    if results:
        return results
    else:
        return None

#---------------------------------------------------------------------------
# enable picture, css, javascript, font

@route('/img/<picture:path>')
def d_img(picture):
    return static_file(picture, root = 'img/')

@route('/css/<css:path>')
def d_css(css):
    return static_file(css, root = 'css/')

@route('/js/<js:path>')
def d_js(js):
    return static_file(js, root = 'js/')

@route('fonts/<font:path>')
def d_font(font):
    return static_file(font, root = 'fonts/')

#---------------------------------------------------------------------------
# debug tools

def ppp(str):
    print(str)

#---------------------------------------------------------------------------
@route('/')
@route('/home')
def home():
    rendered_page = load_and_render("header")
    sql = """SELECT username, content FROM post
                ORDER BY post_id DESC
                LIMIT 10;"""
    fetched_result = sql_with_result(sql)
    if fetched_result is not None:
        for row in fetched_result:
            username = row[0]
            content = row[1]
            ppp(username)
            ppp(content)
            rendered_page += load_and_render("post", username = username, content = content)
    rendered_page += load_and_render("footer")
    return rendered_page

@post('/')
def commit_content():
    username = request.forms.getunicode('username')
    content = request.forms.getunicode('content')
    ip_address = request.environ.get('REMOTE_ADDR')
    submission_time = time.strftime("%Y-%m-%d", time.gmtime())
    ppp(username)
    ppp(content)
    sql = """INSERT INTO post (username, content, ip_address, submission_time)
                VALUES (\'{username}\', \'{content}\', \'{ip_address}\', \'{submission_time}\');
                """.format(username = username, content = content, ip_address = ip_address, submission_time = submission_time)
    execute_sql(sql)
    redirect("/")

#---------------------------------------------------------------------------
# from website: https://community.runabove.com/kb/en/development/how-to-run-bottle-uwsgi-nginx.html
# Run bottle internal test server when invoked directly ie: non-uxsgi mode
if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=8080, debug = False)
# Run bottle in application mode. Required in order to get the application working with uWSGI!
else:
    app = application = bottle.default_app()
