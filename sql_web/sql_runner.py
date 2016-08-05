import sqlite3
from sqlite3 import OperationalError


class ExerciseRunner:
    """
    A class that handles validating student-submitted SQL statements.
    """

    BAD_SETUP_MSG = "Uppsetning æfingarinnar olli villu, sem bendir til þess að æfingin hafi verið rangt sett inn. " \
                    "Mælt er með því að hafa samband við kennara."
    COMMAND_ERROR_MSG = "Keyrsla skipunarinnar olli eftirfarandi villu: <strong>{}</strong>"
    CORRECT_MSG = "Rétt!"
    WRONG_INFO_MSG = "Skipunin er lögleg SQL-skipun, en hún skilaði rangri niðurstöðu."
    NO_EXACT_MATCH = "Skipunin sem þú gafst passar ekki nákvæmlega við þá skipun sem búist var við. " \
                     "Má ekki bjóða þér að reyna aftur?"
    UNEXPECTED_ERROR = "Keyrsla skipunarinnar olli villu sem enginn gerði ráð fyrir!" \
                       "Mælt er með því að hafa samband við kennara."
    INCORRECT = False
    CORRECT = True

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
        elif self.statement_type == "DML":
            return self._validate_dml()
        else:
            raise ValueError("Ég skil ekki verkefnisgerðina \"{}\"".format(self.statement_type))

    def _validate_dml(self):
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()

        try:
            cursor.executescript(self.schema)
        except OperationalError:
            conn.close()
            return self.INCORRECT, self.BAD_SETUP_MSG
        except Exception:
            conn.close()
            return self.INCORRECT, self.UNEXPECTED_ERROR

        try:
            user_result = cursor.execute(self.statements).fetchall()
        except OperationalError as oe:
            conn.close()
            return self.INCORRECT, self.COMMAND_ERROR_MSG.format(str(oe))
        except Exception:
            conn.close()
            return self.INCORRECT, self.UNEXPECTED_ERROR

        if self._querysets_equal(user_result, conn):
            result, message = self.CORRECT, self.CORRECT_MSG
        else:
            result, message = self.INCORRECT, self.WRONG_INFO_MSG
        conn.close()
        return result, message

    def _querysets_equal(self, user_result, conn):
        cursor = conn.cursor()
        try:
            expected_result = cursor.execute(self.to_emulate).fetchall()
        except OperationalError:
            conn.close()
            return self.INCORRECT, self.BAD_SETUP_MSG
        except Exception:
            conn.close()
            return self.INCORRECT, self.UNEXPECTED_ERROR

        while expected_result:  # We check all elements in the set of expected results
            result = expected_result.pop()  # We pick out the elements one by one...
            try:
                i = user_result.index(result)  # ... if the element is in the user's queryset, we pick it out too
                user_result.pop(i)
            except ValueError:
                break
        # If the querysets were equal, all elements were picked out, otherwise one of the lists still has elements.
        return not expected_result and not user_result

    def _validate_ddl(self):
        """
        Performs naive string comparisons on the given SQL statements.
        """
        # First, strip whitespace and normalize case:
        clean_statements = "".join(self.statements.split()).lower()
        clean_to_emulate = "".join(self.to_emulate.split()).lower()
        if clean_statements == clean_to_emulate:
            return self.CORRECT, self.CORRECT_MSG
        else:
            return self.INCORRECT, self.NO_EXACT_MATCH
