# School Vaccination Portal

## 📚 Overview
The **School Vaccination Portal** is a web-based application designed to streamline the management of vaccination drives for students. It provides features for administrators to manage students, vaccination drives, and generate reports, while ensuring secure access through role-based authentication.

---

## 🛠️ Features

### **Admin Features**
- **Student Management**:
  - Add, edit, and delete student records.
  - Bulk upload students via CSV.
  - Mark students as vaccinated.
- **Vaccination Drives**:
  - Create, edit, and delete vaccination drives.
  - Automatically mark past drives as completed.
- **Reports**:
  - Generate vaccination reports.
  - Export reports in CSV, Excel, and PDF formats.
- **Analytics Dashboard**:
  - View total students, vaccinated students, scheduled drives, and available doses.

### **Authentication**
- Role-based access control using JWT.
- Admin-only access to protected routes.

---

## 🏗️ Tech Stack

### **Frontend**
- **React**: For building the user interface.
- **Axios**: For API requests.
- **React Router**: For navigation.
- **CSS Modules**: For styling.

### **Backend**
- **Flask**: For building the REST API.
- **MongoDB**: For database management.
- **Flask-JWT-Extended**: For authentication.
- **Flask-CORS**: For handling cross-origin requests.

---

## 🚀 Setup Instructions

### **Prerequisites**
- **Node.js** and **npm** for the frontend.
- **Python 3.x** and **pip** for the backend.
- **MongoDB** for the database.

---

### **Backend Setup**
1. Navigate to the backend directory:
   ```bash
   cd backend-vaccination-portal/backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Seed the database with initial data:
   ```bash
   python seed.py
   ```
4. Start the backend server:
   ```bash
   python app.py
   ```
5. The backend will run on `http://localhost:5000`.

---

## 📂 Project Structure

### **Backend**
```
backend/
├── app.py                    # Entry point for the Flask app
├── config.py                 # Configuration settings for Flask
├── db.py                     # MongoDB connection setup
├── requirements.txt          # Python dependencies
├── seed.py                   # Script to seed initial data into the database
├── models/                   # Database models
│   ├── students.py           # Model for students
│   ├── users.py              # Model for users
│   └── vaccination_drives.py # Model for vaccination drives
├── routes/                   # API routes
│   ├── admin_routes.py       # Routes for admin operations
│   ├── auth.py               # Authentication routes (login, register)
│   ├── dashboard.py          # Analytics and dashboard routes
│   └── drives.py             # Routes for managing vaccination drives
├── utils/                    # Utility functions
│   └── decorators.py         # Custom decorators (e.g., role-based access)
├── students.csv              # Sample student data for seeding
├── users.csv                 # Sample user data for seeding
├── vaccination_drives.csv    # Sample vaccination drive data for seeding
├── swagger.yaml              # API documentation

```

---

## 🔑 Authentication
- **JWT** is used for secure authentication.
- Tokens are stored in `localStorage` on the frontend.
- Protected routes are accessible only to authorized roles.

---

## 📊 API Endpoints

### **Authentication**
- `POST /login`: Login and get a JWT token.
- `POST /register`: Register a new user (admin only).

### **Students**
- `GET /students`: List all students.
- `POST /students`: Add a new student.
- `POST /students/bulk`: Bulk upload students via CSV.
- `PUT /students/<id>/vaccinate`: Mark a student as vaccinated.

### **Vaccination Drives**
- `GET /drives`: List all drives.
- `POST /drives`: Create a new drive.
- `PUT /drives/<id>`: Update a drive.
- `DELETE /drives/<id>`: Delete a drive.
- `GET /drives/by-class`: Filter drives for student to register based on class

### **Analytics**
- `GET /analytics`: Fetch dashboard analytics.

---

## 🧪 Testing
- Use **Postman** or any REST client to test the API.
- Include the JWT token in the `Authorization` header:
  ```
  Authorization: Bearer <your_token>
  ```

---

## 📦 Deployment
1. Build the backend:
   ```bash
   python app.py
   ```
2. Deploy the backend and frontend to your preferred hosting service.

---

## 🧑‍💻 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License
This project is licensed under the MIT License.
