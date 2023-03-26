from rest_framework.viewsets import ModelViewSet
from .serializer import (
    InventoryGroupSerializer, InventoryGroup, InventoryItem, InventoryItemSerializer
)
from rest_framework.response import Response
from inventory_api.custom_methods import IsAuthenticatedCustom



class InventoryView(ModelViewSet):
    queryset = InventoryItem.objects.select_related("group", "created_by")
    serializer_class = InventoryItemSerializer
    permission_classes = ((IsAuthenticatedCustom), )
    

    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id": request.user.id})
        return super().create(request, *args, **kwargs)


class InventoryGroupView(ModelViewSet):
    queryset = InventoryGroup.objects.select_related("belongs_to", "created_by").prefetch_related("invetories")
    serializer_class = InventoryGroupSerializer
    permission_classes = ((IsAuthenticatedCustom), )
    

    def create(self, request, *args, **kwargs):
        request.data.update({"created_by_id": request.user.id})
        return super().create(request, *args, **kwargs)

