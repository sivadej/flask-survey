from flask import Flask, session, redirect, render_template, request, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret squirrel'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

MOVIES = {'Amadeus', 'Chicken Run', 'Dances With Wolves'}


@app.route('/')
def start():
    session['count'] = 0
    return 'new counter started'


@app.route('/old-home-page')
def redirect_to_home():
    """redirects to new homepage"""
    flash('that page has moved. you are now at the new home page')
    return redirect('/movies')


@app.route('/movies')
def show_all_movies():
    """Show list of all movies in fake DB"""
    return render_template('movies.html', movies=MOVIES)

# use redirect for POST to GET
@app.route('/movies/new', methods=["POST"])
def add_movie():
    title = request.form['title']
    # pretend db
    if title in MOVIES:
        flash('movie already exists.', 'error')
    elif title == '':
        flash('cannot be blank')
    else:
        MOVIES.add(title)
        flash('movie successfully added!', 'success')
    return redirect('/movies')

@app.route('/json')
def json():
    return jsonify({"title":"parasite","directors":{"main_director":"bong joon ho","co_director":"bomby k"}})

@app.route('/movies/json')
def get_movies_json():
    return jsonify(list(MOVIES))

if __name__ == '__main__':
    app.run(debug=True)
