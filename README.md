# 🎓 RepoSphere

Welcome to the **RepoSphere** A Student Repository Management System web application which allows students to securely manage and organize their repository data with a user-friendly interface. Built using Flask and SQLite for robust backend functionality and a modern, responsive UI, this project delivers a seamless experience for CRUD operations, searching, and sorting within repositories using javaScript API.

---

## 📌 Features

- **User Authentication**: Secure login and signup functionalities with error handling and success messages.
- **Repository Management**: Full CRUD (Create, Read, Update, Delete) operations for managing student repositories.
- **Search & Sort**: Easily search and sort repositories by date or number.
- **Modern UI**: An intuitive and attractive UI for streamlined user experience.
- **Secure Sessions**: User sessions managed for secure access to repository functionalities.
- **Responsive Design**: Mobile and desktop-friendly layout.

---

## 🚀 Technologies Used

- **Backend**: Flask, SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite for simple, lightweight storage
- **Libraries**: jQuery for enhanced JS operations, Bootstrap for responsive design

---

## 📂 Project Structure

```
project-root/
│
├── instance             # Database File             
├── static/
│   ├── index.css        # Custom CSS Styling for index.html file        
│   ├── index.js         # JavaScript Logic Handling, Frontend Interactivity And API for index.html file
│   ├── repos.css        # Custom CSS Styling for repos.html file        
│   ├── repos.js         # JavaScript Logic Handling, Frontend Interactivity And API for repos.html file
│   └── Style.css        # Custom CSS Styling
├── templates/
│   ├── index.html       # Landing Page With Login and Signup
│   └── repos.html       # Repository Management Page
├── app.py               # Flask Application Entry Point
├── ve                   # Virtual Environment
├── requirements.txt     # Prerequisites              
└── README.md            # Project Documentation


```

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.13.0
- Flask 3.0.3
- Werkzeug 3.0.6
- SQLite 3.42.0
- blinker==1.8.2
- click==8.1.7
- colorama==0.4.6
- itsdangerous==2.2.0
- Jinja2==3.1.4
- MarkupSafe==3.0.2

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/naseer302/RepoSphere.git
   cd RepoSphere
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
3. **Activate virtual environment:**
   ```bash
   ve\Scripts\activate
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   Open your web browser and navigate to `http://localhost:5000`.

---

## 🌐 Key Functionalities

1. **User Authentication**:
   - Login and signup functionality with secure password handling.

2. **Repository Management**:
   - Add, edit, delete, and view repository entries.

3. **Search and Sort**:
   - Real-time search and sorting by date created or number.

4. **Responsive Design**:
   - UI optimized for various screen sizes and devices.

---

## 💻 Screenshots

### Landing Page
![Landing Page](no image yet)

### Repository Management
![RepoSphere](no image yet)

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

## 🧩 Future Enhancements

- **Advanced Filtering**: Filter repositories based on more criteria.
- **Enhanced Security**: Additional layers for securing sensitive data.
- **User Profile Management**: Profile settings for better user experience.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for any improvements.

---

## 💬 Contact

Created by **Naseer** – [Ping me Via Mail](mailto:na5699577@gmail.com)
