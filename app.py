from flask import Flask, redirect, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def landing_page():
    return redirect('/home')

@app.route('/home')
def home_page():
    return render_template("index.html")

@app.route('/prediction', methods=['POST'])
def prediction():
    data = request.get_json()
    for slider_name, slider_value in data.items():
        print(f"Slider '{slider_name}' value: {slider_value}")
    return jsonify({'message': 'Slider values received successfully'})


if __name__ == "__main__":
    app.run()
