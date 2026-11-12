"""Local smoke tests using Flask test client (no HTTP server needed).
Covers: lecturer login, create session, student login, mark attendance.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'backend')))

from index import app, init_db, _sqlite_db_path
import sqlite3

app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

# Ensure DB initialized
with app.app_context():
    init_db()

client = app.test_client()

# Lecturer login
r = client.post('/login/lecturer', data={'username':'lecturer1','password':'password'}, follow_redirects=True)
print('Lecturer login:', r.status_code)

# Create a session (token mode, no geofence needed)
r = client.post('/session/create', data={'course_name':'Smoke Test Course','host':'Test Host',
                                         'duration':'30','grace':'5','attendance_mode':'token','strict_mode':'0'},
                follow_redirects=True)
print('Create session:', r.status_code)


# Read latest session (token and id)
con = sqlite3.connect(_sqlite_db_path())
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute('SELECT id, token FROM sessions ORDER BY id DESC LIMIT 1')
row = cur.fetchone()
if row:
    session_id = row['id']
    token = row['token']
    print('Found session:', session_id, token)
else:
    print('No session found')
    token = None

# Student login and session check
client2 = app.test_client()
r = client2.post('/login/student', data={'identifier':'UB1001','password':'password'}, follow_redirects=True)
print('Student login:', r.status_code)
if token:
    r_check = client2.post('/session/check', json={'token': token, 'lat':6.317, 'lon':5.631})
    print('Session check:', r_check.status_code, r_check.get_json())
    r = client2.post('/session/mark', json={'token': token, 'lat':6.317, 'lon':5.631})
    try:
        print('Mark attendance response:', r.status_code, r.get_json())
    except Exception as e:
        print('Failed to parse response', e)

    # Now terminate the session and try again
    r_term = client.post(f'/session/{session_id}/terminate', follow_redirects=True)
    print('Terminate session:', r_term.status_code)
    r_check2 = client2.post('/session/check', json={'token': token, 'lat':6.317, 'lon':5.631})
    print('Session check after terminate:', r_check2.status_code, r_check2.get_json())
    r2 = client2.post('/session/mark', json={'token': token, 'lat':6.317, 'lon':5.631})
    print('Mark after terminate:', r2.status_code, r2.get_json())
else:
    print('Skipping mark: no token')
