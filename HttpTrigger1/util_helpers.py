from typing import Union
# from google.auth import default, impersonated_credentials
import functions_framework
from flask import request, g
from werkzeug.exceptions import InternalServerError, BadRequest, NotFound
from jsonschema import ValidationError
from json import dumps
import logging
from traceback import format_exc
# from google.cloud import storage
from util_input_validation import Config

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient

def impersonate_account(signing_account: str, lifetime: int):
    credentials, project = default()
    return impersonated_credentials.Credentials(
        source_credentials=credentials,
        target_principal=signing_account,
        target_scopes="https://www.googleapis.com/auth/devstorage.read_write",
        lifetime=lifetime,
    )
    
# def impersonate_account(tenant_id, client_id, client_secret):
#     # Authenticate using service principal credentials
#     credential = DefaultAzureCredential(
#         tenant_id=tenant_id,
#         client_id=client_id,
#         client_secret=client_secret
#     )
#     return credential

# def create_blob_service_client(account_url, credential):
#     # Create a BlobServiceClient
#     blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
#     return blob_service_client


def create_outgoing_file_ref(file: Union[BlobClient, Config.InputFiles.InputFile]):
    if isinstance(file, BlobClient):
        container_name = file.container_name
        blob_properties = file.get_blob_properties()
        return {
            "bucket_name": str(container_name),
            "full_path": str(file.blob_name),
            "version": str(blob_properties.etag),
            "size": str(blob_properties.size),
            "content_type": str(blob_properties.content_settings.content_type),
            "uploaded": str(blob_properties.last_modified) if blob_properties.last_modified else None,
        }
    elif isinstance(file, Config.InputFiles.InputFile):
        return {
            "bucket_name": str(file.bucket_name),
            "full_path": str(file.full_path),
            "version": str(file.version),
            "size": str(file.size),
            "content_type": str(file.content_type),
            "uploaded": str(file.uploaded.isoformat()) if file.uploaded else None,
        }
    else:
        return {}


@functions_framework.errorhandler(InternalServerError)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    request_json = request.get_json()
    context_json = g.context
    msg = {
        "code": e.code,
        "name": e.name,
        "description": e.description,
        "trace": format_exc(),
    }
    logging.error(dumps({**msg, "context": context_json, "request": request_json}))
    response = e.get_response()
    response.data = dumps(msg)
    response.content_type = "application/json"
    return response


@functions_framework.errorhandler(NotFound)
def handle_not_found(e):
    request_json = request.get_json()
    context_json = g.context
    msg = {"code": e.code, "name": e.name, "description": e.description}
    logging.error(dumps({**msg, "context": context_json, "request": request_json}))
    response = e.get_response()
    response.data = dumps(msg)
    response.content_type = "application/json"
    return response


@functions_framework.errorhandler(BadRequest)
def handle_bad_request(e):
    msg = {
        "code": e.code,
        "name": e.name,
        "description": e.description,
    }
    try:
        request_json = request.get_json()
        context_json = request_json.pop("context")
        if isinstance(e.description, ValidationError):
            original_error = e.description
            msg = {
                **msg,
                "name": "Validation Error",
                "description": original_error.message,
                "trace": original_error.__str__(),
            }
        else:
            msg = {**msg, "trace": format_exc()}
        logging.warning(
            dumps({**msg, "context": context_json, "request": request_json})
        )
    except:
        request_json = request.data
        msg = {**msg, "trace": format_exc()}
        logging.warning(dumps({**msg, "request": str(request_json, "utf-8")}))
    response = e.get_response()
    response.data = dumps(msg)
    response.content_type = "application/json"
    return response
