#!/bin/bash
pushd mongodbMI
#java -cp ./solace-sink-notification-service-0.0.1-SNAPSHOT.jar org.springframework.boot.loader.launch.PropertiesLauncher --spring.config.additional-location=./application.yml
docker run --env-file .env --name mi-mongodb -v /Users/kester/Development/Solace/Demothon2025/team-25/mongodbMI:/config pubsubplus-connector-mongodb:v1.0.0
popd