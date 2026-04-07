# 🎓 Cloud-Based College Event Registration System

## 📌 Overview

This project is a cloud-based web application that allows students to register for college events such as Tech Fest, Cultural Events, and Workshops.

The application is built as a full-stack solution with a frontend interface, backend server, and cloud-based database using Google Cloud Platform (GCP).

---

## 🚀 Features

* Student event registration form
* Data stored in cloud database (Firestore)
* Publicly accessible web application
* Success message after registration
* Scalable and serverless architecture
* Ready for future integrations

---

## 🛠️ Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python (Flask)

### Cloud Services (GCP)

* Cloud Run (Backend Hosting)
* Firestore (Cloud Database)
* Cloud Storage (Frontend Hosting)

---

## 🌐 Architecture

User → Frontend (Cloud Storage) → Backend (Cloud Run) → Firestore Database

---

## ⚙️ How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/HEMANTku2507u0148/eventregistration.git
cd eventregistration
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python app_cloud.py
```

### 4. Open in browser

```text
http://localhost:5000
```

---

## ☁️ Cloud Deployment Steps

### 1. Upload code to GitHub

* Use Git commands to push project

### 2. Deploy Backend on Cloud Run

* Use Dockerfile or source deployment
* Enable public access

### 3. Setup Firestore

* Create Firestore database in Native mode
* Store registration data

### 4. Deploy Frontend on Cloud Storage

* Upload HTML, CSS, JS files
* Enable static website hosting
* Make bucket public

---

## 📂 Project Structure

```
cloud/
├── app_cloud.py
├── Dockerfile
├── requirements.txt
├── templates/
│   ├── index.html
│   └── admin.html
```

---

## 📊 Sample Use Case

1. Student opens the website
2. Fills registration form
3. Clicks submit
4. Data is sent to backend
5. Stored in Firestore
6. Success message displayed

---

## 🔮 Future Enhancements

* User authentication (login/signup)
* Email confirmation
* Admin dashboard
* Event management system
* Cloud monitoring and analytics

---

## 👨‍💻 Author

**Hemant**

---

## 📌 Notes

* This project fulfills the requirements of a cloud-native application using Google Cloud Platform.
* The system is designed to be scalable, reliable, and serverless.

---
