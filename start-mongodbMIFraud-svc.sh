#!/bin/bash
pushd mongodbMIFraud
#java -cp ./solace-sink-notification-service-0.0.1-SNAPSHOT.jar org.springframework.boot.loader.launch.PropertiesLauncher --spring.config.additional-location=./application.yml
docker run --env-file .env --name mi-mongodb-fraud -v /Users/kester/Development/Solace/Demothon2025/team-25/mongodbMIFraud:/config pubsubplus-connector-mongodb:v1.0.0
popd