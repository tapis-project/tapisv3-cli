import json

from tapipy.errors import NotAuthorizedError

from packages.tapis.TapisController import TapisController


class Meta(TapisController):
    def get_config_Action(self, render=True):
        filter_obj = {"name": self.settings.CONFIG}
        metadata = self.client.meta.listDocuments(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            filter=json.dumps(filter_obj)
        )
        result = json.loads(metadata)[0]

        if render:
            self.set_view("TapisResultTableView", result)
            self.view.render()

        return result

    def list_group_Action(self):
        filter_obj = {'name':{'$regex':f".*group.{self.settings.CONFIG}"}}
        metadata = self.client.meta.listDocuments(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            filter=json.dumps(filter_obj)
        )

        self.set_view("TapisResultTableView", json.loads(metadata))
        self.view.render()

    def get_group_Action(self, group, render=True):
        filter_obj = {'name': f"{group}.group.{self.settings.CONFIG}"}
        metadata = self.client.meta.listDocuments(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            filter=json.dumps(filter_obj)
        )

        result = json.loads(metadata)[0]

        if render:
            self.set_view("TapisResultTableView", result)
            self.view.render()

        return result
    
    def create_group_Action(self, group):
        meta = {
            "name": f"{group}.group.{self.settings.CONFIG}",
            "value": {
                "tenant": self.get_config("tenant"),
                "instance": self.get_config("instance"),
                "user": [],
                "images": [],
                "config_type": "group",
                "volume_mounts": [],
                "group_name": group,
                "name": f"{group}.group.{self.settings.CONFIG}"
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

        self.logger.complete(f"Group config '{group}.group.{self.settings.CONFIG}' created")
        self.set_view("TapisResultTableView", meta)
        self.view.render()
    
    def modify_group_Action(self, group, value):
        meta = self.get_group_Action(group, render=False)
        meta["value"] = value
        
        self.client.meta.modifyDocument(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            request_body=meta,
            docId=meta['_id']['$oid']
        )

        self.set_view("TapisResultTableView", meta)
        self.view.render()

    def rename_group_Action(self, group_name, new_group_name):
        meta = self.get_group_Action(group_name, render=False)
        new_meta_name = f"{new_group_name}.group.{self.settings.CONFIG}"
        meta["name"] = new_meta_name
        meta["value"]["group_name"] = new_group_name
        meta["value"]["name"] = new_meta_name
        self.client.meta.modifyDocument(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            request_body=meta,
            docId=meta["_id"]["$oid"]
        )

        self.logger.complete(f"Group '{group_name}.group.{self.settings.CONFIG}' renamed to '{new_group_name}.group.{self.settings.CONFIG}'")

    def delete_group_Action(self, group):
        meta = self.get_group_Action(group, render=False)
        self.client.meta.deleteDocument(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            docId=meta["_id"]["$oid"]
        )

        self.logger.complete(f"Group '{group}' deleted")

    # def get_admin_tenant_metadata():
    #     ag = Agave(api_server=settings.AGAVE_API, token=settings.AGAVE_SERVICE_TOKEN)
    #     metadata = ag.meta.listMetadata()
    #     matching = []
    #     for entry in metadata:
    #         if 'admin_users' in entry['value'] and self.get_config("tenant") in entry['value']['admin_users']:
    #             matching.append(entry)
    #     return matching

    def modify_Action(self, value):
        meta = self.get_config_Action(render=False)
        meta["value"] = value
        self.client.meta.modifyDocument(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            request_body=meta,
            docId=meta["_id"]["$oid"]
        )

        self.set_view("TapisResultTableView", meta)
        self.view.render()

    def set_config_Action(self, key, value):
        meta = self.get_config_Action(render=False)["value"]
        meta[key] = value
        self.modify_Action(meta)

    def set_group_Action(self, key, value):
        meta = self.get_group_Action(render=False)["value"]
        meta[key] = value
        self.modify_group_Action(meta)