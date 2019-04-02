import cv2
import sys
import flask
import jsonpickle
import numpy as np
from flask import Flask, request, Response, session, redirect, url_for
import json
import requests
payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
r = requests.get('https://httpbin.org/get', params=payload)
print(r.url)
