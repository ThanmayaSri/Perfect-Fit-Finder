from flask import Flask, render_template, request

# --- Real brand size charts ---
size_chart = {
    "H&M": [
        {"size": "S", "waist_min": 26, "waist_max": 27, "hip_min": 36, "hip_max": 37},
        {"size": "M", "waist_min": 28, "waist_max": 29, "hip_min": 38, "hip_max": 39},
        {"size": "L", "waist_min": 30, "waist_max": 31, "hip_min": 40, "hip_max": 41},
    ],
    "Zara": [
        {"size": "S", "waist_min": 25, "waist_max": 26, "hip_min": 35, "hip_max": 36},
        {"size": "M", "waist_min": 27, "waist_max": 28, "hip_min": 37, "hip_max": 38},
        {"size": "L", "waist_min": 29, "waist_max": 30, "hip_min": 39, "hip_max": 40},
    ],
    "Forever 21": [
        {"size": "S", "waist_min": 24, "waist_max": 25.5, "hip_min": 34, "hip_max": 35.5},
        {"size": "M", "waist_min": 26, "waist_max": 27.5, "hip_min": 36, "hip_max": 37.5},
        {"size": "L", "waist_min": 28, "waist_max": 30, "hip_min": 38, "hip_max": 40},
    ],
    "Levi's": [
        {"size": "S", "waist_min": 26, "waist_max": 28, "hip_min": 34, "hip_max": 36},
        {"size": "M", "waist_min": 29, "waist_max": 31, "hip_min": 37, "hip_max": 39},
        {"size": "L", "waist_min": 32, "waist_max": 34, "hip_min": 40, "hip_max": 42},
    ],
    "American Eagle": [
        {"size": "S", "waist_min": 26, "waist_max": 28, "hip_min": 36, "hip_max": 38},
        {"size": "M", "waist_min": 29, "waist_max": 31, "hip_min": 39, "hip_max": 41},
        {"size": "L", "waist_min": 32, "waist_max": 34, "hip_min": 42, "hip_max": 44},
    ],
    "Shein": [
        {"size": "S", "waist_min": 25, "waist_max": 26.5, "hip_min": 35, "hip_max": 36.5},
        {"size": "M", "waist_min": 27, "waist_max": 28.5, "hip_min": 37, "hip_max": 38.5},
        {"size": "L", "waist_min": 29, "waist_max": 31, "hip_min": 39, "hip_max": 41},
    ],
    "Victoria's Secret": [
        {"size": "S", "waist_min": 24, "waist_max": 26, "hip_min": 34, "hip_max": 36},
        {"size": "M", "waist_min": 27, "waist_max": 29, "hip_min": 37, "hip_max": 39},
        {"size": "L", "waist_min": 30, "waist_max": 32, "hip_min": 40, "hip_max": 42},
    ],
    "Abercrombie & Fitch": [
        {"size": "S", "waist_min": 25, "waist_max": 27, "hip_min": 35, "hip_max": 37},
        {"size": "M", "waist_min": 28, "waist_max": 30, "hip_min": 38, "hip_max": 40},
        {"size": "L", "waist_min": 31, "waist_max": 33, "hip_min": 41, "hip_max": 43},
    ],
    "Old Navy": [
        {"size": "S", "waist_min": 26, "waist_max": 28, "hip_min": 36, "hip_max": 38},
        {"size": "M", "waist_min": 29, "waist_max": 31, "hip_min": 39, "hip_max": 41},
        {"size": "L", "waist_min": 32, "waist_max": 34, "hip_min": 42, "hip_max": 44},
    ]
}

# --- Estimate body measurements from height and weight ---
def estimate_body_measurements(height, weight):
    # Basic estimation formula (can be refined later)
    waist = (weight / height) * 70
    hip = (weight / height) * 100
    return waist, hip

# --- Flask App Setup ---
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', size_chart=size_chart)

@app.route('/get-size', methods=['POST'])
def get_size():
    height_cm = float(request.form['height'])
    height = height_cm / 2.54
    weight = float(request.form['weight'])
    brand = request.form['brand']

    waist, hip = estimate_body_measurements(height, weight)

    closest_size = "Not Found"
    min_diff = float('inf')  # Start with a large number

    for entry in size_chart[brand]:
        waist_center = (entry['waist_min'] + entry['waist_max']) / 2
        hip_center = (entry['hip_min'] + entry['hip_max']) / 2

        waist_diff = abs(waist - waist_center)
        hip_diff = abs(hip - hip_center)
        total_diff = waist_diff + hip_diff

        if total_diff < min_diff:
            min_diff = total_diff
            closest_size = entry['size']


    return render_template('result.html', size=closest_size)

if __name__ == '__main__':
    app.run(debug=True)
