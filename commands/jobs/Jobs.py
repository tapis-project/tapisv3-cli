from core.Command import Command
from tapipy.errors import InvalidInputError

class Jobs(Command):
    def __init__(self):
        Command.__init__(self)
        self.set_option_set({
            "-f": [ "path_to_file" ],
            "-u": [ "url" ],
            "-j": [ "json" ],
            "--test": []
        })

    def get(self, client, id) -> None:
        try:
            job = client.jobs.getJob(jobId=id)
            print(job)
            return
        except InvalidInputError:
            print(f"Job not found with id '{id}'")

    def list(self, client) -> None:
        jobs = client.jobs.getJobList()
        print(jobs)

    def submit(self, client, name, id, version) -> None:
        try:
            client.jobs.submitJob(name=name, appId=id, appVersion=version)
            return
        except InvalidInputError as e:
            print(e.message)