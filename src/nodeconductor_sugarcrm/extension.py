from nodeconductor.core import NodeConductorExtension


class SugarCRMExtension(NodeConductorExtension):

    @staticmethod
    def django_app():
        return 'nodeconductor_sugarcrm'

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in

    @staticmethod
    def celery_tasks():
        from datetime import timedelta
        return {
            'sugarcrm-sync-crms-quotas': {
                'task': 'nodeconductor.sugarcrm.sync_crms_quotas',
                'schedule': timedelta(minutes=20),
                'args': ()
            },
        }
