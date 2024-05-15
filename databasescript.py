import sqlite3

# Connect to the database
conn = sqlite3.connect("todos.db")
c = conn.cursor()

# Insert data into the todos table
todos = [
    ("Buy groceries", "Get milk, eggs, and bread", 2, False),
    ("Finish report", "Complete quarterly report", 1, False),
    ("Clean the house", "Vacuum and dust the living room", 3, True),
]

c.executemany(
    "INSERT INTO todos (title, description, priority, completed) VALUES (?, ?, ?, ?)",
    todos,
)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully into todo.db")
