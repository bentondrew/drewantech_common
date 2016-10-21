from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
  import drewantech_common
  return 'drewantech_common version installed: {}'.format(drewantech_common.__version__)