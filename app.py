from flask import Flask

app = Flask(__name__)

@app.route("/")
def home_view():
<<<<<<< HEAD
		return "<h1> hello, world! </h1>"
app.run()
=======
		return "<h1> hello, world! ... Testing Heroku </h1>"

>>>>>>> 76659c0d8a9646e07512a84f61aec633122b0151
