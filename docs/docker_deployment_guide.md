# Docker Deployment Guide

This document explain how to run the bimeBazar web application using docker.

First of all, make sure you've installed docker and compose plugin, based on the
[official docs of docker](https://docs.docker.com/compose/install/).

Make sure port 80 on your machine in free

Run the docker image (`-d` for detached mode)

```bash
sudo docker compose up -d --build
```

**Note**: First build will may take several minutes based on the internet speed.

After completing the process service must be up at port 8000 in the local machine. ([127.0.0.1:8000](http://127.0.0.1:8000))


## Loading the Data Fixture

first use bash in the `web` service

```bash
sudo docker compose exec web sh
```

inside the container change directory the django app

```bash
cd bimebazar_web/ 
```

make sure last migration changes applied

```bash
python manage.py migrate
```

load the data fixture data into the database

```bash
python manage.py loaddata fixture/sample_data.json
```

if you load the fixture data there is an admin user with this credentionals: username: `test`, password: `123`.

**Note**: This is a bad practice for real project. I just created this for interview task tests.