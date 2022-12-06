from flask import Flask, jsonify, render_template
from data_loader import load_data, get_current_weather

app = Flask(__name__, template_folder='./template', static_folder="./static")

data = load_data()
current_data = get_current_weather()

@app.route('/', methods=['GET'])
def current_prediction():
    return render_template("index.html", data=current_data)

@app.route("/future-predictions-1", methods=["GET"])
def future_predictions():
    return render_template("future_forecast.html", data=data[0])

@app.route("/future-predictions-2", methods=["GET"])
def future_predictions_2():
    return render_template("future_forecasting_2.html", data=data[1])

@app.route("/future-predictions-3", methods=["GET"])
def future_predictions_3():
    return render_template("future_forecasting_3.html", data=data[2])

if __name__ == "__main__": 
    app.run()