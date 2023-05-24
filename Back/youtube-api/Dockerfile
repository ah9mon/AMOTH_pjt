# Use an official Java 11 runtime as the base image
FROM adoptopenjdk:11-jdk-hotspot

# Set the working directory inside the container
WORKDIR /app

# Copy the Gradle files
COPY build.gradle .
COPY settings.gradle .
COPY gradlew .

# Copy the Gradle wrapper files
COPY gradle gradle

# Download and install Gradle
RUN ./gradlew --version

# Copy the application source code
COPY src src

# Build the application with Gradle
RUN ./gradlew build -x test

# Copy the application JAR file to the working directory
COPY build/libs/youtube-api-0.0.1-SNAPSHOT.jar youtube-api-0.0.1-SNAPSHOT.jar

# Set the entrypoint command to run the Spring Boot application
ENTRYPOINT ["java", "-jar", "youtube-api-0.0.1-SNAPSHOT.jar"]
