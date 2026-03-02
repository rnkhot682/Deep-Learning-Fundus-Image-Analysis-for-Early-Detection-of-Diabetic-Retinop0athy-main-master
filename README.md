# 🩺 Diabetic Retinopathy Detection using Deep Learning

## 📌 Project Description

This project aims to detect **Diabetic Retinopathy (DR)** from retinal fundus images using a Deep Learning model based on **Xception (Transfer Learning)** architecture.

Diabetic Retinopathy is a serious eye condition caused by diabetes that can lead to blindness if not detected early. This system helps in early-stage detection using AI.

The project includes:

- ✔ Model Training (Xception CNN)
- ✔ Performance Evaluation
- ✔ Flask Web Application
- ✔ Image Upload & Real-Time Prediction
- ✔ User Login & Registration System

---

## 🧠 Model Details

- **Base Model:** Xception (Pre-trained on ImageNet)
- **Input Size:** 299 × 299 × 3
- **Output Classes:** 5
- **Optimizer:** Adam
- **Loss Function:** Categorical Crossentropy
- **Activation:** Softmax
- **Framework:** TensorFlow / Keras

---

## 🏷 Classification Categories

| Class | Condition |
|-------|------------|
| 0 | No Diabetic Retinopathy |
| 1 | Mild NPDR |
| 2 | Moderate NPDR |
| 3 | Severe NPDR |
| 4 | Proliferative DR |

---

## 📂 Dataset

The dataset is organized into training and testing folders:
dataset/
training/
0/
1/
2/
3/
4/
testing/
0/
1/
2/
3/
4/

### 📁 Dataset & Model Download Links

- 🔗 **Trained Model (.h5 file):**  
  👉 https://drive.google.com/file/d/1jaWRc_l10clG6lhPosO6ee5Vh5mKrjJD/view?usp=drive_link

- 🔗 **Dataset Folder:**  
  👉 https://www.kaggle.com/datasets/arbethi/diabetic-retinopathy-level-detection?select=preprocessed+dataset

---

## ⚙️ Project Workflow

### 1️⃣ Data Preprocessing
- Images resized to 299 × 299
- Applied Xception `preprocess_input`
- Image augmentation during training

---

### 2️⃣ Model Training
- Loaded Xception without top layer
- Added custom Dense layers
- Trained on retinal dataset
- Saved as:


---

### 3️⃣ Model Evaluation

The following plots were generated:

- 📈 Training vs Validation Accuracy
- 📉 Training vs Validation Loss
- 📊 Confusion Matrix
- 📊 Class Distribution Plot

These help analyze overfitting and classification performance.

---

## 🌐 Web Application (Flask)

The trained model is integrated into a Flask-based web application.

### 💻 Frontend Pages

1. **Index Page**
 - Landing page
 - Navigation to Login / Register
 - After login, Predict option visible

2. **Login Page**
 - User authentication
 - Redirects to home after login

3. **Register Page**
 - New user registration

4. **Prediction Page**
 - Upload retinal image
 - Displays:
   - Predicted Class
   - Confidence Score
   - Uploaded Image

---

## 🔍 How Prediction Works

1. User uploads retinal image.
2. Image is:
 - Converted from BGR → RGB
 - Resized to 299×299
 - Preprocessed using Xception preprocessing
3. Model predicts probability for 5 classes.
4. Highest probability is selected.
5. Result displayed on screen.

---

## 🛠 Technologies Used

- Python
- TensorFlow / Keras
- Flask
- OpenCV
- NumPy
- Matplotlib
- HTML
- CSS
- Bootstrap

---

## 🚀 How to Run the Project

### Step 1: Install Required Libraries

```bash
pip install tensorflow flask numpy opencv-python matplotlib
```
Step 2: Place Model File

Put:
Updated-xception-diabetic-retinopathy.h5

Step 3: Run Flask App
python app.py

Step 4: Open in Browser
http://127.0.0.1:5000/

📊 Output Example

Uploaded Image

Prediction: Moderate NPDR

📄 Conclusion

This project demonstrates how Transfer Learning with Xception can be used for accurate multi-class classification of Diabetic Retinopathy. The integration with a Flask web application makes the system interactive and user-friendly for real-world applications.
