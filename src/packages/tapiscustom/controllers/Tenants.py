from tapipy.errors import InvalidInputError

from packages.tapiscustom.TapisController import TapisController


class Tenants(TapisController):
    """Contains all CRUD functions associated with tenants."""
    def __init__(self):
        TapisController.__init__(self)

    def get_Action(self, tenant_id) -> None:
        """Retrieve the details of a specified tenant."""
        try:
            tenant = self.client.tenants.get_tenant(tenantId=tenant_id)
            self.logger.log(tenant)
            self.logger.newline(1)
            return
        except InvalidInputError:
            self.logger.error(f"Tenant not found with id '{tenant_id}'\n")
            return

    def list_Action(self) -> None:
        """List every tenant on the site."""
        tenants = self.client.tenants.list_tenants()
        if len(tenants) > 0:
            self.logger.newline(1)
            for tenant in tenants:
                self.logger.log(tenant.tenant_id)
            self.logger.newline(1)
            return

        self.logger.error(f"No tenants found\n")
        return
