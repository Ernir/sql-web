import sqlite3


class ExerciseRunner():
    """
    A class that handles validating student-submitted SQL statements.
    """

    def __init__(self, statements, schema, to_emulate, statement_type):
        self.schema = schema
        self.statements = statements
        self.to_emulate = to_emulate
        self.statement_type = statement_type

    def is_valid(self):
        """
        Returns a 2-tuple.
        First element of the tuple is a boolean, True if the exercise is validated as correct, False otherwise.
        The second element is a string containing a message about the result.
        """
        if self.statement_type == "DDL":
            return self._validate_ddl()
        else:
            return self._validate_dml()

    def _validate_dml(self):
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute(self.schema)
        cursor.execute(self.statements)
        results = cursor.fetchall()
        conn.close()

    def _validate_ddl(self):
        """
        Performs naive string comparisons on the given SQL statements.
        """
        # First, strip whitespace and normalize case:
        clean_statements = "".join(self.statements.split()).lower()
        clean_to_emulate = "".join(self.to_emulate.split()).lower()
        if clean_statements == clean_to_emulate:
            return True, "Rétt!"
        else:
            return False, "Skipunin sem þú gafst passar ekki nákvæmlega við þá skipun sem búist var við. Má ekki bjóða þér að reyna aftur?"
