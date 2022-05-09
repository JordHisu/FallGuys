import queue
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    return "<marquee>Fall Guys is Running</marquee>"

@app.route('/createuser', methods=['POST'])
def createuser():
    # data = request.get_json()
    return { 
        'status': 'OK',
        'userid': '1'
    }

@app.route('/login', methods=['POST'])
def login():
    # data = request.get_json()
    return { 
        'status': 'OK',
        'token' : '2'
    }

@app.route('/senddata', methods=['POST'])
def senddata():
    # data = request.get_json()
    return { 
        'status': 'OK'
    }

@app.route('/sendconfig', methods=['POST'])
def sendconfig():
    # data = request.get_json()
    return { 
        'status': 'OK'
    }

@app.route('/sendnotif', methods=['POST'])
def sendnotif():
    # data = request.get_json()
    return { 
        'status': 'OK'
    }

@app.route('/getconfig', methods=['GET'])
def getconfig():
    # data = request.get_json()
    return { 
        'status': 'OK',
        'userlocpp': 5,
        'hrtbldpp': 7,
        'heartrange': [40, 200],
        'oxygenrange': 85
    }

@app.route('/getnotif', methods=['GET'])
def getnotif():
    # data = request.get_json()
    return { 
        'status': 'OK',
        'notifications': [{ 'message' : 'o veio morreu :(' }]
    }


@app.route('/getdata', methods=['GET'])
def getdata():
    # data = request.get_json()
    return { 
        'status': 'OK',
        'bloodoxygen': [99, 95, 97, 80, 96, 98, 100],
        'heartbeat': [120, 118, 116, 110, 105, 110],
        'livelocation': [(-25.459879140972372, -49.30012822151185), (-25.459976010148413, -49.30008530616761)],
        'pressure': [10000, 10005, 9999]
    }
