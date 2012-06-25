### -*- coding: utf-8 -*- ####################################################
from django.core.management.base import BaseCommand

from ets.models import Order

class Command(BaseCommand):
    """Count percentage of order executing"""
    
    help = 'Count percentage of order executing'

    def count_order_percentage(self, compas):
        for order in Order.objects.filter(percentage__lt=100):
            order.percentage = round(order.get_percent_executed())
            order.save()
