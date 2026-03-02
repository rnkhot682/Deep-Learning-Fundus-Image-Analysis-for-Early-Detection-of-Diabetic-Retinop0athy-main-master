import os
import numpy as np
import cv2
import tensorflow as tf
import psycopg2
from flask import Flask, request, flash, render_template, redirect, url_for, session
from tensorflow.keras.applications.xception import preprocess_input
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2 import errors

# ================= CONFIG =================

MODEL_PATH = "Updated-xception-diabetic-retinopathy.h5"
UPLOAD_FOLDER = "User_Images"
IMG_SIZE = 299

CLASS_NAMES = [
    "No Diabetic Retinopathy",
    "Mild NPDR",
    "Moderate NPDR",
    "Severe NPDR",
    "Proliferative DR"
]

DB_CONFIG = {
    "host": "localhost",
    "database": "Diabetic",
    "user": "postgres",
    "password": "Abcd@1234",
    "port": 5432
}

# ================= APP =================

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# defer model loading to compatibility wrapper below
model = None
# Compatibility wrapper: some saved models include a 'quantization_config' key
# in layer configs. Older/newer Keras may not accept that kwarg; define a
# Dense subclass that accepts and ignores it, then pass in custom_objects
from tensorflow.keras.layers import Dense as _KerasDense


class DenseCompat(_KerasDense):
    def __init__(self, *args, quantization_config=None, **kwargs):
        super().__init__(*args, **kwargs)


# Try loading with a compatibility mapping (safe for inference)
try:
    model = tf.keras.models.load_model(MODEL_PATH, custom_objects={"Dense": DenseCompat})
    print("Model loaded successfully (compat)")
except Exception:
    # fallback to default load (raise original error)
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully")

# ================= DATABASE =================

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# ================= ROUTES =================

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

# -------- REGISTER --------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)",
                (name, email, phone, hashed_password)
            )
            conn.commit()

            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))

        except errors.UniqueViolation:
            conn.rollback()
            flash("Email already exists!", "danger")
            return redirect(url_for("register"))

        finally:
            cur.close()
            conn.close()

    return render_template("register.html")


# -------- LOGIN --------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, password, name FROM users WHERE email=%s", (email,))
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            session["user_name"] = user[2]

            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")


# -------- LOGOUT --------

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("index"))


# -------- PREDICTION --------

@app.route("/predict", methods=["GET", "POST"])
def predict():

    if "user_id" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":

        file = request.files["file"]
        if file.filename == "":
            flash("No file selected!", "danger")
            return render_template("prediction.html")

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        img = cv2.imread(filepath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img = img.astype("float32")
        img = preprocess_input(img)
        img = np.expand_dims(img, axis=0)

        preds = model.predict(img)
        class_id = int(np.argmax(preds))
        confidence = float(np.max(preds))

        result = CLASS_NAMES[class_id]

        return render_template(
            "prediction.html",
            prediction=result,
            confidence=f"{confidence:.2f}",
            fname=filepath
        )

    return render_template("prediction.html")


# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)
