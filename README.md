### npm dependencies web service.

*what is this?*

This is a set of services that efficiently fetch, store, and serve
queries for npm dependencies. Unlike with `registry.npmjs.org`, an entire
dependency tree is returned.

I'd like to showcase several methods for improving query latency and
service scalability in a container environment.

*how usable is this?*

This is primarily a demonstration, and as such...
- error handling is very lackluster.
- practically not configurable; a lot is hardcoded.

Barring the above, pretty usable!

*deployment*:

```up.sh``` builds and deploys a docker compose, consisting of the following services:

- MongoDB service (3 instances for alphabetical sharding; persistent volumes).
- python/aiohttp based backend/api service (3 replicas).
- nodejs/express based frontend service (3 replicas).
- nginx service.

*usage*:

nginx is configured to expose to port 8080.
- ```/<package>/<version>``` displays a tree view of the dependencies (see example below).
- ```/api/<package>/<version>``` returns a json representation of the dependencies.

*performance*:
- nginx for horizontal scaling.
- [aiohttp.](http://y.tsutsumi.io/aiohttp-vs-multithreaded-flask-for-high-io-applications.html)
- alphabetical database sharding (a-i; j-q; r-z).
- frontend server in-memory cache of the last N requests.
- frontend->backend data retrieval:
  - executed when frontend server in-memory cache is a miss.
  - database query when backend in-memory cache is a miss.
  - multithreaded http requests when database query is a miss.
  - each (not previously stored) subtree in the tree is stored throughout the query.

*testing*:

- ```run_tests.sh``` executes pytest based functional tests.

![header image](https://github.com/leongold/dep-view/blob/master/dep-view-demo.png)
