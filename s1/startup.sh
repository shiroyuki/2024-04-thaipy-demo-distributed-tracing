#!/usr/bin/env bash
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true

opentelemetry-instrument \
    --exporter_otlp_traces_endpoint "http://127.0.0.1:4317" \
    --exporter_otlp_traces_insecure "true" \
    --metrics_exporter none \
    --logs_exporter none \
    --service_name s1 \
    --traces_exporter console,otlp \
    flask run -p 8080
