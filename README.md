# ThaiPy Demo on Distributed Tracing

### Presenter

Juti Noppornpitak, a senior software developer at [DNAstack](https://dnastack.com), Toronto, Ontario, Canada.

### Key points

* In this demo, we are using the standard OpenTelemetry.
* While there are [many collectors](https://opentelemetry.io/ecosystem/vendors/) in the market, we will use Jeager for this demo.

### Getting started

* Run `docker compose up -d` to start Jaeger.
  * [Jaeger UI](http://localhost:16686) should be available at http://localhost:16686.
* Set up and run [the S1 app](s1). See its [README](s1/README.md) for more information.
* Set up and run [the S2 app](s2). See its [README](s2/README.md) for more information.

### Test Requests

> The test script requires `httpie` (CLI app).

```shell
http GET localhost:8080/api/notices
```

```shell
http POST localhost:8080/api/notices --raw '{
  "title": "ABC",
  "content": "Sample Content"
}'
```

```shell
http GET localhost:8081/ping/notices/random
```
