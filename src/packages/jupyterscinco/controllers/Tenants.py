import json

from tapipy.errors import NotAuthorizedError

from packages.tapis.TapisController import TapisController


class Tenants(TapisController):
    def create_Action(self):
        meta = {
            "name": f"{self.settings.CONFIG}",
            "value": {
                "tenant": self.get_config("tenant"),
                "instance": self.get_config("instance"),
                "user": [],
                "images": [],
                "config_type": "tenant",
                "volume_mounts": [],
                "name": f"{self.settings.CONFIG}"
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

        self.logger.complete(f"Tenant config '{self.settings.CONFIG}' created")
        self.set_view("TapisResultTableView", meta)
        self.view.render()
        
    def delete_Action(self):
        meta = self.get_Action()
        self.client.meta.deleteDocument(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            docId=meta["_id"]["$oid"]
        )

        self.logger.complete(f"Tenant config '{self.settings.CONFIG}' deleted")

    def get_Action(self):
        result = self._get()

        self.set_view("TapisResultTableView", result)
        self.view.render()
    
    def patch_Action(self, key, value):
        meta = self._get()["value"]
        meta[key] = value
        self.modify_Action(meta)

    def list_Action(self):
        filter_obj = {'name':{'$regex':f"{self.settings.CONFIG}"}}
        metadata = self.client.meta.listDocuments(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            filter=json.dumps(filter_obj)
        )
        
        self.set_view("JupSciMetaView", json.loads(metadata))
        self.view.render()

    def list_all_Action(self):
        metadata = self.client.meta.listDocuments(
            db=self.get_config("database"),
            collection=self.get_config("collection")
        )
        
        self.set_view("JupSciMetaView", json.loads(metadata))
        self.view.render()

    def put_Action(self, value):
        meta = self.get_Action()
        meta["value"] = value
        self.client.meta.modifyDocument(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            request_body=meta,
            docId=meta["_id"]["$oid"]
        )

        self.set_view("TapisResultTableView", meta)
        self.view.render()

    def _get(self):
        filter_obj = {"name": self.settings.CONFIG}
        metadata = self.client.meta.listDocuments(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            filter=json.dumps(filter_obj)
        )

        return json.loads(metadata)[0]