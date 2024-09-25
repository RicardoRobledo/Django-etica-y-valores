from django.db import models

from etica_y_valores.base.models import BaseModel


class EnterpriseModel(BaseModel):
    """
    This model define an enterprise

    Attributes:
        branch_name (str): enterprise name
        state (str): state of the branch
    """

    class Meta:
        verbose_name = 'Enterprise'
        verbose_name_plural = 'Enterprises'

    enterprise_name = models.CharField(
        unique=True, max_length=255, null=False, blank=False)
    state = models.CharField(max_length=255, null=False, blank=False)
    subdomain = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.enterprise_name

    def __repr__(self):
        return f"EnterpriseModel(enterprise_name={self.enterprise_name}, state={self.state}, subdomain={self.subdomain}, created_at={self.created_at})"
