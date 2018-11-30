### npm dependencies web service.

```run.sh``` builds and deploys a docker compose, consisting of the following services:

- MongoDB service (using a persistent volume).
- python/aiohttp based backend/api service (3 replicas).
- nodejs/express based frontend service (3 replicas).
- nginx service.

general performance tuning notes:
- nginx for horizontal scaling.
- backend data retrieval:
  - in-memomry cache of the last N requests.
  - database query when in-memory cache is a miss.
  - parallel http requests via multiprocessing.
- [aiohttp.](http://y.tsutsumi.io/aiohttp-vs-multithreaded-flask-for-high-io-applications.html)

testing:
```run_tests.sh``` executes pytest based functional tests. 

![header image](https://github.com/leongold/dep-view/blob/master/dep-view-demo.png)
