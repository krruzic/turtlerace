from pprint import pprint

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

from utils import *
from models import Bet

RPC_URL = "http://127.0.0.1:8070/json_rpc"
WALLET = TrtlServer(RPC_URL)

app = Flask(__name__, static_url_path='/static')
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY=os.environ.get("SECRET_KEY"),
    WTF_CSRF_SECRET_KEY=os.environ.get("WTF_CSRF_SECRET_KEY"),
    SQLALCHEMY_DATABASE_URI='sqlite:///trtlrace.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
))
db = SQLAlchemy(app)

@app.route('/')
def test_route():
    blocknum = "hello"
    return render_template('home.html', blocknum=blocknum)

@app.route('/get_pids')
def get_pids():
    addr = request.args.get('address')
    if len(addr) == 99:
        pids = gen_paymentids(addr,7)
    return json.dumps({'status': 'OK',
        'pids': pids})

# @app.route

if __name__ == "__main__":
    app.run()