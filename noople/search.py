"""Noople: a trivial (and terrible) search engine

Noople provides a search interface, but no search results.
It is useful for demonstrating certain aspects of the
Python Flask framework (routes, GET parameters) as well as
common security vulnerabilities, such as XSS and SQLi.
"""

import sqlite3
from flask import Flask, current_app, request, escape

app = Flask(__name__)

# Change the following to DuckDuckNope for enhanced privacy
SITE_NAME = 'noople'
DB_PATH = 'instance/database.db'


def check_db():
    """Creates a database if none is present."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM query LIMIT 1;")
        conn.close()
    except:
        init_db()


def insert_query(search_query=None):
    """Insert a row into the query table

    Argument:
    q: the search text to be inserted
    """
    if not search_query:
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert a row of data
    cursor.execute("INSERT INTO query VALUES (NULL, ?);", (search_query,))

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    conn.close()


def select_recent_queries(max_rows=5):
    """Select recent searches from the query table

    Keyword argument:
    max_rows -- the number of rows to return
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert a row of data
    cursor.execute("""SELECT search
                      FROM query
                      ORDER BY id DESC
                      LIMIT """ + str(max_rows) + ";")

    results = cursor.fetchall()

    # We can also close the connection if we are done with it.
    conn.close()

    return results


def get_search_results_html(search_query=None):
    """Return search results, formatted as HTML"""

    if search_query:
        # Insert the search term into the database
        insert_query(search_query)

        # Format results as HTML
        search_results = f'<p>You searched for: {escape(search_query)}</p>'
        search_results += '<p>No results found.</p>'
        return search_results

    # No search term specified, so return an empty string
    return ""


def get_recent_searches_html():
    """Return a formatted list of recent searches"""

    # Get recent queries from the database
    recent_queries = select_recent_queries()

    # If results were returned, create an HTML list
    if recent_queries:
        recent_searches = '<p>Recent searches:</p><ul>'
        for query in recent_queries:
            recent_searches += f'<li><a href="/?q={escape(query[0])}">'
            recent_searches += f'{escape(query[0])}'
            recent_searches += '</a></li>'
        recent_searches += '</ul>'
        return recent_searches

    # Otherwise, return a blank string
    return ""


def html_wrapper(content):
    """Wraps provided string content in an HTML page"""

    header = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>''' + SITE_NAME + '''</title>
</head>
<body>
'''

    footer = '''
</body>
</html>'''
    return header + content + footer


@app.route('/')
def search():
    """Display search form and search results

    Optional GET parameter, q -- contains search string
    """
    # Check for database tables
    check_db()
    # Check for GET data
    search_query = request.args.get("q", None)
    # Format search results as HTML
    search_results = get_search_results_html(search_query)
    # Format recent searches as HTML
    recent_searches = get_recent_searches_html()

    return html_wrapper('<h1>' + SITE_NAME + '''</h1>
    <form action="/" method="GET">
        <input type="text" name="q">
        <input type="submit" value="search">
    </form>''' + search_results + recent_searches)


@app.route('/init/')
def init():
    """init route

    Calls init and returns user to the main page.
    """
    try:
        init_db()
    except:
        return html_wrapper('''<h1>An error occurred.</h1>
                  <p>An error occurred while initializing
                  the database. Try again?</p>''')

    return html_wrapper('''<h1>Database initialized.</h1>
              <p>Return to the <a href="/">main page</a>.</p>''')


def init_db():
    """Initialize database

    Drops and recreates the query table
    """
    # Open connection to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Open the schema file and execute its SQL code
    with current_app.open_resource('schema.sql') as db_schema:
        cursor.executescript(db_schema.read().decode('utf8'))

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    conn.close()
