from core.TapisCommand import TapisCommand
from tapipy.errors import InvalidInputError

class Jobs(TapisCommand):
    def __init__(self):
        TapisCommand.__init__(self)
        self.set_option_set({
            "-f": [ "path_to_file" ],
            "-u": [ "url" ],
            "-j": [ "json" ],
            "--test": []
        })

    def download(self, client, uuid, output_path) -> None:
        try:
            client.jobs.getJobOutputDownload(jobUuid=uuid, outputPath=output_path)
            self.logger.complete(f"Download complete for job {uuid}")
            return
        except InvalidInputError as e:
            self.logger.error(f"{e.message}")

    def get(self, client, uuid) -> None:
        try:
            job = client.jobs.getJob(jobUuid=uuid)
            self.logger.log(job)
            return
        except InvalidInputError:
            self.logger.error(f"Job not found with uuid '{uuid}'")

    def history(self, client, uuid) -> None:
        try:
            status = client.jobs.getJobHistory(jobUuid=uuid)
            self.logger.log(status)

            return
        except InvalidInputError:
            self.logger.error(f"Job not found with uuid '{uuid}'")
            self.exit(1)

    def status(self, client, uuid) -> None:
        try:
            status = client.jobs.getJobStatus(jobUuid=uuid)
            self.logger.log(status)

            return
        except InvalidInputError:
            self.logger.error(f"Job not found with uuid '{uuid}'")
            self.exit(1)

    def list(self, client) -> None:
        jobs = client.jobs.getJobList()
        self.logger.log(jobs)

    # NOTE the requirement on description is a bug in the api. Leave
    # description as required for now
    def submit(self, client, name, app_id, app_version, description) -> None:
        try:
            job = client.jobs.submitJob(name=name, appId=app_id, appVersion=app_version, description=description)
            self.logger.info(f"Job submitted. Uuid: {job.uuid}")
            return
        except InvalidInputError as e:
            self.logger.error(e.message)
            self.exit(1)