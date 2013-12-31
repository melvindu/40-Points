from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from fortypoints.template import templated
from fortypoints.games import create_game, constants as GAME
from fortypoints.games.forms import NewGameForm
from fortypoints.users import get_user

game = Blueprint('games', __name__, template_folder='templates/games')


@game.route('/play/<int:game_id>')
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
      usernames = [field.data for field in form.players.entries] + [current_user.name]
      users = []
      for username in usernames:
        user = get_user(name=username)
        if not user:
          flash('Invalid User {username}'.format(username=username), 'danger')
          return render_template('games/new.html', form=form)
        users.append(user)

      if len(users) < GAME.MIN_PLAYERS:
        flash('Must invite at least {min} players'.format(min=GAME.MIN_PLAYERS), 'danger')
        return render_template('games/new.html', form=form)
      game = create_game(users)
      return redirect(url_for('games.play', game_id=game.id))
  return render_template('games/new.html', form=form)
