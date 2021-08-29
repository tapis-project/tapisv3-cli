from tapipy.tapis import Tapis
import sys

tacc_username = sys.argv[1]
tacc_password = sys.argv[2]

# Authenticate
client = Tapis(base_url= "https://tacc.develop.tapis.io", username=tacc_username, password=tacc_password)
client.get_tokens()

def list_jobs() -> None:
    print(dir(client.jobs))
    jobs = client.jobs.getJobList()
    print(jobs)

if __name__ == "__main__":
    list_jobs()
