from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///video_games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/top-games')
def top_games():
    return render_template('top_games.html')


@app.route('/collections', methods=['GET'])
def collections():
    games = Game.query.all()
    return render_template('collections.html', games=games)

@app.route('/add', methods=['POST'])
def add_game():
    new_game = Game(
        title=request.form['title'],
        year=int(request.form['year'])
    )
    db.session.add(new_game)
    db.session.commit()
    return redirect(url_for('collections'))

# Route: Delete a game
@app.route('/delete/<int:game_id>', methods=['POST'])
def delete_game(game_id):
    game = Game.query.get(game_id)
    if game:
        db.session.delete(game)
        db.session.commit()
    return redirect(url_for('collections'))

# Route: Edit a game
@app.route('/edit/<int:game_id>', methods=['GET', 'POST'])
def edit_game(game_id):
    game = Game.query.get(game_id)
    if request.method == 'POST':
        if game:
            game.title = request.form['title']
            game.year = int(request.form['year'])
            db.session.commit()
        return redirect(url_for('collections'))
    return render_template('edit.html', game=game)

@app.route('/login')
def login():
    return render_template('login.html')



if __name__ == '__main__':
    app.run(host="127.0.0.2",
            port=5000,
            debug=True)