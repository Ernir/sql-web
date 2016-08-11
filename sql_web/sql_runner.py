import re
import sqlite3
from sqlite3 import OperationalError


class ExerciseRunner:
    """
    A class that handles validating student-submitted SQL statements.
    """

    UNALTERED_INPUT = "Engar breytingar voru gerðar á skipuninni sem var gefin í upphafi. " \
                      "Þú þarft að gera breytingu til að leysa verkefnið."
    BAD_SETUP_MSG = "Uppsetning æfingarinnar olli villu, sem bendir til þess að æfingin hafi verið rangt sett inn. " \
                    "Mælt er með því að hafa samband við kennara."
    BROKEN_COMMAND_MSG = "Keyrsla skipunarinnar olli eftirfarandi villu: <strong>{}</strong>"
    CORRECT_MSG = "Rétt! Verkefninu er nú lokið og niðurstaðan vistuð."
    WRONG_RESULTS_MSG = "Skipunin er lögleg SQL-skipun, en hún skilaði rangri niðurstöðu. "
    NO_EXACT_MATCH = "Skipunin sem þú gafst passar ekki nákvæmlega við þá skipun sem búist var við. " \
                     "Má ekki bjóða þér að reyna aftur?"
    UNEXPECTED_ERROR = "Keyrsla skipunarinnar olli villu sem enginn gerði ráð fyrir!" \
                       "Mælt er með því að hafa samband við kennara."
    NUM_DIFFERENCES = "Fjöldi stafabreytinga sem gera þarf á lausninni til að hún sé eins og lausn kennarans er {}. "
    INCORRECT = False
    CORRECT = True

    def __init__(self, statements, exercise):
        self.user_statements = statements
        self.schema = exercise.given_schema
        self.prepopulated = exercise.prepopulated
        self.to_emulate = exercise.sql_to_emulate
        self.statement_type = exercise.statement_type

        self.schema_setup_complete = False
        self.conn = sqlite3.connect(":memory:")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def is_valid(self):
        """
        Returns a 2-tuple.
        First element of the tuple is a boolean, True if the exercise is validated as correct, False otherwise.
        The second element is a string containing a message about the result.
        """

        sane, message = self._is_sane()
        if not sane:
            return sane, message

        if self.statement_type == "DDL":
            return self._validate_ddl()
        elif self.statement_type == "DML":
            return self._validate_dml()
        else:
            raise ValueError("Unexpected statement type: \"{}\"".format(self.statement_type))

    def parse_schema(self):
        """
        Returns Python-readable information about the defined tables, which consists of a list of dictionaries with
        the following parameters:
        name: The name of a database table
        schema: The CREATE TABLE statement used to create the table in the first place
        columns: A list of the table's column names, in order
        data: All of the table's data, as a list of tuples, in column order.
        """
        cursor = self.conn.cursor()
        if not self.schema_setup_complete:
            self._setup_schema()
        try:
            # SQLite stores raw data about its tables, which we need
            raw_tables = cursor.execute("SELECT name, sql FROM sqlite_master WHERE type = 'table'").fetchall()
            tables = [{"name": raw_table[0], "schema": raw_table[1]} for raw_table in raw_tables]

            for table in tables:
                # We need to extract the column names of each table
                schema = "".join(table["schema"].splitlines())
                all_columns = re.search(".*\((.*)\)", schema).group(1)
                column_definitions = [col_def.strip() for col_def in all_columns.split(",")]
                table["columns"] = []
                for column in column_definitions:
                    table["columns"].append(column.split()[0])

                statement = "SELECT {} FROM {}".format(",".join(table["columns"]), table["name"])
                table["data"] = cursor.execute(statement).fetchall()
        except OperationalError:
            tables = []
        return tables

    def _is_sane(self):
        """
        Checks the entered statement for input errors.
        Returns a boolean indicating whether an error is found. If there's an error, also return an error message.
        """
        if self.prepopulated.strip() == self.user_statements.strip():
            return self.INCORRECT, self.UNALTERED_INPUT
        # ToDo identify more common input errors.
        return self.CORRECT, ""

    def _validate_dml(self):
        """
        Runs the given queries against an in-memory SQLite database for comparison
        """
        cursor = self.conn.cursor()

        if not self.schema_setup_complete:
            self._setup_schema()
        # Fetch the results of the query that should be emulated.
        try:
            expected_result = cursor.execute(self.to_emulate).fetchall()
        except OperationalError:
            return self.INCORRECT, self.BAD_SETUP_MSG
        except Exception:
            return self.INCORRECT, self.UNEXPECTED_ERROR

        # Fetch the results of whatever statement the user entered.
        try:
            user_result = cursor.execute(self.user_statements).fetchall()
        except OperationalError as oe:
            return self.INCORRECT, "{}.\n {}".format(
                self.BROKEN_COMMAND_MSG.format(str(oe)), self.NUM_DIFFERENCES.format(
                    self._lax_levenshtein(self.user_statements, self.to_emulate)
                )
            )
        except Exception:
            return self.INCORRECT, self.UNEXPECTED_ERROR

        # Compare the results of the queryset to be emulated and the result of the user's query
        ordered = "ORDER BY" in self.to_emulate.upper()
        if self._querysets_equal(user_result, expected_result, ordered):
            result, message = self.CORRECT, self.CORRECT_MSG
        else:
            result, message = self.INCORRECT, "{}\n {}".format(
                self.WRONG_RESULTS_MSG, self.NUM_DIFFERENCES.format(
                    self._lax_levenshtein(self.user_statements, self.to_emulate)
                )
            )
        return result, message

    def _setup_schema(self):
        # Set up the pre-defined database schema.
        cursor = self.conn.cursor()
        try:
            cursor.executescript(self.schema)
            self.schema_setup_complete = True
        except OperationalError:
            self.schema_setup_complete = False
            return self.INCORRECT, self.BAD_SETUP_MSG
        except Exception:
            self.schema_setup_complete = False
            return self.INCORRECT, self.UNEXPECTED_ERROR

    @staticmethod
    def _querysets_equal(user_queryset, expected_queryset, ordered=False):
        """
        Compares two querysets as returned by a Python sqlite3 cursor for equality.
        """
        if len(user_queryset) != len(expected_queryset):
            return False

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
        distance = self._lax_levenshtein(self.user_statements, self.to_emulate)
        if distance == 0:
            return self.CORRECT, self.CORRECT_MSG
        else:
            return self.INCORRECT, "{}\n {}".format(
                self.NO_EXACT_MATCH, self.NUM_DIFFERENCES.format(
                    self._lax_levenshtein(self.user_statements, self.to_emulate)
                )
            )

    def _lax_levenshtein(self, s1, s2):
        """
        Returns the Levenshtein distance between two strings, discarding spaces and case differences.
        """
        s1 = "".join(s1.split()).lower()
        s2 = "".join(s2.split()).lower()
        return self._levenshtein(s1, s2)

    def _levenshtein(self, s1, s2):
        """
        Calculates the Levenshtein distance between two strings.
        Implementation borrowed from:
        https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
        """
        if len(s1) < len(s2):
            return self._levenshtein(s2, s1)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]
