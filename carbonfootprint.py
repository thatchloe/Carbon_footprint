# -*- coding: utf-8 -*-
from calculator import inter_cal, aus_cal, esp_cal
from helper import plotting, PDF

from typing import Optional
from fastapi import FastAPI




def carbonfootprint(v, country, file_name):
    if country == 'inter':
        
        name, area, t_grapes_harvested = v
        vineyard = inter_cal(name, area, t_grapes_harvested, file_name)
        total_CO2e = float(vineyard[0])
        per_tonne_grape = total_CO2e/t_grapes_harvested
        
        scope1 = float(vineyard[1]) 
        scope2 = float(vineyard[2]) 
        scope3 = float(vineyard[3]) 
    
        scope1_share = (scope1/(scope1 + scope2 + scope3))*100
        scope2_share = (scope2/(scope1 + scope2 + scope3))*100
        scope3_share = 100 - scope1_share - scope2_share
        
        transport = float(vineyard[4]) 
        waste = float(vineyard[5]) 
        electricity = float(vineyard[6])
        heating = float(vineyard[7])
        mobile_fuel = float(vineyard[8])
        vineyard_practices = float(vineyard[9])
        
        
        transport_share = (transport/total_CO2e)*100
        waste_share = (waste/total_CO2e)*100
        electricity_share = (electricity/total_CO2e)*100
        heating_share = (heating/total_CO2e)*100
        mobile_fuel_share = (mobile_fuel/total_CO2e)*100
        vineyard_practices_share = (vineyard_practices/total_CO2e)*100
        renew = 100 - (transport_share + waste_share + electricity_share + heating_share + mobile_fuel_share + vineyard_practices_share)
        
       
        scope_labels = ['Scope1', 'Scope2', 'Scope3']
        scope_shares = [scope1_share, scope2_share, scope3_share]
        scope_colors = ['#ff9999','#66b3ff','#99ff99']
        scope_explodes = (0.05, 0.05, 0.05)
        title1 = 'Emissions per scope category'
        name1 = 'inter_scopes.png'
        
        #plotting(scope_labels, scope_shares, scope_colors, scope_explodes, title1, name1)
        #scopes = (os.getcwd()+'/'+ name1)
        
        x_labels = ['Transport', 'Waste', 'Electricity', 'Heating', 'Mobile Fuel', 'Vineyard practices', 'Renewable power']
        x_shares = [transport_share, waste_share, electricity_share, heating_share, mobile_fuel_share, vineyard_practices_share, renew]
        x_colors = ['#003f5c', '#444e86', '#955196', '#dd5182', '#ff6e54', '#ffa600', '#66b3ff']
        x_explodes = (0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05)
        title2 = 'Contributions of source activities to total emissions' 
        name2 = 'inter_x.png'
        
        #plotting(x_labels, x_shares, x_colors, x_explodes, title2, name2)
        #x = (os.getcwd()+'/'+ name2)
        
        pdf = PDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.titles(f'Carbon footprint of vineyard {name} (General model)')
        pdf.set_xy(35.0,40.0)
        pdf.charts(name1)
        pdf.set_xy(35.0, 140.0)
        pdf.charts(name2)
        content = f'According to the results, the emissions in the vineyards ({area} ha) were estimated to be {total_CO2e} tonnes CO2e for {t_grapes_harvested} tonnes of harvested grapes or {per_tonne_grape} tonnes of CO2e per tonne of harvested grapes.'
        pdf.texts(content)
        pdf.output('inter.pdf','I')
        
    elif country == 'aus':
        name, area, t_grapes_harvested, unharvested_area, irrigated_area = v
        vineyard = aus_cal(name, area, t_grapes_harvested, unharvested_area, irrigated_area, file_name)
        total_CO2e = float(vineyard[0])
        per_tonne_grape = round(total_CO2e/t_grapes_harvested, 2)
        
        scope1 = float(vineyard[1]) 
        scope2 = float(vineyard[2]) 
        
        scope1_share = (scope1/(scope1 + scope2))*100
        scope2_share = 100 - scope1_share
        
        electricity = float(vineyard[3])
        fertilisers = float(vineyard[5])
        mobile_fuel = float(vineyard[4])
        
        
        electricity_share = (electricity/total_CO2e)*100
        fertilisers_share = (fertilisers/total_CO2e)*100
        mobile_fuel_share = 100 - (electricity_share + fertilisers_share)
        
       
        scope_labels = ['Scope1', 'Scope2']
        scope_shares = [scope1_share, scope2_share]
        scope_colors = ['#ff9999','#66b3ff']
        scope_explodes = (0.05, 0.05)
        title1 = 'Emissions per scope category'
        name1 = 'aus_scopes.png'
        
        #plotting(scope_labels, scope_shares, scope_colors, scope_explodes, title1, name1)
        #scopes = (os.getcwd()+'/'+ name1)
        
        x_labels = ['Electricity', 'Mobile Fuel', 'Fertilisers']
        x_shares = [electricity_share, mobile_fuel_share, fertilisers_share]
        x_colors = ['#003f5c', '#444e86', '#955196']
        x_explodes = (0.05, 0.05, 0.05)
        title2 = 'Contributions of source activities to total emissions' 
        name2 = 'aus_x.png'
        
        #plotting(x_labels, x_shares, x_colors, x_explodes, title2, name2)
        #x = (os.getcwd()+'/'+ name2)
        
        pdf = PDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.titles(f'Carbon footprint of vineyard {name} (Australian model)')
        pdf.set_xy(35.0,40.0)
        pdf.charts(name1)
        pdf.set_xy(35.0, 140.0)
        pdf.charts(name2)
        content = f'According to the results, the emissions in the vineyards ({area} ha) were estimated to be {total_CO2e} tonnes CO2e for {t_grapes_harvested} tonnes of harvested grapes or {per_tonne_grape} tonnes of CO2e per tonne of harvested grapes.'
        pdf.texts(content)
        pdf.output('aus.pdf','I')
        
    elif country == 'esp':
        name, area, t_grapes_harvested = v
        vineyard = esp_cal(name, area, t_grapes_harvested, file_name)
        total_CO2e = float(vineyard[0])
        per_tonne_grape = round(total_CO2e/t_grapes_harvested, 2)
        
        scope1 = float(vineyard[1]) 
        scope2 = float(vineyard[2]) 
        
        scope1_share = (scope1/(scope1 + scope2))*100
        scope2_share = 100 - scope1_share
        
        electricity = float(vineyard[3])
        heating = float(vineyard[5])
        
        
        electricity_share = round((electricity/total_CO2e)*100, 2)
        heating_share = round((heating/total_CO2e)*100, 2)
        refrigeration_share = 100 - (electricity_share + heating_share)
        
       
        scope_labels = ['Scope1', 'Scope2']
        scope_shares = [scope1_share, scope2_share]
        scope_colors = ['#ff9999','#66b3ff']
        scope_explodes = (0.05, 0.05)
        title1 = 'Emissions per scope category'
        name1 = 'esp_scopes.png'
        
        #plotting(scope_labels, scope_shares, scope_colors, scope_explodes, title1, name1)
    
        
        x_labels = ['Electricity', 'Mobile Fuel', 'Fertilisers']
        x_shares = [electricity_share, heating_share, refrigeration_share]
        x_colors = ['#003f5c', '#444e86', '#955196']
        x_explodes = (0.05, 0.05, 0.05)
        title2 = 'Contributions of source activities to total emissions' 
        name2 = 'esp_x.png'
        
        #plotting(x_labels, x_shares, x_colors, x_explodes, title2, name2)
        
        
        pdf = PDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.titles(f'Carbon footprint of vineyard {name} (Spanish model)')
        pdf.set_xy(35.0,40.0)
        pdf.charts(name1)
        pdf.set_xy(35.0, 140.0)
        pdf.charts(name2)
        content = f'According to the results, the emissions in the vineyards ({area} ha) were estimated to be {total_CO2e} tonnes CO2e for {t_grapes_harvested} tonnes of harvested grapes or {per_tonne_grape} tonnes of CO2e per tonne of harvested grapes.'
        pdf.texts(content)
        pdf.output('esp.pdf','I')
    
def test_cases():
    carbonfootprint(['X',10,10], 'inter', 'inter.xlsx')
    carbonfootprint(['X',10,10,1,4], 'aus', 'aus.xlsx')
    carbonfootprint(['X',10,10], 'esp', 'esp.xlsx')
    

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/carbon/{filename}")
def calc_carbon(filename: str, q: Optional[str] = None):
    if 'inter' in filename:
        carbonfootprint(['X',10,10], 'inter', 'inter.xlsx')
    elif 'aus' in filename:
        carbonfootprint(['X',10,10,1,4], 'aus', 'aus.xlsx')
    elif 'esp' in filename:
        carbonfootprint(['X',10,10], 'esp', 'esp.xlsx')
    else:
        return {'Error': 'Select a valid location'}
    return {'Success': 'New '+filename+'.pdf created.'}