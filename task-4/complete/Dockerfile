FROM openjdk:24-slim
WORKDIR /app
COPY build/libs/*.jar app.jar
ENTRYPOINT ["java","-jar","./app.jar"]