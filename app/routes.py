from app import app
from flask import request

@app.route('/')
def index():    return "Hello, World!"# -*- coding: utf-8 -*-

@app.route('/postJson', methods=['POST'])
def post():
    content = request.get_json()
    print(content)
    return 'JSON POSTED SUCCESSFULLY ...'
