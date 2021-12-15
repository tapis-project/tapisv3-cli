import json

from tapipy.errors import NotAuthorizedError

from packages.jupyterscinco.JupSciController import JupSciController
from packages.jupyterscinco.utils.build_config import build_config
from utils.Prompt import prompt


class Configs(JupSciController):
    # Creates a config
    def create_Action(self, tenant, instance):
        config = build_config(tenant, instance, self.config_type, group=self.group)
        
        meta = {
            "name": config,
            "value": {
                "tenant": tenant,
                "instance": instance,
                "images": [],
                "config_type": "tenant",
                "volume_mounts": [],
            }
        }

        try:
            self.client.meta.createDocument(
                db=self.get_config("database"),
                collection=self.get_config("collection"),
                basic='true',
                request_body=meta
            )
        except NotAuthorizedError:
            self.logger.error("You are not authorized to perform this action")
            self.exit(1)

        self.logger.complete(f"Tenant config '{config}' created")
        self.set_view("JupSciMetaView", meta)
        self.view.render()
    
    # Delete a config
    def delete_Action(self, tenant, instance):
        config = build_config(tenant, instance, self.config_type, group=self.group)
        if prompt.confirm(f"Confirm deletion of config '{config}'"):
            meta = self._get(tenant, instance)
            self.client.meta.deleteDocument(
                db=self.get_config("database"),
                collection=self.get_config("collection"),
                docId=meta["_id"]["$oid"]
            )

            self.logger.complete(f"Tenant config '{config}' deleted")

    # Fetch a config from the database and collection specified in the configs
    def get_Action(self, tenant, instance):
        result = self._get(tenant, instance)

        self.set_view("JupSciMetaView", result)
        self.view.render()
    
    # Update a specific key for a given config
    def patch_Action(self, tenant, instance, key, value):
        meta = self._get(tenant, instance)["value"]
        meta[key] = value
        self.client.meta.modifyDocument(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            request_body=meta,
            docId=meta["_id"]["$oid"]
        )

        self.set_view("JupSciMetaView", meta)
        self.view.render()

    # Lists all configs in the collection
    def list_Action(self):
        metadata = self.client.meta.listDocuments(
            db=self.get_config("database"),
            collection=self.get_config("collection")
        )
        
        self.set_view("JupSciMetaView", json.loads(metadata))
        self.view.render()

    # Updates the entire value for a given config
    def put_Action(self, tenant, instance, value):
        meta = self._get(tenant, instance)
        meta["value"] = value
        self.client.meta.modifyDocument(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            request_body=meta,
            docId=meta["_id"]["$oid"]
        )

        self.set_view("JupSciMetaView", meta)
        self.view.render()

    # Convenience method to fetch a config from the database without rendering the result
    # to the shell
    def _get(self, tenant, instance):
        filter_obj = {"name": build_config(tenant, instance, self.config_type, group=self.group)}
        metadata = self.client.meta.listDocuments(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            filter=json.dumps(filter_obj)
        )

        return json.loads(metadata)[0]