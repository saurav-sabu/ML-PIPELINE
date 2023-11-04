from flask import Flask
from src.logger import logging
from src.exception import CustomException
import sys

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    try:
        raise Exception("We are testing custom file")
        
    except Exception as e:
        abc = CustomException(e,sys)
        logging.info(abc.error_message)
        return "Welcome to World of DESTRUCTION"

if __name__ == "__main__":
    app.run(debug=True)