#!/usr/bin/env python
import os
from flask import Flask, abort, request, jsonify, g, url_for

from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

import requests
import json
import random
from tinydb import TinyDB, Query
# initialization
app = Flask(__name__)

db = TinyDB('db.json')
User = Query()

@app.route('/', methods=['POST'])
def new_user():
    username = request.json.get('username')
    interest = request.json.get('interest')
    splitint = interest.split(',')
    lenspl = len(splitint)
    newdict = dict()
    for lens in range(lenspl):
        reqgif = requests.get('https://api.giphy.com/v1/gifs/search?api_key=ee58ff1d10c54fd29ddb0388126c2bcd&q={}&limit=25&offset=0&rating=G&lang=en'.format(splitint[lens]))
        gifjs = (reqgif.json())
        randch = random.choice(gifjs['data'])
        newdict.update({lens : dict({'name' : splitint[lens], 'gif' : randch['images']['fixed_width']['url']})})


    db.insert({'username' : username, 'interest' : newdict})

    #return (jsonify({'username': username, 'interest' : dict({'name' :interest, 'gif': })}), 201)


@app.route('/all')
def get_user():
    #for item in db:
    #    return(item)
    with open('db.json', 'r') as dbrd:
        dbread = (dbrd.read())

    #return(dbread)
    return(dbread)

@app.route('/getinterests')
#@auth.login_required
def getinterests():
    return jsonify({'data': 'Hello, {}! interest: {}'.format(g.user.username, g.user.interest)})


if __name__ == '__main__':
    if not os.path.exists('db.json'):
        db.create_all()
    app.run(debug=True)
