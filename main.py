import pandas
from pathlib import Path
import sqlite3


class COLORS:
    BLACK = '\033[30m'
    GREEN = '\033[32m'
    GREY = '\033[90m'
    RED = '\033[31m'
    WHITE = '\033[37m'


class SCHEMA:
    UNIT_ENROLMENT = "(id INTEGER PRIMARY KEY, unit_code TEXT, student_id INTEGER, semester_year INTEGER, semester INTEGER)"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("database/uni.db")

    def getConn(self):
        return self.conn


def scan_unit_dir(db: Database, university_dir: Path):
    path_unit = Path(str(university_dir) + "/UNIT")
    print_dir_file_status(path_unit)

    if path_unit.exists():
        for unit_dir in path_unit.iterdir():
            db_conn = db.getConn()

            db_conn.execute("CREATE TABLE IF NOT EXISTS " +
                            "Unit" + " (id INTEGER PRIMARY KEY, code TEXT, title TEXT)")
            db_conn.execute(
                "INSERT INTO Unit (code) VALUES ('" + unit_dir.name + "')")
            db_conn.commit()

            path_student_list = str(unit_dir) + "/student_list.csv"
            if Path(path_student_list).exists():
                student_list = pandas.read_csv(
                    path_student_list, index_col=0, sep="\t")
                # print(student_list)
                for student in student_list.itertuples():
                    db_conn.execute("CREATE TABLE IF NOT EXISTS " +
                                    "Unit_Enrolment " + SCHEMA.UNIT_ENROLMENT)
                    db_conn.execute("INSERT INTO Unit_Enrolment (unit_code, student_id, semester_year, semester) VALUES ('" +
                                    unit_dir.name + "', '" + str(student.Index) + "', '" + str(
                                        student.semester_year) + "', '" +
                                    str(student.semester) + "')")
                    db_conn.commit()


def scan_data_dir(db: Database):
    """
    """

    db_conn = db.getConn()

    data_path = Path("data")
    print_dir_file_status(data_path)

    for university_dir in data_path.iterdir():
        print_dir_file_status(university_dir)
        db_conn.execute("CREATE TABLE IF NOT EXISTS " +
                        "University" + " (id INTEGER PRIMARY KEY, name TEXT)")
        db_conn.execute(
            "INSERT INTO University (name) VALUES ('" + university_dir.name + "')")
        db_conn.commit()
        scan_unit_dir(db, university_dir)


def print_dir_file_status(path: Path):
    if path.is_dir():
        file_type = "Directory"
    elif path.is_file():
        file_type = "File"

    print(file_type + " `" + str(path) + "` [", end="")

    if (path.exists()):
        status_color = COLORS.GREEN
        status_str = "FOUND"
    else:
        status_color = COLORS.RED
        status_str = "MISSING"
    print(status_color + status_str, end="")

    print(COLORS.WHITE + "]")


def print_table(db: Database, table_name: str):
    db_conn = db.getConn()
    db_cursor = db_conn.cursor()

    db_cursor.execute(
        "SELECT * FROM sqlite_master WHERE type = 'table' AND name = '" + table_name + "'")
    if (len(db_cursor.fetchall()) == 1):
        db_cursor.execute(
            "SELECT * FROM " + table_name)
        print(db_cursor.fetchall())

    db_conn.commit()


def main_menu():
    input_int = -1
    db = Database()
    db_conn = db.getConn()

    while input_int != 0:
        print("1. Build database")
        print("2. Display database")
        print("3. Delete database")
        print("0. Exit")
        print("")
        input_str = input("Enter selection: ")
        print("")
        input_int = int(input_str) if input_str.isdigit() else -1

        if input_int == 1:
            scan_data_dir(db)
        elif input_int == 2:
            print_table(db, "University")
            print_table(db, "Unit")
            print_table(db, "Unit_Enrolment")
        elif input_int == 3:
            db_conn.execute("DROP TABLE IF EXISTS University")
            db_conn.execute("DROP TABLE IF EXISTS Unit")
            db_conn.execute("DROP TABLE IF EXISTS Unit_Enrolment")
            db_conn.commit()

    db_conn.execute("DROP TABLE IF EXISTS University")
    db_conn.execute("DROP TABLE IF EXISTS Unit")
    db_conn.execute("DROP TABLE IF EXISTS Unit_Enrolment")
    db_conn.commit()
    exit()


if __name__ == "__main__":
    main_menu()
