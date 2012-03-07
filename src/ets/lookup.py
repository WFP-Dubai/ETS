# Django settings for ets project.

from ajax_select import LookupChannel

from ets.models import Warehouse

class WarehouseChannel(LookupChannel):
    
    model = Warehouse
    min_length = 1
    search_field = 'code'
    
    def get_objects(self,ids):
        """ Get the currently selected objects when editing an existing model """
        # return in the same order as passed in here
        # this will be however the related objects Manager returns them
        # which is not guaranteed to be the same order they were in when you last edited
        # see OrdredManyToMany.md
        things = self.model.objects.in_bulk(ids)
        return [things[aid] for aid in ids if things.has_key(aid)]

    def can_add(self,user,argmodel):
        """ Check if the user has permission to add 
            one of these models. This enables the green popup +
            Default is the standard django permission check
        """
        return False
