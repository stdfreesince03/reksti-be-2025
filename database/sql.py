import sqlite3
import json
import os
from typing import List, Optional

DEFAULT_DATABASE_PATH = "local_database.db"

class Database:
    _instance = None

    def __new__(cls, db_path: str = DEFAULT_DATABASE_PATH):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db_path = db_path
        return cls._instance

    def connect(self):
        return sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)

db = Database()

class Student:
    @staticmethod
    def create(nim: str, name: str, classes: Optional[List[str]] = None):
        classes_json = json.dumps(classes or [])
        with db.connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO students (nim, name, classes) VALUES (?, ?, ?)",
                (nim, name, classes_json)
            )

    @staticmethod
    def read(nim: str) -> Optional[tuple]:
        with db.connect() as conn:
            row = conn.execute("SELECT nim, name, classes FROM students WHERE nim = ?", (nim,)).fetchone()
            if row:
                # Deserialize the JSON string back into a list
                classes = json.loads(row[2]) if row[2] else []
                return (row[0], row[1], classes)
            return None

    @staticmethod
    def update(nim: str, name: str, classes: Optional[List[str]] = None):
        classes_json = json.dumps(classes or [])
        with db.connect() as conn:
            conn.execute(
                "UPDATE students SET name = ?, classes = ? WHERE nim = ?",
                (name, classes_json, nim)
            )

    @staticmethod
    def delete(nim: str):
        with db.connect() as conn:
            conn.execute("DELETE FROM students WHERE nim = ?", (nim,))

    @staticmethod
    def add_class(nim: str, new_class: str):
        with db.connect() as conn:
            row = conn.execute("SELECT classes FROM students WHERE nim = ?", (nim,)).fetchone()
            if row:
                current_classes = json.loads(row[0]) if row[0] else []
                current_classes.append(new_class)

                classes_json = json.dumps(current_classes)
                conn.execute("UPDATE students SET classes = ? WHERE nim = ?", (classes_json, nim))


class Encoding:
    @staticmethod
    def create(nim: str, vector: List[float]):
        vector_json = json.dumps(vector.tolist())
        with db.connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO encodings (nim, vector) VALUES (?, ?)",
                (nim, vector_json)
            )

    @staticmethod
    def read(nim: str) -> Optional[List[float]]:
        with db.connect() as conn:
            row = conn.execute("SELECT vector FROM encodings WHERE nim = ?", (nim,)).fetchone()
            return json.loads(row[0]) if row else None

    @staticmethod
    def update(nim: str, vector: List[float]):
        vector_json = json.dumps(vector)
        with db.connect() as conn:
            conn.execute("UPDATE encodings SET vector = ? WHERE nim = ?", (vector_json, nim))

    @staticmethod
    def delete(nim: str):
        with db.connect() as conn:
            conn.execute("DELETE FROM encodings WHERE nim = ?", (nim,))


class ClassEntry:
    @staticmethod
    def create(cid: str, nim: str, status: bool):
        with db.connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO classes (cid, nim, status) VALUES (?, ?, ?)",
                (cid, nim, int(status))
            )

    @staticmethod
    def read(cid: str) -> List[dict]:
        with db.connect() as conn:
            rows = conn.execute("SELECT nim, status FROM classes WHERE cid = ?", (cid,)).fetchall()
            return [{"nim": row[0], "status": bool(row[1])} for row in rows]

    @staticmethod
    def update(cid: str, nim: str, status: bool):
        with db.connect() as conn:
            conn.execute(
                "UPDATE classes SET status = ? WHERE cid = ? AND nim = ?",
                (int(status), cid, nim)
            )

    @staticmethod
    def delete(cid: str):
        with db.connect() as conn:
            conn.execute("DELETE FROM classes WHERE cid = ?", (cid,))


def create_local_db(db_path: str = DEFAULT_DATABASE_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create `students` table with classes as TEXT to store JSON
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            nim TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            classes TEXT DEFAULT NULL
        )
    ''')

    # Create `encodings` table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS encodings (
            nim TEXT PRIMARY KEY,
            vector TEXT NOT NULL,  -- Store vector as JSON
            FOREIGN KEY(nim) REFERENCES students(nim)
        )
    ''')

    # Create `classes` table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
        cid TEXT NOT NULL,
        nim TEXT NOT NULL,
        status INTEGER NOT NULL CHECK (status IN (0, 1)),
        PRIMARY KEY (cid, nim),
        FOREIGN KEY(nim) REFERENCES students(nim)
        )
    ''')

    conn.commit()
    conn.close()



if __name__ == "__main__":
    # if os.path.exists(DEFAULT_DATABASE_PATH):
    #     os.remove(DEFAULT_DATABASE_PATH)
    #     print(f"Deleted existing database: {DEFAULT_DATABASE_PATH}")

    create_local_db()
    print("Database successfully created!")

    conn = sqlite3.connect(DEFAULT_DATABASE_PATH)
    cursor = conn.cursor()

    print("\nInteractive SQL prompt (type 'exit' to quit):")

    try:
        while True:
            sql_query = input("SQL> ")

            if sql_query.lower() in ('exit', 'quit'):
                print("Exiting...")
                break

            try:
                cursor.execute(sql_query)

                if sql_query.strip().lower().startswith("select"):
                    results = cursor.fetchall()
                    for row in results:
                        print(row)
                else:
                    conn.commit()
                    print("Query executed successfully!")
            except Exception as e:
                print(f"Error: {e}")
    finally:
        conn.close()
