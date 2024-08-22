import prometheus_client

REQUEST_COUNT = prometheus_client.Counter('request_count', 'Number of requests received')