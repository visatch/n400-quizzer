# N400-Quizzer

A simple quiz application designed to help you learn the 100 questions asked during the N400 (U.S. naturalization) test.

## How to Run Locally

Follow these steps to set up and run the project on your local machine:

### 1. Install Necessary Packages
Ensure Python and pip are installed on your system. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Apply Database Migrations
Set up the database by applying migrations:

```bash
python manage.py migrate
```

### 3. Load Questions 

```bash
python manage.py load_questions
```

### 4. Run the Development Server
Start the Django development server:

```bash
python manage.py runserver
```

### 5. Access the Project
Open your web browser and navigate to:

```
http://127.0.0.1:8000/
```

The application should now be running locally.

---

