<div align="center">

[![Python v3.10](https://img.shields.io/badge/Python-v3.10-blue)](https://docs.python.org/3.10/)

</div>

# Uni Model Builder

Attempt to build a model of students at a University based on bits and pieces of information.

## Setup

### Venv

#### Windows

```bash
python -m venv ./venv/
./venv/Scripts/activate
```

#### Linux

```bash
python3 -m venv ./venv/
source venv/bin/activate
```

## Expected Data Formats

The script will automatically scan the `/data/` folder for `.csv` files, populate the database and build a model.
The expected default separator is `\t`.
Fields marked with `*` are optional.

### Student

```
data/STUDENT/student_list.csv
id	first_name*	last_name*	student_email	personal_email*	mobile_phone*	whatsapp*
```

### Unit

```
data/UNIT/unit_list.csv
code	title*

data/UNIT/{UNIT_CODE}/student_list.csv
id	first_name*	last_name*	student_email	semester_year*	semester*

data/UNIT/{UNIT_CODE}/email_list.csv
full_name	student_email
```

### University

```
data/{UNIVERSITY_NAME}
```
