def list_jobs(client) -> None:
    jobs = client.jobs.getJobList()
    print(jobs)
