import sqlite3
from flask import Flask, request
from noople import db

app = Flask(__name__)


def insert_query(q=None):
    """Insert a row into the query table

    Argument:
    q: the search text to be inserted
    """
    if not q:
        return
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()

    # Insert a row of data
    cursor.execute("INSERT INTO query VALUES (NULL, '" + q + "');")

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    conn.close()


def select_recent_queries(max_rows=5):
    """Select recent searches from the query table

    Keyword argument:
    max_rows -- the number of rows to return
    """
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()

    # Insert a row of data
    cursor.execute("""SELECT search
                      FROM query
                      ORDER BY id DESC
                      LIMIT """ + max_rows + ";")

    results = cursor.fetchall()

    # We can also close the connection if we are done with it.
    conn.close()

    return results


@app.route('/')
def search():
    """Display search form and search results

    Optional GET parameter, q -- contains search string
    """
    # check for GET data
    search_term = ''
    recent_searches = ''
    q = request.args.get("q", None)
    if q:
        search_term = '<p>You searched for: ' + q + '</p>'
        search_term += '<p>No results found.</p>'
        insert_query(q)

    recent_queries = select_recent_queries()
    if len(recent_queries) > 1:
        recent_searches = '<p>Recent searches:</p><ul>'
        for query in recent_queries:
            recent_searches += '<li><a href="/?q=' + query[0] + '">'
            recent_searches += query[0]
            recent_searches += '</a></li>'
        recent_searches += '</ul>'

    return '''<h1>noople</h1>
              <form action="/" method="GET">
              <input type="text" name="q">
              <input type="submit" value="search">
              </form>''' + search_term + recent_searches


@app.route('/init/')
def init():
    """Initialize database

    Drops and recreates the query table
    """
    db.init_db()
    db.get_db().execute('SELECT * FROM query')
    return 'Database initialized.'
