from .models import InventoryGroup, InventoryItem
from core.serializers import CustomUserSerializer
from rest_framework import serializers

class InventoryGroupSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    belongs_to = serializers.SerializerMethodField(read_only=True)
    belongs_by_id = serializers.CharField(write_only=True)
    total_items = serializers.CharField(read_only=True, required=False)
    
    class Meta:
        model = InventoryGroup
        fields = "__all__"
        
    def get_belongs_to(self, objects):
        if objects.belongs_to is not None:
            return InventoryGroupSerializer(objects.belongs_to).data
        return None
    
    

class InventoryItemSerializer(serializers.Serializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    # price = serializers.FloatField(required = True)
    group = InventoryGroupSerializer(read_only=True)
    group_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = InventoryItem
        fields = "__all__"