import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

# Database setup
a = sqlite3.connect("qu_iz_app.db")
b = a.cursor()
b.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
b.execute("""
CREATE TABLE IF NOT EXISTS results (
    user_id INTEGER,
    subject TEXT,
    score INTEGER,
    correct_answers INTEGER,
    incorrect_answers INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")
a.commit()

#  questions
questions = {
    "DSA": [
        {"question": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n^2)", "O(1)"], "answer": 1},
        {"question": "Which data structure is used for BFS?", "options": ["Stack", "Queue", "Array", "Tree"], "answer": 1},
        {"question": "Which sorting algorithm is the fastest?", "options": ["Bubble Sort", "Quick Sort", "Insertion Sort", "Selection Sort"], "answer": 1},
        {"question": "What is a full binary tree?", "options": ["All nodes have 2 children", "All leaves are at the same level", "Nodes have 0 or 2 children", "None"], "answer": 2},
        {"question": "What is a graph?", "options": ["Set of vertices and edges", "Only vertices", "Only edges", "None"], "answer": 0},
    ],
    "ML": [
        {"question": "Which algorithm is used for classification?", "options": ["SVM", "K-Means", "Apriori", "Naive Bayes"], "answer": 3},
        {"question": "What is supervised learning?", "options": ["Labeled data", "Unlabeled data", "Both", "None"], "answer": 0},
        {"question": "Which metric is used for regression?", "options": ["Precision", "Recall", "RMSE", "F1 Score"], "answer": 2},
        {"question": "Which model uses backpropagation?", "options": ["SVM", "Decision Trees", "Neural Networks", "KNN"], "answer": 2},
        {"question": "What is overfitting?", "options": ["High accuracy on test", "High accuracy on train", "Both", "None"], "answer": 1},
    ],
    "Python": [
        {"question": "Which keyword is used to define a function?", "options": ["def", "func", "lambda", "None"], "answer": 0},
        {"question": "What does 'list.append()' do?", "options": ["Adds at the start", "Adds at the end", "Removes an element", "None"], "answer": 1},
        {"question": "Which module is used for regular expressions?", "options": ["regex", "re", "reg", "None"], "answer": 1},
        {"question": "Which is immutable?", "options": ["List", "Dictionary", "Set", "Tuple"], "answer": 3},
        {"question": "How do you create a virtual environment?", "options": ["venv", "virtualenv", "Both", "None"], "answer": 2},
    ],
}

# Main Application Class
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.username = None
        self.user_id = None
        self. welcome_scr()

    def clear_scr(self):
        """Clears the current screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def exit_appli(self):
        """Handles exit confirmation."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit the application?"):
            self.root.quit()

    def welcome_scr(self):
        """Creates the welcome screen."""
        self.clear_scr()
        tk.Label(self.root, text="Welcome to the Quiz lets test your knowledge >_<", font=("Arial", 24)).pack(pady=20)
        tk.Button(self.root, text="Register", command=self.register_scr, width=20).pack(pady=10)
        tk.Button(self.root, text="Login", command=self.login_scr, width=20).pack(pady=10)
        tk.Button(self.root, text="Exit", command=self.exit_appli, width=20).pack(pady=10)

    def register_scr(self):
        """Creates the registration screen."""
        self.clear_scr()
        tk.Label(self.root, text="Register", font=("Arial", 18)).pack(pady=20)
        tk.Label(self.root, text="Username:").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()
        tk.Label(self.root, text="Password:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def register():
            username = username_entry.get()
            password = password_entry.get()
            if not username or not password:
                messagebox.showerror("Error", "All fields are required!")
                return
            try:
                b.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                a.commit()
                messagebox.showinfo("Success", "Registration successful!")
                self.welcome_scr()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists!")

        tk.Button(self.root, text="Register", command=register).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.welcome_scr).pack()
        tk.Button(self.root, text="Exit", command=self.exit_appli).pack(pady=10)

    def login_scr(self):
        """Creates the login screen."""
        self.clear_scr()
        tk.Label(self.root, text="Login", font=("Arial", 18)).pack(pady=20)
        tk.Label(self.root, text="Username:").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()
        tk.Label(self.root, text="Password:").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def login():
            username = username_entry.get()
            password = password_entry.get()
            b.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
            user = b.fetchone()
            if user:
                self.username = username
                self.user_id = user[0]
                self.sbjt_scr()
            else:
                messagebox.showerror("Error", "Invalid credentials!")

        tk.Button(self.root, text="Login", command=login).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.welcome_scr).pack()
        tk.Button(self.root, text="Exit", command=self.exit_appli).pack(pady=10)

    def sbjt_scr(self):
        """Creates the subject selection screen."""
        self.clear_scr()
        tk.Label(self.root, text=f"Welcome, {self.username}!", font=("Arial", 18)).pack(pady=20)
        tk.Label(self.root, text="Select a subject:").pack()
        for subject in questions.keys():
            tk.Button(self.root, text=subject, command=lambda s=subject: self.quiz_scr(s), width=20).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.welcome_scr, width=20).pack(pady=10)

    def quiz_scr(self, subject):
        """Creates the quiz screen for the selected subject."""
        self.clear_scr()
        tk.Label(self.root, text=f"{subject} Quiz", font=("Arial", 18)).pack(pady=20)

        shuffled_questions = random.sample(questions[subject], len(questions[subject]))
        score = [0]
        correct_answers = [0]
        incorrect_answers = [0]
        q_index = [0]

        def nxt_qtn():
            if q_index[0] >= len(shuffled_questions):
                result_text = f"Quiz Finished!\nYour score: {score[0]}/{len(shuffled_questions)}\n"
                result_text += f"Correct Answers: {correct_answers[0]}\nIncorrect Answers: {incorrect_answers[0]}"
                messagebox.showinfo("Result", result_text)
                b.execute("""
                    INSERT INTO results (user_id, subject, score, correct_answers, incorrect_answers)
                    VALUES (?, ?, ?, ?, ?)
                """, (self.user_id, subject, score[0], correct_answers[0], incorrect_answers[0]))
                a.commit()
                self.sbjt_scr()
                return
           
            question_data = shuffled_questions[q_index[0]]
            q_index[0] += 1

            self.clear_scr()
            tk.Label(self.root, text=f"Question {q_index[0]}/{len(shuffled_questions)}", font=("Arial", 16)).pack(pady=10)
            tk.Label(self.root, text=question_data["question"], wraplength=400).pack(pady=10)

            for i, option in enumerate(question_data["options"]):
                tk.Button(
                    self.root,
                    text=option,
                    command=lambda i=i: chk_ans(i, question_data["answer"])
                ).pack(pady=5)

        def chk_ans(selected, correct):
            if selected == correct:
                score[0] += 1
                correct_answers[0] += 1
            else:
                incorrect_answers[0] += 1
            nxt_qtn()

        nxt_qtn()

# Run the application
root = tk.Tk()
app = QuizApp(root)
root.mainloop()
