# Educational Management System

A Django-based backend system designed to manage educational interactions between admins, doctors (instructors), and students. The system handles user authentication with admin verification, course creation and enrollment, online examinations, and a digital library.

## 🚀 Features

### User Management (`register` app)
* **Multi-User Roles:** Supports **Admin**, **Doctor**, and **Student** roles.
* **Authentication:** Secure Registration and Login endpoints.
* **Admin Verification:** New accounts require validation by an Admin before access is granted.
* **Profile Management:** Users can edit their first name, last name, and password.

### Course Management (`course` app)
* **Course Creation:** Doctors can create new courses.
* **Enrollment System:**
    * Students can browse courses and send registration requests.
    * Doctors can view and accept student requests.
* **Course Content:** Supports adding lectures and exams to the course stream.
* **Progress Tracking:** Tracks the last page/content accessed by the student.

### Examination System (`exam` app)
* **Dynamic Exams:** Doctors can create exams with specific questions, degrees, and answers.
* **Online Solving:** Students can submit answers to exams directly through the API.
* **Grading:**
    * **Auto-grading:** The system calculates results based on provided model answers.
    * **Gradebook:** Doctors can finalize and correct exam results.

### Digital Library (`library` app)
* **Article Repository:** Users can retrieve a list of educational articles.
* **Publishing:** Authorized users can add new articles with titles and subjects.

## 🛠️ Technology Stack
* **Framework:** Django 5.0
* **API:** Django REST Framework
* **Database:** SQLite (default)
* **CORS:** `django-cors-headers` enabled for frontend integration.

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd educational-management-system
    ```

2.  **Install Dependencies**
    Ensure you have Python installed. It is recommended to use a virtual environment.
    ```bash
    pip install django djangorestframework django-cors-headers
    ```

3.  **Apply Database Migrations**
    ```bash
    python manage.py migrate
    ```

4.  **Run the Server**
    ```bash
    python manage.py runserver
    ```

## 🔗 API Endpoints

### Authentication & Users
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/register/` | Create a new account |
| `POST` | `/login/` | Authenticate user |
| `GET` | `/getrequests/` | (Admin) View pending user approvals |
| `PUT` | `/replyuser/<pk>/<state>/` | (Admin) Approve (1) or Reject user |
| `GET` | `/getallusers/` | List all verified users |
| `GET` | `/getprofile/<id>/` | Retrieve user profile |
| `PUT` | `/editfirstname/<id>/` | Update first name |
| `PUT` | `/editlastname/<id>/` | Update last name |
| `PUT` | `/editpassword/<id>/` | Change password |
| `DELETE` | `/logiut/<id>/` | Delete account/Logout |

### Courses
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/getmycourses/<id>/` | List courses for a specific user |
| `POST` | `/createcourse/<doctorId>/` | Create a new course |
| `PUT` | `/addlecture/<courseId>/` | Add a lecture to a course |
| `PUT` | `/addexam/<courseId>/` | Add an exam to a course |
| `GET` | `/getpage/<courseId>/<studentId>/<pageIndex>/` | Get course content page |
| `GET` | `/getcourses/<studentId>/` | List available courses to join |
| `PUT` | `/courseregister/<courseId>/<studentId>/` | Request to join a course |
| `GET` | `/getallregisterrequests/<doctorId>/` | View course join requests |
| `PUT` | `/acceptregisterrequest/<courseId>/<studentId>/` | Accept a student into a course |
| `GET` | `/getstudentsincourse/<courseId>/` | List students in a course |
| `DELETE` | `/deletestudentfromcourse/<courseId>/<studentId>/` | Remove a student |
| `DELETE` | `/deletecourse/<courseId>/` | Delete a course |

### Exams
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/solveexam/<courseId>/<examId>/` | Submit exam answers |
| `POST` | `/doctor/correctexam/` | Finalize student grade |
| `GET` | `/doctor/getdoctorlist/<pk>/` | Get list of student results (Doctor view) |
| `GET` | `/student/getstudentlist/<pk>/` | Get personal exam results (Student view) |

### Library
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/getarticles/` | Retrieve all articles |
| `POST` | `/addarticle/` | Publish a new article |
