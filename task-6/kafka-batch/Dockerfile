FROM openjdk:24-slim
WORKDIR .
COPY opentelemetry-javaagent.jar opentelemetry-javaagent.jar
COPY build/libs/*.jar app.jar
# Использование opentelemetry агента. В трейс будут попадать все вызовы - много информации.
ENTRYPOINT ["java","-javaagent:/opentelemetry-javaagent.jar","-Dotel.service.name=kafka-batch","-Dotel.exporter.otlp.protocol=grpc","-Dotel.exporter.otlp.endpoint=http://jaeger:4317","-jar","/app.jar"]
#ENTRYPOINT ["java","-jar","/app.jar"]

