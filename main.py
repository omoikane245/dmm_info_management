from .jobs.abstract_job import AbstractJob
from flask import Request, Response
from importlib import import_module

import functions_framework
import json
import yaml

@functions_framework.http
def main(request: Request) -> Response:
    request_json = request.get_json(silent=True)
    job_id = request_json["job_id"]
    result = get_instance(job_id).execute()
    return Response(response=json.dumps({"status": result.name}))

def get_instance(job_id: str) -> AbstractJob:
    with open("config.yml", "r", encoding="utf-8") as yml:
        config = yaml.safe_load(yml)
        file_name = config["jobs"][f"{job_id}"]["file-name"]
        job_name = config["jobs"][f"{job_id}"]["job-name"]
        module = import_module(f"jobs.{file_name}")
        cls = getattr(module, job_name)
        return cls()
