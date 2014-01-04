import math

from fortypoints import app

@app.template_filter('log')
def log(value, base=2):
  return math.log(value, base)
