### npm dependencies web service.

*deployment*:

```run.sh``` builds and deploys a docker compose, consisting of the following services:

- MongoDB service (using a persistent volume).
- python/aiohttp based backend/api service (3 replicas).
- nodejs/express based frontend service (3 replicas).
- nginx service.

*usage*:
- ```http://localhost:8080/<package>/<version>``` displays a tree view of the dependencies.
- ```http://localhost:8080/api/<package>/<version>``` returns a json representation of the dependencies.

*general performance tuning notes*:
- nginx for horizontal scaling.
- backend data retrieval:
  - in-memomry cache of the last N requests.
  - database query when in-memory cache is a miss.
  - parallel http requests via multiprocessing.
- [aiohttp.](http://y.tsutsumi.io/aiohttp-vs-multithreaded-flask-for-high-io-applications.html)
- TODO: database horizontal scaling/sharding!

*testing*:
```run_tests.sh``` executes pytest based functional tests. 

![header image](https://github.com/leongold/dep-view/blob/master/dep-view-demo.png)
