# Classic Deployment guid

First cd to the project dir,

create a virtualenv:

```bash
python3 -m venv venv
```

**Note**: venv dir ignored in `.gitignore` file, So it's OK to create in the the project directory itself.

install dependencies:

```bash
pip3 install -r requirements.txt
```

configure the database target in django setting and run the django `migrate`

```bash
python3 bimebazar_web/manage.py migrate
```

run the bimebazar task's django app (runserver for development perposes):

```bash
python3 bimebazar_web/manage.py runserver
```