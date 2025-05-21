# Fraud detection with speach recognition and agent mesh

## install prerequisites

```shell
python3 -m venv .venv 
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Create a .env file by copying sample.env to .env and adjust the proper fields.

```shell
SOLACE_AGENT_MESH_NAMESPACE=team-25/
SOLACE_DEV_MODE=False
SOLACE_BROKER_URL=wss://mr-connection-[serviceId].messaging.solace.cloud:443
SOLACE_BROKER_SMF_URL=tcps://mr-connection-[serviceId].messaging.solace.cloud:55443
SOLACE_BROKER_VPN=[message-vpn-name]
SOLACE_BROKER_USERNAME=solace-cloud-client
SOLACE_BROKER_PASSWORD=[password]
LLM_SERVICE_API_KEY=[llm api key]
LLM_SERVICE_ENDPOINT=https://api.openai.com/v1
LLM_SERVICE_PLANNING_MODEL_NAME=openai/gpt-4o
EMBEDDING_SERVICE_MODEL_NAME=openai/text-embedding-ada-002
EMBEDDING_SERVICE_API_KEY=[llm api key]
EMBEDDING_SERVICE_ENDPOINT=https://api.openai.com/v1
RUNTIME_CONFIG_PATH=build/config.yaml
REST_API_SERVER_INPUT_PORT=5050
REST_API_SERVER_HOST=127.0.0.1
REST_API_SERVER_INPUT_ENDPOINT=/api/v1/request
WEBUI_ENABLED=True
WEBUI_PORT=5001
WEBUI_HOST=localhost
WEBUI_RESPONSE_API_URL=http://127.0.0.1:5050/api/v1/request
WEBUI_FRONTEND_SERVER_URL=http://localhost:5001
WEBUI_FRONTEND_URL=http://localhost:5001
LLM_SERVICE_CODING_MODEL_NAME=
LLM_SERVICE_GENERAL_FAST_MODEL_NAME=
LLM_SERVICE_GENERAL_GOOD_MODEL_NAME=
LLM_SERVICE_REASONING_EXPENSIVE_MODEL_NAME=
LLM_SERVICE_REASONING_NORMAL_MODEL_NAME=
LLM_SERVICE_WRITING_MODEL_NAME=
MONITOR_SLACK_STATUS_CHANNEL=
REST_API_SERVER_INPUT_RATE_LIMIT=
SOLACE_BROKER_BASIC_AUTH=
SOLACE_BROKER_REST_MESSAGING_URL=
WEBUI_FRONTEND_AUTH_LOGIN_URL=
WEBUI_FRONTEND_BOT_NAME=
WEBUI_FRONTEND_COLLECT_FEEDBACK=
WEBUI_FRONTEND_REDIRECT_URL=
WEBUI_FRONTEND_USE_AUTHORIZATION=
WEBUI_FRONTEND_WELCOME_MESSAGE=
WEBUI_LOCAL_DEV=

TEAM25_MONGO_HOST="[mongo db url]"
TEAM25_MONGO_PORT="[mongo port]"
TEAM25_MONGO_USER="[mongo user]"
TEAM25_MONGO_PASSWORD="[mongo password]"
TEAM25_MONGO_DB="finance"
TEAM25_MONGO_COLLECTION="transactions"
TEAM25_DB_PURPOSE="Contains detailed information about transactions."
#TEAM25_DB_DESCRIPTION="Fields: transactionType (string), amount(number), transactionNum, accountNum, currency, timestamp)"
TEAM25_DB_DESCRIPTION=""
TEAM25_AUTO_DETECT_SCHEMA="true"
IMAGE_GEN_ENDPOINT=
IMAGE_GEN_API_KEY=
IMAGE_GEN_MODEL=

INPUT_QUEUE_NAME = "financeQueue"
OUTPUT_TOPIC_NAME = "transaction/checked"
```

make sure to adjust the serviceId of your broker and the credentials, also provide a proper llm api key.

When this is done execute the following command to run the agent mesh:
```shell
source .env
solace-agent-mesh run -b
```

This will spin up the agent mesh.

## configure the broker

Next step is to setup the broker queues:

Go to the UI of the broker and select the demothonteam25 message VPN.
Create the queues for the INPUT_TOPIC_QUEUE and the OUTPUT_TOPIC_QUEUE from the .env file:
Make sure the following subscription is added to the financeQueue: _acmebank/solace/core/>_
and _acmebank/solace/core/>_ to the checkedQueue
Both queues are owned by solace-cloud-client and are set to _Exclusive_

## Connect solace feed

Goto https://feeds.solace.dev/ and select the core banking community feed
Fill in the proper url vpn username and password and select `Start All`. Let it run for a few minutes.

You can use Mongo Compass pointing to your mongodb to check if data is coming in.

## Fraud detection aplication.

This should be converted to some kind of custom agent or custom gateway
cd into the fraud detection folder and start:
```shell
source .env
cd fraud-detector
python3 fraud_detector.py
```

This will tap into the financeQueue and predict possible fraudulous transactions and publish those to the checkedQueue.

## Query database

With the speach module you can ask questions to the agent mesh about details in the mongo db.
Open another terminal

```shell
source .env
cd speach
python3 speach.py
```
The reading of the answer has to be implemented.
