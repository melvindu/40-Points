from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from fortypoints.template import templated
from fortypoints.games import create_game
from fortypoints.users import get_user
from fortypoints.games.forms import NewGameForm

game = Blueprint('games', __name__, template_folder='templates/games')


@game.route('/play/<int:game_id>', methods=['GET', 'POST'])
@login_required
def play(game_id):
  """
  Play a game.
  """
  return render_template('games/play.html')
  

@game.route('/new', methods=['GET', 'POST'])
@login_required
def new():
  """
  New Game Form.
  """
  form = NewGameForm(request.form)
  # make sure data are valid, but doesn't validate password is right
  if form.validate_on_submit():
    if form.add_player.data:
      form.players.append_entry()
      return render_template('games/new.html', form=form)
    else:
      users = filter(None, form.players.entries.data)
      users = [get_user(user) for user in users]
      game = create_game(users)
      return redirect(url_for('games.'))
  flash('Invalid User', 'error')
  return render_template('games/new.html', form=form)
