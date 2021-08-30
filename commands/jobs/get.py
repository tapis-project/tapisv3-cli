from tapipy.errors import InvalidInputError

def get(client, id) -> None:
    try:
        job = client.jobs.getJob(jobId=id)
        print(job)
        return
    except InvalidInputError:
        print(f"Job not found with id '{id}'")