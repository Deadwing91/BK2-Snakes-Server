import sqlite3
import json
from models import Species


def get_single_species(id):
    with sqlite3.connect("./Snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name
        FROM species a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        snake_species = Species(data['id'], data['name'])

        return snake_species.__dict__

def get_all_species():
    """Function to get all customers"""
    # Open a connection to the database
    with sqlite3.connect("./Snakes.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name
        FROM Species a
        """)

        # Initialize an empty list to hold all animal representations
        species = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            snake_species = Species(row['id'], row['name'])

            #location = Location(row['id'], row['location_name'], row['location_address'])

            #employee.location = location.__dict__


            species.append(snake_species.__dict__)

    return species