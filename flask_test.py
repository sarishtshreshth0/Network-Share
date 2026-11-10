from flask import Flask


app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello from the Flask!!!'


@app.route('/about')
def about():
    return 'This is the about section'

@app.route('/test')
def test():
    return 'This is test section of the proxy-server'


app.run(host = '127.0.0.1' , port = 5000)