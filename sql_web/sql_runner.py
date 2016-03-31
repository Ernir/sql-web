import sqlite3


class ExerciseRunner():
    """
    A class that handles running student-submitted SQL statements.
    """

    def run(self, schema, statements):
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute(schema)
        cursor.execute(statements)
        results = cursor.fetchall()
        conn.close()
        return results