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

## Load Fixture Data

If you are interested in loading fixture data do these steps.

make sure last migration changes applied

```bash
python bimebazar_web/manage.py migrate
```

load the data fixture data into the database

```bash
python bimebazar_web/manage.py loaddata fixture/sample_data.json
```


## Run the server

run the bimebazar task's django app (runserver for development perposes):

```bash
python3 bimebazar_web/manage.py runserver
```

remember you can access the django app on port `8000` on local machine on [http://127.0.0.1:8000](http://127.0.0.1:8000). Also if you load the fixture data there is an admin user with this credentionals: username: `test`, password: `123`.

**Note**: This is a bad practice for real project. I just created this for interview task tests.

