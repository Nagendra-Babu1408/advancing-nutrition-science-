from flask import Flask, render_template, request, jsonify
import io
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)

# ✅ Initialize Gemini AI Model
genai.configure(api_key="AIzaSyDnAlZ4nMrTcwPEFXJen7iEuavGmLJuMBY")
model = genai.GenerativeModel("gemini-2.0-flash")

@app.route("/")
def index():
    return render_template("index.html")

# ✅ BMI Calculation API
@app.route("/calculate_bmi", methods=["POST"])
def calculate_bmi():
    data = request.json
    weight = float(data.get("weight", 0))
    height = float(data.get("height", 0)) / 100  # Convert to meters
    age = int(data.get("age", 0))
    activity_level = data.get("activity_level", "sedentary").lower()

    if not weight or not height or not age:
        return jsonify({"error": "All BMI fields are required"}), 400

    bmi = weight / (height ** 2)

    # ✅ Health Status
    if bmi < 18.5:
        health_status = "Underweight"
        advice = "Increase calorie intake with protein and healthy fats."
    elif 18.5 <= bmi < 24.9:
        health_status = "Normal weight"
        advice = "Maintain a balanced diet and regular exercise."
    elif 25 <= bmi < 29.9:
        health_status = "Overweight"
        advice = "Focus on portion control, fiber-rich foods, and exercise."
    else:
        health_status = "Obese"
        advice = "A structured diet and workout plan is recommended."

    activity_multiplier = {"sedentary": 1.2, "moderate": 1.5, "active": 1.8}
    calories = weight * 24 * activity_multiplier.get(activity_level, 1.2)

    return jsonify({
        "bmi": round(bmi, 2),
        "health_status": health_status,
        "advice": advice,
        "calories": round(calories, 0)
    })

# ✅ Text Analysis API
@app.route("/analyze_text", methods=["POST"])
def analyze_text():
    data = request.json
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    response = model.generate_content(prompt)
    return jsonify({"response": response.text})

# ✅ Image Analysis API
@app.route("/analyze_image", methods=["POST"])
def analyze_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]
    image = Image.open(image_file)

    prompt = "Analyze this dish and provide nutrition details, including calories, macronutrients, and health benefits."
    response = model.generate_content([prompt, image])

    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(debug=True)
