from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from fortypoints.template import templated
from fortypoints import games
from fortypoints.games.forms import NewGameForm

game = Blueprint('games', __name__, template_folder='templates/games')


@game.route('/new', methods=['GET', 'POST'])
@login_required
def new():
  """
  New Game Form.
  """
  form = NewGameForm(request.form)
  # make sure data are valid, but doesn't validate password is right
  if form.validate_on_submit():
    pass
  flash('Wrong email or password', 'danger')
  return render_template('users/login.html', form=form)
