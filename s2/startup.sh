#!/usr/bin/env bash
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true

opentelemetry-instrument \
    --exporter_otlp_traces_endpoint "http://127.0.0.1:4317" \
    --exporter_otlp_traces_insecure "true" \
    --metrics_exporter none \
    --logs_exporter none \
    --service_name s2 \
    --traces_exporter console,otlp \
    uvicorn app:app --port 8081
