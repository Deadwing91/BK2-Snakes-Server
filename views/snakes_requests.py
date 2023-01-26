import sqlite3
import json
from models import Snakes
from models import Species


def get_single_snake(id):
    with sqlite3.connect("./Snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            s.id,
            s.name,
            s.owner_id,
            s.species_id,
            s.gender,
            s.color
        FROM Snakes s
        WHERE s.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        snake = Snakes(data['id'], data['name'], data['owner_id'], data['species_id'],
                        data['gender'], data['color'])
                        
        if snake.species_id == 2:
                return ''

        return snake.__dict__

def get_all_snakes():
    """Function to get all customers"""
    # Open a connection to the database
    with sqlite3.connect("./Snakes.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            s.id,
            s.name,
            s.owner_id,
            s.species_id,
            s.gender,
            s.color
        FROM Snakes s
        """)

        # Initialize an empty list to hold all animal representations
        snakes = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            snake = Snakes(row['id'], row['name'], row['owner_id'], row['species_id'], row['gender'], row['color'])

            #location = Location(row['id'], row['location_name'], row['location_address'])

            #employee.location = location.__dict__


            snakes.append(snake.__dict__)

    return snakes

def get_snakes_by_species(species_id):
    """Returns a list of dict. of all snakes of X species"""
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.owner_id,
            a.species_id,
            a.gender,
            a.color
        FROM Snakes a
        WHERE a.species_id = ?
        """, ( species_id, ))

        snakes = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            snake = Snakes(row['id'], row['name'], row['owner_id'],
                            row['species_id'], row['gender'], row['color'])

            snakes.append(snake.__dict__)

    return snakes


def create_snake(new_response):
    """Args: snake (json string), returns new dictionary with id property added"""
    with sqlite3.connect("./snakes.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Snakes
            ( name, owner_id, species_id, gender, color )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_response['name'], new_response['owner_id'],
            new_response['species_id'], new_response['gender'],
            new_response['color'], ))

        id = db_cursor.lastrowid

        new_response['id'] = id

    return new_response
