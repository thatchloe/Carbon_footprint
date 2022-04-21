# -*- coding: utf-8 -*-


from vineyard import Inter, Aus, Esp
from helper import data


def inter_cal(name, area, t_grapes_harvested, file_name):
    v = Inter(name, area, t_grapes_harvested)
    p = file_name

   
    waste = v.waste_disposal(data(p, 3)) + v.solid_waste(data(p, 12)) + v.waste_water(data(p, 13))
    heating = v.stationary_combustion(data(p, 2), 'inter') 
    mobile_fuel = v.mobile_fuel(data(p, 5), 'inter') + v.machinery(data(p, 4))
    vineyard_practices = v.N2O(data(p, 6)) - v.C(data(p, 1))
    scope1 = waste + heating + mobile_fuel + vineyard_practices
    
    electricity = v.purchased_power(data(p, 7), 'inter')
    renew = v.renewable_energy(data(p, 9))
    scope2 = electricity + renew
    
    transport = v.transport(data(p, 10),'road') + v.transport(data(p, 8),'rail') + v.transport(data(p, 0),'air') + v.transport(data(p, 11),'ship')
    scope3 = transport
    
    total = round(scope1 + scope2 + scope3, 2)
    return (total, scope1, scope2, scope3, transport, waste, electricity, heating, mobile_fuel, vineyard_practices, renew)




def aus_cal(name, area, t_grapes_harvested, unharvested_area, irrigated_area, file_name):
    v = Aus(name, area, t_grapes_harvested, unharvested_area, irrigated_area)
    p = file_name
    
    
    mobile_fuel = v.mobile_fuel(data(p, 2), 'aus') 
    fertilisers = v.fertilisers(data(p, 0), data(p, 1), data(p, 4))
    scope1 = mobile_fuel + fertilisers
    
    electricity = v.purchased_power(data(p, 3), 'aus')
    scope2 = electricity 
    
    
    total = round(scope1 + scope2, 2)
    return (total, scope1, scope2, electricity, mobile_fuel, fertilisers)


def esp_cal(name, area, t_grapes_harvested, file_name):
    v = Esp(name, area, t_grapes_harvested)
    p = file_name
   

    heating = v.stationary_combustion(data(p, 0), 'esp') 
    refrigeration = v.fugitive(data(p, 2))
    scope1 = heating + refrigeration
    
    electricity = v.purchased_power(data(p, 3), 'esp')
    scope2 = electricity
    
    total = round(scope1 + scope2, 2)
    return (total, scope1, scope2, electricity, heating, refrigeration)





