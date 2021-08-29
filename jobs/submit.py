from tapipy.tapis import Tapis
from tapipy.errors import InvalidInputError
import sys
tacc_username = sys.argv[1]
tacc_password = sys.argv[2]
job_name = sys.argv[3]
app_id = sys.argv[4]
app_version = sys.argv[5]

client = Tapis(base_url= "https://tacc.develop.tapis.io", username=tacc_username, password=tacc_password)
client.get_tokens()

def submit_job() -> None:
    try:
        client.jobs.submitJob(name=job_name, appId=app_id, appVersion=app_version)
        return
    except InvalidInputError as e:
        print(e.message)


if __name__ == "__main__":
    submit_job()