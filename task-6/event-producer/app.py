from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json

from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.kafka import KafkaInstrumentor

app = Flask(__name__)

# Инициализация трейсера Jaeger через OpenTelemetry
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "kafka-producer"})
    )
)

jaeger_exporter = OTLPSpanExporter(
    endpoint="jaeger:4317",
    insecure=True
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)

# Kafka продюсер с OpenTelemetry
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Инструментирование Kafka для автотрассировки
KafkaInstrumentor().instrument(producer=producer)

TOPIC = 'topic-sprint4-task6'

@app.route('/send_event', methods=['POST'])
def send_event():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    with tracer.start_as_current_span("send_kafka_event"):
        try:
            producer.send(TOPIC, data)
            producer.flush()
            return jsonify({"status": "message sent", "data": data}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
