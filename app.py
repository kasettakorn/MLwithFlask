from flask import Flask, render_template, request, jsonify, redirect, url_for
from keras.models import load_model, Model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = "/static/images"

# connect = pymysql.connect("192.168.64.2", "root", "", "FakeOrReal")
# def load_data():
#     cur = connect.cursor()
#     cur.execute("select * from Users")
#     rows = cur.fetchall()
#     return rows

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/fake_detection")
def fake_detection():
    return render_template("fakeDetection.html")

@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        if request.files:

            file = request.files["image"]
            filepath = "./static/images/image.jpg"
            file.save(filepath)

    return redirect(url_for('showData'))
@app.route("/showData")
def showData():
    #loadimage, resize, to array
    img = load_img("./static/images/image.jpg", target_size = (300, 300))    
    img = img_to_array(img)        
    img = img.reshape(1, 300, 300, 3)    
    img = img.astype('uint8')
    result = model.predict(img)
    fakeRate = format(result[0][0]*100, '.2f')
    realRate = format(result[0][1]*100, '.2f')
    return render_template("ShowData.html", fakeRate=fakeRate, realRate=realRate)
if __name__ == "__main__":
    model = load_model("model.h5")
    app.run(debug=True)