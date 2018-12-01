### npm dependencies web service.

*deployment*:

```run.sh``` builds and deploys a docker compose, consisting of the following services:

- MongoDB service (3 replicas for alphabetical sharding; persistent volumes).
- python/aiohttp based backend/api service (N replicas).
- nodejs/express based frontend service (N replicas).
- nginx service.

*usage*:
- ```/<package>/<version>``` displays a tree view of the dependencies.
- ```/api/<package>/<version>``` returns a json representation of the dependencies.

*general performance tuning notes*:
- nginx for horizontal scaling.
- alphabetical database sharding (a-i; j-q; r-z).
- backend data retrieval:
  - in-memomry cache of the last N requests.
  - database query when in-memory cache is a miss.
  - parallel http requests via multiprocessing when database query is a miss.
  - [aiohttp.](http://y.tsutsumi.io/aiohttp-vs-multithreaded-flask-for-high-io-applications.html)

*testing*:

- ```run_tests.sh``` executes pytest based functional tests. 

*roadmap*:
- CI.

![header image](https://github.com/leongold/dep-view/blob/master/dep-view-demo.png)
