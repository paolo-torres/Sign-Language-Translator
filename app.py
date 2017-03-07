import sys, thread, time
sys.path.insert(0, "./lib")
sys.path.insert(0, "./lib/x64")
import Leap
from classifier import clf
from flask import Flask, render_template, jsonify, request, json
from hand_data import get_hand_position
from lib import Leap
import pickle
import random
import redis
import os

app = Flask(__name__)

controller = Leap.Controller()
controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

past_symbol = 'a'
prev_prediction = None
text = []

r = redis.StrictRedis(host = 'localhost', port = 6379, db = 0)

@app.route('/')
def tutorial():
	return render_template('tutorial.html')

@app.route('/videochat')
def video():
	return render_template('videochat.html')

@app.route('/current')
def current_symbol():
	global past_symbol
	global prev_prediction
	hand_pos = get_hand_position(controller)
	if not hand_pos:
		new = past_symbol != ' '
		past_symbol = ' '
	features = [v for k, v in hand_pos.iteritems()]
	prediction = ''.join(clf.predict(features))
	if prediction != prev_prediction:
		text.append(prediction)
		prev_prediction = prediction

@app.route('/wordLog')
def word():
	return text[len(text)-1]

if __name__ == '__main__':
    app.run(debug = True)