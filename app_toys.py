from flask import Flask, render_template, request, url_for, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from flask_modus3 import Modus
from toy import Toy

app = Flask(__name__)
modus = Modus(app)

# enable toolbar in debug mode only. In production, set to False to disable toolbar.
app.debug = False

# set a secret key to enable Flask session cookies
app.config['SECRET_KEY'] = 'yo'

toolbar = DebugToolbarExtension(app)

duplo = Toy(name='duplo')
lego = Toy(name='lego')
knex = Toy(name='knex')

toys = [duplo,lego,knex]

@app.route('/toys', methods=['GET','POST'])
def toys_home():
    if request.method == 'POST':
        # get value of input field with attribute name of toy-name
        toy_name = request.form['toy-name']
        toys.append(Toy(toy_name))
        print (f"{toy_name} added to toys list")
        flash("flash! ah")
        # respond with redirect to toys index route, which is this toys_home GET
        return redirect(url_for('toys_home'))
    # just return the html with args when the method is GET
    return render_template('toys.html', toys=toys)

@app.route('/toys/new')
def new_toy():
    return render_template('toy_form.html')

@app.route('/toys/<int:id>', methods=['GET','PATCH', 'DELETE'])
def show_toy(id):
    found_toy = next(toy for toy in toys if toy.id == id)

    # if updating...
    if request.method == "PATCH":
        found_toy.name = request.form['toy-name']
        return redirect(url_for('toys_home'))

    # if deleting...
    if request.method == "DELETE":
        toys.remove(found_toy)
        return redirect(url_for('toys_home'))

    return render_template('show_toy.html', toy=found_toy, max=len(toys))

@app.route('/toys/<int:id>/edit')
def edit_toy(id):
    found_toy = next(toy for toy in toys if toy.id == id)
    return render_template('edit_toy.html', toy=found_toy)

@app.route('/')
def poop():
    return render_template('index.html', name='bomby')

@app.route('/title')
def title():
    return render_template('title.html')

@app.route('/myform')
def myform():
    return render_template('form.html')

@app.route('/showdata')
def show_data():
    text = request.args.get('input1')
    return f"you entered {text}"