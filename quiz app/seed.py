from app import app, db
from models import Question
import sqlalchemy
import pymysql

# Create database if it doesn't exist
engine = sqlalchemy.create_engine('mysql+pymysql://root:Sivareddy%402005@localhost/')
with engine.connect() as conn:
    conn.execute(sqlalchemy.text("CREATE DATABASE IF NOT EXISTS quiz_db"))

with app.app_context():
    db.create_all()
    
    # Check if we already have questions
    if Question.query.count() == 0:
        questions = [
            Question(category="Science", text="What is the chemical symbol for gold?", option_a="Go", option_b="Gd", option_c="Au", option_d="Ag", correct_option="c"),
            Question(category="Science", text="Which planet is known as the Red Planet?", option_a="Venus", option_b="Mars", option_c="Jupiter", option_d="Saturn", correct_option="b"),
            Question(category="Science", text="What is the hardest natural substance on Earth?", option_a="Gold", option_b="Iron", option_c="Diamond", option_d="Quartz", correct_option="c"),
            Question(category="History", text="In what year did World War II end?", option_a="1945", option_b="1939", option_c="1918", option_d="1914", correct_option="a"),
            Question(category="History", text="Who was the first President of the United States?", option_a="Thomas Jefferson", option_b="Abraham Lincoln", option_c="George Washington", option_d="John Adams", correct_option="c"),
            Question(category="History", text="Which ancient civilization built the Machu Picchu?", option_a="Aztec", option_b="Maya", option_c="Inca", option_d="Olmec", correct_option="c"),
            Question(category="Tech", text="What does 'HTTP' stand for?", option_a="HyperText Transfer Protocol", option_b="HyperText Transmission Protocol", option_c="Hyperlink Transfer Technology", option_d="Hyperlink Text Transfer", correct_option="a"),
            Question(category="Tech", text="Who is known as the father of the computer?", option_a="Alan Turing", option_b="Charles Babbage", option_c="Bill Gates", option_d="Steve Jobs", correct_option="b"),
            Question(category="Tech", text="Which company created the Python programming language?", option_a="Google", option_b="Microsoft", option_c="Apple", option_d="None of the above (created by Guido van Rossum)", correct_option="d"),
            Question(category="Science", text="What gas do plants absorb from the atmosphere?", option_a="Oxygen", option_b="Nitrogen", option_c="Carbon Dioxide", option_d="Hydrogen", correct_option="c")
        ]
        db.session.bulk_save_objects(questions)
        db.session.commit()
        print("Database seeded with 10 questions.")
    else:
        print("Questions already exist in the database.")
