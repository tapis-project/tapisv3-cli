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

    def download(self, uuid, output_path) -> None:
        try:
            self.client.jobs.getJobOutputDownload(jobUuid=uuid, outputPath=output_path)
            self.logger.complete(f"Download complete for job {uuid}")
            return
        except InvalidInputError as e:
            self.logger.error(f"{e.message}")

    def get(self, uuid) -> None:
        try:
            job = self.client.jobs.getJob(jobUuid=uuid)
            self.logger.log(job)
            return
        except InvalidInputError:
            self.logger.error(f"Job not found with uuid '{uuid}'")

    def history(self, uuid) -> None:
        try:
            status = self.client.jobs.getJobHistory(jobUuid=uuid)
            self.logger.log(status)

            return
        except InvalidInputError:
            self.logger.error(f"Job not found with uuid '{uuid}'")
            self.exit(1)

    def status(self, uuid) -> None:
        try:
            status = self.client.jobs.getJobStatus(jobUuid=uuid)
            self.logger.log(status)

            return
        except InvalidInputError:
            self.logger.error(f"Job not found with uuid '{uuid}'")
            self.exit(1)

    def list(self) -> None:
        jobs = self.client.jobs.getJobList()
        self.logger.log(jobs)

    # NOTE the requirement on description is a bug in the api. Leave
    # description as required for now
    def submit(self, name, app_id, app_version, description) -> None:
        try:
            job = self.client.jobs.submitJob(name=name, appId=app_id, appVersion=app_version, description=description)
            self.logger.info(f"Job submitted. Uuid: {job.uuid}")
            return
        except InvalidInputError as e:
            self.logger.error(e.message)
            self.exit(1)