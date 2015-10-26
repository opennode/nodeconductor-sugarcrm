from rest_framework import serializers

from nodeconductor.structure import serializers as structure_serializers
from nodeconductor.structure import SupportedServices
from . import models


class ServiceSerializer(structure_serializers.BaseServiceSerializer):

    SERVICE_TYPE = SupportedServices.Types.SugarCRM
    SERVICE_ACCOUNT_FIELDS = {
        'backend_url': 'URL of OpenStack service project link that will be used for sugarCRM resources creation '
                       '(required, e.g.: http://example.com/api/openstack-service-project-link/1/)',
        'username': 'NodeConductor user username (e.g. Username)',
        'password': 'NodeConductor user password (e.g. Password)',
    }
    SERVICE_ACCOUNT_EXTRA_FIELDS = {
        'image_name': 'CRMs OpenStack instance image name. (default: "sugarcrm")',
        'security_groups_names': 'List of CRMs OpenStack instance security groups names. (default: ["http"])',
        'min_cores': 'Minimum amount of cores for CRMs OpenStack instance. (default: 2)',
        'min_ram': 'Minimum amount of ram for CRMs OpenStack instance. (default: 2048 MB)',
        'system_size': 'Storage volume size CRMs OpenStack instance. (default: 32768 MB)',
        'data_size': 'Data volume size of CRMs OpenStack instance. (default: 65536 MB)',
    }

    class Meta(structure_serializers.BaseServiceSerializer.Meta):
        model = models.SugarCRMService
        view_name = 'sugarcrm-detail'


class ServiceProjectLinkSerializer(structure_serializers.BaseServiceProjectLinkSerializer):

    class Meta(structure_serializers.BaseServiceProjectLinkSerializer.Meta):
        model = models.SugarCRMServiceProjectLink
        view_name = 'sugarcrm-spl-detail'
        extra_kwargs = {
            'service': {'lookup_field': 'uuid', 'view_name': 'sugarcrm-detail'},
        }


class CRMSerializer(structure_serializers.BaseResourceSerializer):
    service = serializers.HyperlinkedRelatedField(
        source='service_project_link.service',
        view_name='sugarcrm-detail',
        read_only=True,
        lookup_field='uuid')

    service_project_link = serializers.HyperlinkedRelatedField(
        view_name='sugarcrm-spl-detail',
        queryset=models.SugarCRMServiceProjectLink.objects.all(),
        write_only=True)

    class Meta(structure_serializers.BaseResourceSerializer.Meta):
        model = models.CRM
        view_name = 'sugarcrm-crms-detail'
