import sqlite3
from sqlite3 import OperationalError


class ExerciseRunner:
    """
    A class that handles validating student-submitted SQL statements.
    """

    BAD_SETUP_MSG = "Uppsetning æfingarinnar olli villu, sem bendir til þess að æfingin hafi verið rangt sett inn. " \
                    "Mælt er með því að hafa samband við kennara."
    BROKEN_COMMAND_MSG = "Keyrsla skipunarinnar olli eftirfarandi villu: <strong>{}</strong>"
    CORRECT_MSG = "Rétt!"
    WRONG_RESULTS_MSG = "Skipunin er lögleg SQL-skipun, en hún skilaði rangri niðurstöðu."
    NO_EXACT_MATCH = "Skipunin sem þú gafst passar ekki nákvæmlega við þá skipun sem búist var við. " \
                     "Má ekki bjóða þér að reyna aftur?"
    UNEXPECTED_ERROR = "Keyrsla skipunarinnar olli villu sem enginn gerði ráð fyrir!" \
                       "Mælt er með því að hafa samband við kennara."
    INCORRECT = False
    CORRECT = True

    def __init__(self, statements, schema, to_emulate, statement_type):
        self.schema = schema
        self.user_statements = statements
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
        """
        Runs the given queries against an in-memory SQLite database for comparison
        """
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()

        # Set up the pre-defined database schema.
        try:
            cursor.executescript(self.schema)
        except OperationalError:
            conn.close()
            return self.INCORRECT, self.BAD_SETUP_MSG
        except Exception:
            conn.close()
            return self.INCORRECT, self.UNEXPECTED_ERROR

        # Fetch the results of the query that should be emulated.
        try:
            expected_result = cursor.execute(self.to_emulate).fetchall()
        except OperationalError:
            conn.close()
            return self.INCORRECT, self.BAD_SETUP_MSG
        except Exception:
            conn.close()
            return self.INCORRECT, self.UNEXPECTED_ERROR

        # Fetch the results of whatever statement the user entered.
        try:
            user_result = cursor.execute(self.user_statements).fetchall()
        except OperationalError as oe:
            conn.close()
            return self.INCORRECT, self.BROKEN_COMMAND_MSG.format(str(oe))
        except Exception:
            conn.close()
            return self.INCORRECT, self.UNEXPECTED_ERROR

        # Compare the results of the queryset to be emulated and the result of the user's query
        ordered = "ORDER BY" in self.to_emulate.upper()
        if self._querysets_equal(user_result, expected_result, ordered):
            result, message = self.CORRECT, self.CORRECT_MSG
        else:
            result, message = self.INCORRECT, self.WRONG_RESULTS_MSG
        conn.close()
        return result, message

    @staticmethod
    def _querysets_equal(user_queryset, expected_queryset, ordered=False):
        """
        Compares two querysets as returned by a Python sqlite3 cursor for equality.
        """
        while user_queryset and expected_queryset:
            try:
                result = expected_queryset.pop(0)  # We pick out the elements one by one...
            except IndexError:
                break
            try:
                i = user_queryset.index(result)  # ... if the element is in the user's queryset, we find it...
            except ValueError:
                break

            # ... and pop it out.
            if not ordered or i == 0:
                user_queryset.pop(i)
        # If the querysets were equal, all elements were picked out, otherwise one of the lists still has elements.
        return not expected_queryset and not user_queryset

    def _validate_ddl(self):
        """
        Performs naive string comparisons on the given SQL statements.
        """
        # First, strip whitespace and normalize case:
        clean_statements = "".join(self.user_statements.split()).lower()
        clean_to_emulate = "".join(self.to_emulate.split()).lower()
        if clean_statements == clean_to_emulate:
            return self.CORRECT, self.CORRECT_MSG
        else:
            return self.INCORRECT, self.NO_EXACT_MATCH
