import json

from datetime import datetime

from tapipy.errors import InvalidInputError

from packages.tapiscustom.TapisController import TapisController


class Jobs(TapisController):
    """Contains all of the CRUD functions associated with jobs."""
    def __init__(self):
        TapisController.__init__(self)

    def cancel_Action(self, uuid) -> None:
        """Cancel a job that has been submitted."""
        try:
            self.client.jobs.cancelJob(jobUuid=uuid)
            self.logger.newline(1)
            self.logger.complete(f"Job '{uuid}' successfully cancelled\n")
            return
        except InvalidInputError as e:
            self.logger.error(f"{e.message}\n")
            return

    def download_Action(self, uuid, output_path) -> None:
        """Downloads the output of a completed job."""
        try:
            self.client.jobs.getJobOutputDownload(jobUuid=uuid, outputPath=output_path)
            self.logger.complete(f"Download complete for job '{uuid}'\n")
            return
        except InvalidInputError as e:
            self.logger.error(f"{e.message}\n")
            return

    def get_Action(self, uuid) -> None:
        """Retrieve the details of a specified job."""
        try:
            job = self.client.jobs.getJob(jobUuid=uuid)
            self.logger.log(job)
            self.logger.newline(1)
            return
        except InvalidInputError:
            self.logger.error(f"Job not found with UUID '{uuid}'\n")
            return

    def history_Action(self, uuid) -> None:
        """Retrieve the computation history of a specified job."""
        try:
            status = self.client.jobs.getJobHistory(jobUuid=uuid)
            self.logger.log(status)
            self.logger.newline(1)
            return
        except InvalidInputError:
            self.logger.error(f"Job not found with UUID '{uuid}'\n")
            self.exit(1)

    def list_Action(self) -> None:
        """Retrieve the current list of submitted jobs."""
        jobs = self.client.jobs.getJobList()
        self.logger.log(jobs)

        return

    def output_Action(self, uuid, output_path) -> None:
        """Displays the output files produced from a completed job."""
        try:
            self.client.jobs.getJobOutputList(jobUuid=uuid, outputPath=output_path)
            self.logger.newline(1)
            self.logger.complete(f"Download complete for job '{uuid}'\n")
            return
        except InvalidInputError as e:
            self.logger.error(f"{e.message}\n")
            return

    def status_Action(self, uuid) -> None:
        """Retrieve the current operational status of a specified job."""
        try:
            status = self.client.jobs.getJobStatus(jobUuid=uuid)
            self.logger.log(status)
            self.logger.newline(1)
            return
        except InvalidInputError:
            self.logger.error(f"Job not found with UUID '{uuid}'\n")
            self.exit(1)

    def submit_Action(self, app_id, app_version, *args) -> None:
        """Submit a job to be run using a specified application and its version."""
        # Set the name and description to datetime-appid-username
        name = f"{datetime.now()}-{app_id}-{self.client.username}"
        description = name
        # If the user specified args after the appid and appversion, we assume they
        # are passing name in the first arg and description in the second
        name = args[0] if len(args) >= 1 else name
        description = args[0] if len(args) > 1 else description

        try:
            job = self.client.jobs.submitJob(name=name, appId=app_id, appVersion=app_version, description=description)
            self.logger.info(f"Job submitted. UUID: {job.uuid}\n")
            return
        except InvalidInputError as e:
            self.logger.error(f"{e.message}\n")
            self.exit(1)

    def submit_def_Action(self, job_definition_file, *args) -> None:
        """ 
        Submit a job using a custom job JSON definition file. 
        The job request body can contain more file inputs than are specified
        in the application, as long as strictFileInputs is set to 'false' in
        the system.
        """
        job_request = json.loads(open(job_definition_file, "r").read())

        try:
            job = self.client.jobs.submitJob(**job_request)
            self.logger.info(f"Job submitted. UUID: {job.uuid}\n")
            return
        except InvalidInputError as e:
            self.logger.error(f"{e.message}\n")
            self.exit(1)

    def resubmit_Action(self, uuid) -> None:
        """Re-submit a job using a specified job UUID."""
        # TODO Some error -> With the tables on the Java side?
        try:
            self.client.jobs.resubmitJob(jobuuid=uuid)
            self.logger.info(f"Job resubmitted. UUID: {uuid}\n")
            return
        except InvalidInputError as e:
            self.logger.error(f"{e.message}\n")
            self.exit(1)