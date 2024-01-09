###############################################
#############  Sample Curl ####################
###############################################

#!/bin/bash

# Replace with your Azure Function App URL
###"https://<function-app-name>.azurewebsites.net/api/<function-key>"
function_url="https://<function-app-name>.azurewebsites.net/api/<function-key>"

# Replace with your Azure Function App key or any other authentication mechanism
api_key="<function-key>"  ###"Function-key"
set -x

curl -m 59 -X POST "$function_url" -H "x-functions-key: $api_key" -H "Content-Type: application/json" -d '{"context": {"azure_subscription": "dev-sub","azure_location": "east us","client_id": "customer1"},"input_files": {"source_file": {"bucket_name": "247ai-stg-cca-customer1-audio-landing","full_path": "1685951506932890_Daniel_and_Gus_1.wav","version": "0x8DC10DFBCC614FA","uploaded": "2024-01-09T12:23:51Z"}},"function_config": {"label_tags": {"client": "ci_client","step": "ci_step","type": "ci_media_type"},"functions": {"deepgram": ["deepgram"]},"config_bucket_name": "247ai-stg-cca"}}'

#####################################
#################### OR #############
#!/bin/bash

# Replace with your Azure Function App URL
###"https://<function-app-name>.azurewebsites.net/api/<function-key>"
function_url="https://<function-app-name>.azurewebsites.net/api/<function-key>"

# Replace with your Azure Function App key or any other authentication mechanism
api_key="<function-key>"  ###"your-api-key"
set -x

curl -m 59 -X POST "$function_url" \
-H "x-functions-key: $api_key" \
-H "Content-Type: application/json" \
-d '{
    "context": {
        "azure_subscription": "dev-sub",
        "azure_location": "east us",
        "client_id": "customer1"
    },
    "input_files": {
        "source_file": {
            "bucket_name": "247ai-stg-cca-customer1-audio-landing",
            "full_path": "1685951506932890_Daniel_and_Gus_1.wav",
            "version": "0x8DC10DFBCC614FA",
            "uploaded": "2024-01-09T12:23:51Z"
        }
    },
    "function_config": {
        "label_tags": {
            "client": "ci_client",
            "step": "ci_step",
            "type": "ci_media_type"
        },
        "functions": {
            "deepgram": ["deepgram"]
        },
        "config_bucket_name": "247ai-stg-cca"
    }
}'
