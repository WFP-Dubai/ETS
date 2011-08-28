
import models as ets_models


def update_compas():
    #Update places
    ets_models.Place.update()
    
    #Update persons
    ets_models.CompasPerson.update()
    
    #Update stocks
    ets_models.EpicStock.update()
    
    #Update loss/damage types
    ets_models.LossDamageType.update()
    
    #Update orders
    ets_models.LtiOriginal.update()
    