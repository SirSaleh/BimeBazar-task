# Docker Deployment Guide

This document explain how to run the bimeBazar web application using docker.

First of all, make sure you've installed docker and compose plugin, based on the
[official docs of docker](https://docs.docker.com/compose/install/).

Make sure port 80 on your machine in free

Run the docker image

```bash
docker compose up --build
```

**Note**: First build will may take several minutes based on the internet speed.

After completing the process service must be up at port 80 in the local machine. ([127.0.0.1](http://127.0.0.1))