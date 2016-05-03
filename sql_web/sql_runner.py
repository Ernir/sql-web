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
        Returns 0 if OK
        """
        if self.statement_type == "DDL":
            return self._validate_ddl()
        else:
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
        # First, strip whitespace:
        clean_statements = "".join(self.statements.split())
        clean_to_emulate = "".join(self.to_emulate.split())
        print(self.statements)
        return clean_statements == clean_to_emulate