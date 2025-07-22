# database.py

import sqlite3

def init_db():
    """Initializes the database and creates tables if they don't exist."""
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()

    # Create jobs table to store scraped job postings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            company TEXT,
            description TEXT NOT NULL,
            url TEXT UNIQUE
        )
    ''')

    # Create skills table (master list of all unique skills)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # Create a linking table for the many-to-many relationship between jobs and skills
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_skills (
            job_id INTEGER,
            skill_id INTEGER,
            FOREIGN KEY (job_id) REFERENCES jobs (id),
            FOREIGN KEY (skill_id) REFERENCES skills (id),
            PRIMARY KEY (job_id, skill_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()

