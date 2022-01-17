import sqlite3

# class Patient:
#
#     """generic patient class"""
#
#     def __init__(self, firstName, middleInit, lastName, age, gender, dob):
#
#         self.firstName = firstName
#         self.middleInit = middleInit
#         self.lastName = lastName
#         self.age = age
#         self.gender = gender
#         self. dob = dob
#
#
#
# class Staff:
#
#     """generic staff class"""
#
#     def __init__(self, firstName, lastName, job):
#
#         self.firstName = firstName
#         self.lastName = lastName
#         self.job = job
#


conn = sqlite3.connect('patients.db')
#conn = sqlite3.connect(':memory:')

c = conn.cursor()

# c.execute("""CREATE TABLE patients (
#     firstName text,
#     middleInit text,
#     lastName text,
#     age integer,
#     gender text,
#     dob integer
#     )""")
#
# conn.commit()
# conn.close()

c.execute("""CREATE TABLE staff (
    firstName text,
    lastName text,
    job text
    )""")

conn.commit()
conn.close()

def insert_patient(p):
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()

    c.execute("INSERT INTO patients VALUES (?,?,?,?,?,?)", (p.firstName, p.middleInit, p.lastName, p.age, p.gender, p.dob))

    conn.commit()
    conn.close()

def insert_staff(s):
    conn = sqlite3.connect('staff.db')
    c = conn.cursor()

    c.execute("INSERT INTO staff VALUES (?,?,?)",
              (s.firstName, s.lastName, s.job))

    conn.commit()
    conn.close()

def get_patient_by_lastName(ln):
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()

    c.execute("SELECT * FROM patients WHERE lastName = (?)", (ln,))
    return c.fetchall()

    conn.commit()
    conn.close()


def get_patient_by_dob(dob):
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()

    c.execute("SELECT * FROM patients WHERE dob = (?)", (dob,))
    return c.fetchall()

    conn.commit()
    conn.close()

def get_staff_by_job(j):
    conn = sqlite3.connect('staff.db')
    c = conn.cursor()

    c.execute("SELECT * FROM staff WHERE job = (?)", (j,))
    return c.fetchall()

    conn.commit()
    conn.close()


# def update_patient( ):
#   pass

def drop_patient(rowid):
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()

    c.execute("DELETE from patients WHERE rowid = (?)", rowid)

    conn.commit()
    conn.close()

def drop_staff(rowid):
    conn = sqlite3.connect('staff.db')
    c = conn.cursor()

    c.execute("DELETE from staff WHERE rowid = (?)", rowid)

    conn.commit()
    conn.close()

def remove_patient(p):
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()

    c.execute("SELECT count(*) FROM patients")

    if c.fetchone()[0] != 0:

        c.execute("SELECT rowid, * FROM patients WHERE firstName = (?) AND lastName = (?) AND dob = (?)", (p.firstName, p.lastName, p.dob,))

        temp = c.fetchall()
        temp.append(c.fetchone())

        if len(temp) > 1:

            rowid = temp[0][0]

            conn.commit()
            conn.close()

            drop_patient(str(rowid))

def remove_staff(s):
    conn = sqlite3.connect('staff.db')
    c = conn.cursor()

    c.execute("SELECT count(*) FROM staff")

    if c.fetchone()[0] != 0:

        c.execute("SELECT rowid, * FROM staff WHERE firstName = (?) AND lastName = (?) AND job = (?)",
                  (s.firstName, s.lastName, s.job))

        temp = c.fetchall()
        temp.append(c.fetchone())

        if len(temp) > 1:
            rowid = temp[0][0]

            conn.commit()
            conn.close()

            drop_staff(str(rowid))

