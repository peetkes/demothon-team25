Make a copy of sample.env and name it `.env`.
Fill in the urls and other information.
Make sure you have the details of your solace broker and  queue name.
Make sure you have the details for your mongodb, database and collection

This will be picked up by the docker run command so it will pass the environment variables into the application yaml

```shell
SOLACE_BROKER_URL=wss://mr-connection-[service_id].messaging.solace.cloud:443
SOLACE_BROKER_SMF_URL=tcps://mr-connection-[service-id].messaging.solace.cloud:55443
SOLACE_BROKER_VPN=[message_vpn_name]
SOLACE_BROKER_USERNAME=[broker_username]
SOLACE_BROKER_PASSWORD=[broker_password]
SOLACE_QUEUE=[queue_name]

TEAM25_MONGODB_MONGO_HOST=[mongo_db_host]
TEAM25_MONGODB_MONGO_PORT=[mongo_db_port]
TEAM25_MONGODB_MONGO_USER=[mongo_username]
TEAM25_MONGODB_MONGO_PASSWORD=[mongo_password]
TEAM25_MONGODB_MONGO_DB=[mongo_database_name]
TEAM25_MONGODB_MONGO_COLLECTION=[mongo_database_collection]

```