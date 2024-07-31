# Roadmap Planning

The task send in `pdf` format can seen `/task_planning/BimeBazar-Backend-Task.pdf`.

## Roadmap

The road map I predict we need to satisfy the requirements of the project. 

| Step | Description | degree of necessity |
| ---- | ----------- | ------- |
| Initialize the git repository |  | MUST HAVE |
| Initialize a bare django project | | MUST HAVE |
| Add a dockerfile at first (change the dockerfile after each next step if required) | | MUST HAVE |
| Design DB schema (django models) | Schema defined in this project should be Based on the requirements in BimeBazar Task file | MUST HAVE |
| Add a fixture to seed the data (If there is enough time) | | COULD HAVE |
| Add django admin for the models | | SHOULD HAVE |
| Create Base router for DRF and add related urls to django url pattern | | MUST HAVE |
| Define DRF viewsets for required APIs | Unit-tests included, DRF viewsets required for this project | MUST HAVE |
| Add swagger docs (If there is enough time) | | SHOULD HAVE |


**Note**: `degree of necessity` is defined like below:

| degree | description |
| ------ | ----------- |
| MUST HAVE | These cases are mandatory |
| SHOULD HAVE | These cases are required but in second place (after MUST HAVE ones) |
| COULD HAVE | These cases are a plus, so we try to do it if there is enough time |