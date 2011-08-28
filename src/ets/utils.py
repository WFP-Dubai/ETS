
import models as ets_models


def update_compas(using):
    #Update places
    ets_models.Place.update(using)
    
    #Update persons
    ets_models.CompasPerson.update(using)
    
    #Update stocks
    ets_models.EpicStock.update(using)
    
    #Update loss/damage types
    ets_models.LossDamageType.update(using)
    
    #Update orders
    ets_models.LtiOriginal.update(using)
    