import json


def export_status(id: str, status: str, prompt: str, response: str):
    status = {"id": id, "status": status, "prompt": prompt, "response": response}
    return json.dumps(status)
