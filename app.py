# Import Flask
from flask import Flask,render_template,request,jsonify

# Import necessary classes and functions from your custom modules
from src.pipeline.prediction_pipeline import PredictionPipeline,CustomClass

# Create Flask instance
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def prediction_data():
    # Handle GET request to render the home page
    if request.method == "GET":
        return render_template("home.html")
    else:
        # Handle POST request to process form data and make predictions

        # Create an instance of CustomClass with form data
        data = CustomClass(
            age = int(request.form.get("age")),
            workclass= int(request.form.get("workclass")),
            education_num=int(request.form.get("education_num")),
            marital_status=int(request.form.get("marital_status")),
            occupation=int(request.form.get("occupation")),
            relationship=int(request.form.get("relationship")),
            race=int(request.form.get("race")),
            sex=int(request.form.get("sex")),
            capital_gain=int(request.form.get("capital_gain")),
            capital_loss=int(request.form.get("capital_loss")),
            hours_per_week=int(request.form.get("hours_per_week")),
            native_country=int(request.form.get("native_country"))
        )

    # Extract a DataFrame from the CustomClass instance
    final_data = data.get_dataframe()

    # Create an instance of PredictionPipeline
    pipeline_prediction = PredictionPipeline()

    # Make predictions using the pipeline
    predict = pipeline_prediction.predict(final_data)

    # Determine the result based on the prediction
    result = predict
    
    # Render the appropriate result template based on the prediction result
    if result == 0:
        return render_template("results.html",final_result=f"You Income is less than equal $50k:{result}")
    else:
        return render_template("results.html",final_result=f"You Income is more than $50k:{result}")
    
# Run the Flask app if the script is executed
if __name__ == "__main__":
    app.run(debug=True)
