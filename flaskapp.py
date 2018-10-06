from sps import predict

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/<name>")
def predict_stats(name=None):
    if name!=None:
        try:
            prediction = predict(name)
            return render_template("index.html", prediction=prediction)

        except(RuntimeError, TypeError, NameError, KeyError, ValueError, IndexError):
            return render_template("wrong.html")
    else:
        return render_template("start.html")

if __name__ == "__main__":
    app.run()