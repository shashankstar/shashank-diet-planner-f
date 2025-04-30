from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Sample vegetarian food data
food_data = pd.DataFrame([
    {"Food": "Oats", "Calories": 389, "Protein": 16.9, "Carbs": 66.3, "Fat": 6.9},
    {"Food": "Paneer", "Calories": 265, "Protein": 18.3, "Carbs": 1.2, "Fat": 20.8},
    {"Food": "Brown Rice", "Calories": 111, "Protein": 2.6, "Carbs": 23, "Fat": 0.9},
    {"Food": "Moong Dal", "Calories": 347, "Protein": 24.5, "Carbs": 59.9, "Fat": 1.2},
    {"Food": "Boiled Potato", "Calories": 87, "Protein": 1.9, "Carbs": 20.1, "Fat": 0.1},
    {"Food": "Curd", "Calories": 61, "Protein": 3.5, "Carbs": 4.7, "Fat": 3.3},
    {"Food": "Almonds", "Calories": 579, "Protein": 21.2, "Carbs": 21.6, "Fat": 49.9},
    {"Food": "Roti", "Calories": 104, "Protein": 2.7, "Carbs": 18, "Fat": 3}
])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    calorie_target = int(request.form["calories"])
    goal = request.form["goal"]

    food_data["Grams"] = (calorie_target / food_data["Calories"]) * 100 / len(food_data)
    food_data["Calories_Total"] = (food_data["Calories"] * food_data["Grams"]) / 100
    food_data["Protein_Total"] = (food_data["Protein"] * food_data["Grams"]) / 100
    food_data["Carbs_Total"] = (food_data["Carbs"] * food_data["Grams"]) / 100
    food_data["Fat_Total"] = (food_data["Fat"] * food_data["Grams"]) / 100

    total_macro = {
        "Calories": food_data["Calories_Total"].sum(),
        "Protein": food_data["Protein_Total"].sum(),
        "Carbs": food_data["Carbs_Total"].sum(),
        "Fat": food_data["Fat_Total"].sum()
    }

    return render_template("result.html", food_data=food_data.round(1).to_dict(orient="records"), total_macro=total_macro, goal=goal, calories=calorie_target)

if __name__ == "__main__":
    app.run(debug=True)
