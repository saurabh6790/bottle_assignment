import bottle # https://bottlepy.org/docs/dev/tutorial_app.html
import sqlite3
import json

db = sqlite3.connect(':memory:')
db.row_factory = sqlite3.Row
db.executescript('''
    BEGIN TRANSACTION;
    CREATE TABLE wombat(id integer primary key, name varchar(128), dob date);
    INSERT INTO wombat VALUES(1,'Alice','1865-11-26');
    INSERT INTO wombat VALUES(2,'Queen','1951-07-26');
    INSERT INTO wombat VALUES(3,'Johnny','2010-03-05');
    COMMIT;
''')

@bottle.get('/')
def index():
    bottle.response.content_type = 'text/plain'
    return "Inspire Candidate Exercise"

@bottle.get('/wombats')
def get_wombats():
    bottle.response.content_type = 'application/json'
    cur = db.execute('SELECT * FROM wombat')
    return { 'wombats': [dict(row) for row in cur.fetchall()] }

@bottle.post('/wombats')
def post_wombats():
    bottle.response.content_type = 'application/json'

    name = bottle.request.forms.get('name')
    if name is None:
        return bottle.HTTPResponse(status=400, body="Missing parameter: name")   

    dob = bottle.request.forms.get('dob')
    if dob is None:
        return bottle.HTTPResponse(status=400, body= "Missing parameter: dob")   

    cur = db.execute('INSERT INTO wombat(name, dob) VALUES(?,?)', (name, dob))
    return { 'id': cur.lastrowid, 'name': name, 'dob': dob }

@bottle.error(404)
def error404(error):
    bottle.response.content_type = 'text/plain'
    return "Not Found"

@bottle.error(405)
def error405(error):
    bottle.response.content_type = 'text/plain'
    return "Method Not Allowed"


if __name__ == '__main__':
    import sys
    hostname = 'localhost'
    port = '8080'
    if len(sys.argv) >= 2:
        hostname = sys.argv[1]
    if len(sys.argv) >= 3:
        port = sys.argv[2]

    bottle.debug()
    bottle.run(host=hostname, port=int(port), reloader=True)
