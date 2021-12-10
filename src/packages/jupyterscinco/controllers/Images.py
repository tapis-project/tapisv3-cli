import json

from packages.jupyterscinco.JupSciController import JupSciController
from utils.Prompt import prompt


class Images(JupSciController):
    def add_Action(self, tenant, instance):
        meta = self._get(tenant, instance)

        display_name = prompt.text("displayName")
        name = prompt.text("name")

        meta["value"]["images"].append({"displayName": display_name, "name": name})

        self.client.meta.modifyDocument(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            request_body=meta,
            docId=meta["_id"]["$oid"]
        )

        self.set_view("JupSciMetaView", meta)
        self.view.render()

    def list_Action(self, tenant, instance):
        meta = self._get(tenant, instance)
        images = meta["value"]["images"]

        self.set_view("DictTable", images)
        self.view.render()

    def remove_Action(self, tenant, instance):
        meta = self._get(tenant, instance)
        images = meta["value"]["images"]

        removed_image_name = prompt.select(
            "Choose an image to remove", 
            [image["name"] for image in images])

        modified_images = [image for image in images if image["name"] != removed_image_name]

        meta["value"]["images"] = modified_images

        self.client.meta.modifyDocument(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            request_body=meta,
            docId=meta["_id"]["$oid"]
        )

        self.logger.complete(f"Removed image '{removed_image_name}'")

    # Convenience method to fetch a config from the database without rendering the result
    # to the shell
    def _get(self, tenant, instance):
        filter_obj = {"name": self._build_config(tenant, instance)}
        result = self.client.meta.listDocuments(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            filter=json.dumps(filter_obj)
        )

        meta = json.loads(result)
        if len(meta) > 0:
            return meta[0]
            
        self.logger.error("Invalid tenant or instance")
        self.exit(1)