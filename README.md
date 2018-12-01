### npm dependencies web service.

*deployment*:

```up.sh``` builds and deploys a docker compose, consisting of the following services:

- MongoDB service (3 replicas for alphabetical sharding; persistent volumes).
- python/aiohttp based backend/api service (3 replicas).
- nodejs/express based frontend service (3 replicas).
- nginx service.

*usage*:
- ```/<package>/<version>``` displays a tree view of the dependencies.
- ```/api/<package>/<version>``` returns a json representation of the dependencies.

*performance*:
- nginx for horizontal scaling.
- [aiohttp.](http://y.tsutsumi.io/aiohttp-vs-multithreaded-flask-for-high-io-applications.html)
- alphabetical database sharding (a-i; j-q; r-z).
- frontend server in-memory cache of the last N requests.
- frontend->backend data retrieval:
  - executed when frontend server in-memory cache is a miss.
  - database query when backend in-memory cache is a miss.
  - parallel http requests via multiprocessing when database query is a miss.

*testing*:

- ```run_tests.sh``` executes pytest based functional tests.

*how usable is this?*

This is a demonstration, and as such...
- error handling is very lackluster.
- practically not configurable; a lot is hardcoded.


![header image](https://github.com/leongold/dep-view/blob/master/dep-view-demo.png)
