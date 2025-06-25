from flask import Flask, render_template, request
from fuzzy_model import clasificar_calidad

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = ""
    if request.method == "POST":
        acidez = float(request.form['acidez'])
        cafeina = float(request.form['cafeina'])
        humedad = float(request.form['humedad'])
        aroma = float(request.form['aroma'])
        resultado = clasificar_calidad(acidez, cafeina, humedad, aroma)
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
