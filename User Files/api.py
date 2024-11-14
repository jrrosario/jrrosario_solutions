from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import sqlite3
import os

app = FastAPI()
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "employee.db")


def get_db():
    """
    Provide a connection to the SQLite database for the request lifecycle.

    :yield: SQLite database connection object
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


class EmployeeCheckIn(BaseModel):
    """
    Model representing an employee check-in record.

    :param user: Name of the user
    :param timestamp: Check-in timestamp
    :param hours: Number of hours checked in
    :param project: Project name associated with the check-in
    """
    user: str
    timestamp: str
    hours: float
    project: str


@app.get("/employee_check_in/", response_model=List[EmployeeCheckIn])
def read_items(db: sqlite3.Connection = Depends(get_db)):
    """
    Retrieve all employee check-in records from the database.

    :param db: Database connection (injected by FastAPI dependency)
    :return: List of all employee check-in records
    """
    cursor = db.cursor()
    cursor.execute("SELECT * FROM employee_check_in")
    rows = cursor.fetchall()
    return [EmployeeCheckIn(user=row['user'], timestamp=row['timestamp'], hours=row['hours'], project=row['project']) for row in rows]


@app.get("/employee_check_in/{user}", response_model=List[EmployeeCheckIn])
def read_item(user: str, db: sqlite3.Connection = Depends(get_db)):
    """
    Retrieve all check-in records for a specific user.

    :param user: Username for which to retrieve check-in records
    :param db: Database connection (injected by FastAPI dependency)
    :return: List of check-in records for the specified user
    :raises HTTPException: If no check-in records are found for the user
    """
    cursor = db.cursor()
    cursor.execute("SELECT * FROM employee_check_in WHERE user = ?", (user,))
    rows = cursor.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Employee check-ins not found")
    return [EmployeeCheckIn(user=row['user'], timestamp=row['timestamp'], hours=row['hours'], project=row['project']) for row in rows]
