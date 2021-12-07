import json

from packages.jupyterscinco import settings
from packages.tapis.TapisController import TapisController

class Meta(TapisController):
    def get_config_Action(self):
        filter_obj = {"name": settings.CONFIG}
        metadata = self.client.meta.listDocuments(
            db=settings.DATABASE,
            collection=settings.COLLECTION,
            filter=json.dumps(filter_obj)
        )
        self.logger.log(json.loads(metadata)[0])

    def list_group_Action(self):
        filter_obj = {'name':{'$regex':f".*group.{settings.CONFIG}"}}
        metadata = self.client.meta.listDocuments(
            db=settings.DATABASE,
            collection=settings.COLLECTION,
            filter=json.dumps(filter_obj)
        )
        return json.loads(metadata)

    def get_group_Action(self, group):
        filter_obj = {'name': f"{group}.group.{settings.CONFIG}"}
        metadata = self.client.meta.listDocuments(
            db=settings.DATABASE,
            collection=settings.COLLECTION,
            filter=json.dumps(filter_obj)
        )
        return json.loads(metadata)[0]
    
    def create_group_Action(self, group):
        meta = {
            "name": f"{group}.group.{settings.CONFIG}",
            "value": {
                "tenant": settings.TENANT,
                "instance": settings.INSTANCE,
                "user": [],
                "images": [],
                "config_type": "group",
                "volume_mounts": [],
                "group_name": group,
                "name": f"{group}.group.{settings.CONFIG}"
            }
        }
        self.client.meta.createDocument(
            db=settings.DATABASE,
            collection=settings.COLLECTION,
            basic='true',
            request_body=meta
        )
    
    def modify_group_Action(self, group, value):
        meta = self.get_tapis_group_config_metadata(group)
        meta["value"] = value
        print(meta)
        self.client.meta.modifyDocument(
            db=settings.DATABASE,
            collection=settings.COLLECTION,
            request_body=meta,
            docId=meta['_id']['$oid']
        )

    def rename_group_Action(self, group, new_group):
        meta = self.get_tapis_group_config_metadata(group)
        new_meta_name = f"{new_group}.group.{settings.CONFIG}"
        meta["name"] = new_meta_name
        meta["value"]["group_name"] = new_group
        meta["value"]["name"] = new_meta_name
        self.client.meta.modifyDocument(
            db=settings.DATABASE,
            collection=settings.COLLECTION,
            request_body=meta,
            docId=meta["_id"]["$oid"]
        )

    def delete_group_Action(self, group):
        meta = self.get_tapis_group_config_metadata(group)
        self.client.meta.deleteDocument(
            db=settings.DATABASE,
            collection=settings.COLLECTION,
            docId=meta['_id']['$oid']
        )

    # def get_admin_tenant_metadata():
    #     ag = Agave(api_server=settings.AGAVE_API, token=settings.AGAVE_SERVICE_TOKEN)
    #     metadata = ag.meta.listMetadata()
    #     matching = []
    #     for entry in metadata:
    #         if 'admin_users' in entry['value'] and settings.TENANT in entry['value']['admin_users']:
    #             matching.append(entry)
    #     return matching

    def modify_Action(self, value):
        meta = self.get_tapis_config_metadata()
        meta['value'] = value
        self.client.meta.modifyDocument(db=settings.DATABASE, collection=settings.COLLECTION, request_body=meta, docId=meta['_id']['$oid'])


    def set_config(self, key, value):
        current = self.get_config_metadata()['value']
        current[key] = value
        self.write_config_metadata(current)