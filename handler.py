import runpod
import requests
import os

SEG_SERVER_URL = "http://127.0.0.1:8083"

def handler(job):
    """
    Handles incoming jobs and routes them to the appropriate server.
    """
    job_input = job.get("input")
    
    # Validate job input
    if not job_input:
        return {"error": "Missing input data"}

    # Route to the appropriate server
    try:
        response = requests.post(SEG_SERVER_URL, json=job_input)

        if response.status_code != 200:
            return {"error": f"Server responded with status {response.status_code}", "details": response.text}
        
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    runpod.serverless.start({"handler": handler})
