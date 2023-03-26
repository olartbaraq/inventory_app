from .models import (
    InventoryGroup, InventoryItem, Shop, Invoice, InvoiceItem
    )
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
        

class InventoryItemWithSumSerializer(InventoryItemSerializer):
    sum_of_item = serializers.IntegerField()

class ShopSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    amount_total = serializers.CharField(read_only=True, required=False)
    count_total = serializers.CharField(read_only=True, required=False)
    
    class Meta:
        model = Shop
        fields = "__all__"
        

class ShopWithAmountSerializer(ShopSerializer):
    amount_total = serializers.FloatField()
    month = serializers.CharField(required=False)

class InvoiceItemSerializer(serializers.ModelSerializer):
    invoice = serializers.CharField(read_only=True)
    invoice_id = serializers.CharField(write_only=True)
    item = InventoryItemSerializer(read_only=True)
    item_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = InvoiceItem
        fields = "__all__"
        

class InvoiceItemDataSerializer(serializers.Serializer):
    item_id = serializers.CharField()
    quantity = serializers.IntegerField()
    

class InvoiceSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    created_by_id = serializers.CharField(write_only=True, required=False)
    shop = ShopSerializer(read_only=True)
    shop_id = serializers.CharField(write_only=True)
    invoice_items = InvoiceItemSerializer(read_only=True, many=True)
    invoice_item_data = InvoiceItemDataSerializer(write_only=True, many=True)
    
    class Meta:
        model = Invoice
        fields = "__all__"
        
    def create(self, validated_data):
        invoice_item_data = validated_data.pop("invoice_item_data")
        if not invoice_item_data:
            raise Exception("You must provide an invoice item data")
        invoice = super().create(validated_data)
        # invoice_id = invoice.data.get("id")
        
        invoice_item_serializer = InvoiceItemSerializer(data = [
            {"invoice_id": invoice.id, **item} for item in invoice_item_data
        ], many=True)
        
        if invoice_item_serializer.is_valid():
            invoice_item_serializer.save()
        else:
            invoice.delete()
            raise Exception(invoice_item_serializer.errors)
        
        return invoice