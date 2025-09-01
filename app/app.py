from flask import Flask, request 
import logging
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from jaeger_client import Config
import opentracing

app = Flask(__name__)

# Logging
logging.basicConfig(filename="/var/log/app/app.log", level=logging.INFO)

# Prometheus metrics
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint"])

# Jaeger Tracing
def init_tracer(service):
    config = Config(
        config={"sampler": {"type": "const", "param": 1},
                "logging": True},
        service_name=service,
    )
    return config.initialize_tracer()

tracer = init_tracer("flask-app")

@app.route("/")
def home():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    with tracer.start_active_span("home-request"):
        logging.info("Home endpoint hit")
        return "Hello, Observability!"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

