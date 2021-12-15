import json

from packages.jupyterscinco.JupSciController import JupSciController
from packages.jupyterscinco.utils.build_config import build_config
from utils.Prompt import prompt


class Mounts(JupSciController):
    def add_Action(self, tenant, instance):
        meta = self._get(tenant, instance)

        mount_type = prompt.select("type", ["nfs"])
        path = prompt.text("path", description="[required]")
        mount_path = prompt.text("mountPath", description="[required]")
        readonly = prompt.select_bool("readOnly")
        server = prompt.text("server", required=False)

        mount = {
            "type": mount_type, 
            "path": path,
            "mountPath": mount_path,
            "readOnly": readonly,
        }

        if server is not None:
            mount["server"] = server

        meta["value"]["volume_mounts"].append(mount)

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
        mounts = meta["value"]["volume_mounts"]

        self.set_view("DictTable", mounts)
        self.view.render()

    def remove_Action(self, tenant, instance):
        meta = self._get(tenant, instance)
        mounts = meta["value"]["volume_mounts"]

        removed_mount_path = prompt.select(
            "Choose a mount to remove", 
            [mount["mountPath"] for mount in mounts])

        modified_mounts = [mount for mount in mounts if mount["mountPath"] != removed_mount_path]

        meta["value"]["volume_mounts"] = modified_mounts

        self.client.meta.modifyDocument(
            db=self.get_config("database"),
            collection=self.get_config("collection"),
            request_body=meta,
            docId=meta["_id"]["$oid"]
        )

        self.logger.complete(f"Removed mount '{removed_mount_path}'")

    # Convenience method to fetch a config from the database without rendering the result
    # to the shell
    def _get(self, tenant, instance):
        filter_obj = {"name": build_config(tenant, instance, self.config_type, group=self.group)}
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