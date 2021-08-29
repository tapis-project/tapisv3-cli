from tapipy.tapis import Tapis
from tapipy.errors import InvalidInputError
import sys

tacc_username = sys.argv[1]
tacc_password = sys.argv[2]
job_id = sys.argv[3]

# Authenticate
client = Tapis(base_url= "https://tacc.develop.tapis.io", username=tacc_username, password=tacc_password)
client.get_tokens()

def get_job_by_id() -> None:
    try:
        job = client.jobs.getJob(jobId=job_id)
        print(job)
        return
    except InvalidInputError:
        print(f"Job not found with id '{job_id}'")

if __name__ == "__main__":
    get_job_by_id()