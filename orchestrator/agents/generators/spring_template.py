from __future__ import annotations

from pathlib import Path

from orchestrator.agents.generators.common import write_if_missing


def scaffold_spring_boot_microservice(project_root: Path) -> None:
    service_root = project_root / "apps" / "springboot-microservice"

    write_if_missing(
        service_root / "pom.xml",
        """<project xmlns=\"http://maven.apache.org/POM/4.0.0\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"
  xsi:schemaLocation=\"http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd\">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.example</groupId>
  <artifactId>springboot-microservice</artifactId>
  <version>0.0.1-SNAPSHOT</version>
  <name>springboot-microservice</name>
  <properties>
    <java.version>21</java.version>
    <spring-boot.version>3.3.5</spring-boot.version>
  </properties>

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-dependencies</artifactId>
        <version>${spring-boot.version}</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-test</artifactId>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
      </plugin>
    </plugins>
  </build>
</project>
""",
    )

    write_if_missing(
        service_root / "src" / "main" / "java" / "com" / "example" / "microservice" / "Application.java",
        """package com.example.microservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
""",
    )

    write_if_missing(
        service_root / "src" / "main" / "java" / "com" / "example" / "microservice" / "HealthController.java",
        """package com.example.microservice;

import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController {
    @GetMapping("/healthz")
    public Map<String, String> health() {
        return Map.of("status", "ok");
    }
}
""",
    )

    write_if_missing(
        service_root / "src" / "main" / "resources" / "application.yml",
        """server:
  port: 8080

management:
  endpoints:
    web:
      exposure:
        include: health,info
  endpoint:
    health:
      probes:
        enabled: true
""",
    )

    write_if_missing(
        service_root / "Dockerfile",
        """FROM maven:3.9.9-eclipse-temurin-21 AS build
WORKDIR /workspace
COPY pom.xml .
COPY src ./src
RUN mvn -q -DskipTests package

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /workspace/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
""",
    )

    write_if_missing(
        service_root / "README.md",
        """# Spring Boot Microservice Template

## Best practices included
- Java 21 + Spring Boot 3 baseline.
- Health endpoint and Actuator probes.
- Validation starter included.
- Multi-stage Docker build.
- Small and test-ready project structure.
""",
    )
