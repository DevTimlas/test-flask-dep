from flask import Flask

app = Flask("hello")

@app.route("/")
def hello():
	return "Hello Geeks!! from Google Colab"

if __name__ == "__main__":
	app.run()

