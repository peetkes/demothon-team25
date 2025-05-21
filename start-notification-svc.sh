#!/bin/bash
pushd notification
#java -cp ./solace-sink-notification-service-0.0.1-SNAPSHOT.jar org.springframework.boot.loader.launch.PropertiesLauncher --spring.config.additional-location=./application.yml
docker run --name mi-notification-svc -it -v /Users/kester/Development/Solace/Demothon2025/team-25/notification:/config solace-sink-notification:v1.0.0
popd