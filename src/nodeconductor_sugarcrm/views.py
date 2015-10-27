from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from nodeconductor.structure import views as structure_views
from nodeconductor.structure.managers import filter_queryset_for_user
from . import models, serializers


class SugarCRMServiceViewSet(structure_views.BaseServiceViewSet):
    queryset = models.SugarCRMService.objects.all()
    serializer_class = serializers.ServiceSerializer


class SugarCRMServiceProjectLinkViewSet(structure_views.BaseServiceProjectLinkViewSet):
    queryset = models.SugarCRMServiceProjectLink.objects.all()
    serializer_class = serializers.ServiceProjectLinkSerializer


class CRMViewSet(structure_views.BaseResourceViewSet):
    queryset = models.CRM.objects.all()
    serializer_class = serializers.CRMSerializer

    def perform_provision(self, serializer):
        resource = serializer.save()
        backend = resource.get_backend()
        backend.provision(resource)

    # User can only create and delete CRMs. He cannot stop them.
    @structure_views.safe_operation(valid_state=models.CRM.States.ONLINE)
    def destroy(self, request, resource, uuid=None):
        if resource.backend_id:
            backend = resource.get_backend()
            backend.destroy(resource)
        else:
            self.perform_destroy(resource)


class CRMUserViewSet(viewsets.ViewSet):

    def dispatch(self, request, crm_uuid, *args, **kwargs):
        queryset = filter_queryset_for_user(models.CRM.objects.all(), request.user)
        self.crm = get_object_or_404(queryset, uuid=crm_uuid)
        self.backend = self.crm.get_backend()
        return super(CRMUserViewSet, self).dispatch(request, crm_uuid, *args, **kwargs)

    def get_serializer_context(self):
        return {'crm': self.crm, 'request': self.request}

    def list(self, request, crm_uuid):
        users = self.backend.list_users()
        serializer = serializers.CRMUserSerializer(users, many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    def retrieve(self, request, crm_uuid, pk=None):
        user = self.backend.get_user(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CRMUserSerializer(user, context=self.get_serializer_context())
        return Response(serializer.data)

    def destroy(self, request, crm_uuid, pk=None):
        user = self.backend.get_user(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.backend.delete_user(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, crm_uuid):
        serializer = serializers.CRMUserSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        user = self.backend.create_user(status='Active', **serializer.validated_data)
        user_data = serializers.CRMUserSerializer(user, context=self.get_serializer_context()).data
        return Response(user_data, status=status.HTTP_201_CREATED)
