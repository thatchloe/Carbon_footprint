# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 23:45:14 2021

@author: Hoang Anh
"""

import pandas as pd
from helper import unit_convert

class Vineyard():
    def __init__(self, name, area, t_grapes_harvested):
        self.area = area                                
        self.t_grapes_harvested = t_grapes_harvested    
        self.name = name
        #self.file_name = file_name
    
    
    
    def N2O(self, data, EF1=0.01, EF2_temp=3):
        '''FSN : Annual amount of synthetic fertiliser addition (kg N/yr)
        FON : Annual amount of organic N addition, manure, sludge etc. (kg N/yr)
        FCR : Annual amount of N in crop residue (generally for N fixing crops) (kg N/yr)
        FOS_temp : Annual area of managed/drained organic soils (ha)
        EF1 : Emission factor for N inputs 
        EF2_temp : Emission factor for managed/drained soils
        N2ODirect-N : Annual direct N2O-N emissions (kg N2O-N/yr)
        N2O-NN Inputs : Annual direct N2O-N emissions from N addition (kg N2O-N/yr)
        N2O-NOS Annual direct N2O-N emissions from managed soil (kg N2O-N/yr)'''
        CO2e = 0
        if data == []:
            return CO2e
        GWP = pd.read_excel('./emission_factors/inter_EF.xlsx', sheet_name='GWP')
        for d in data:
            FSN, FON, FCR, FSOM, FOS_temp, N2O_NPRP = d
            N2O_NN_inputs = (FSN + FON + FCR + FSOM) * EF1 
            N2O_NOS = FOS_temp * EF2_temp
            N2O_N = N2O_NN_inputs + N2O_NOS + N2O_NPRP
            N2O = N2O_N * (44/28) 
            CO2e += N2O * GWP[GWP['Gas']=='N2O']['CO2e'].values[0]
        CO2e = CO2e*0.001
        return CO2e

    
   
    
    def mobile_fuel(self, data, country):
        '''The fuel quantity normally measured as a volume, 
        is converted into the Standard International unit for volume (Litre)
        The volume of fuel is then converted into an energy value. 
        Gigajoules are used as the  emission factors assume this notation of units. 
        CO2e fuel = Fuel Energy * EFfuel'''
        CO2e = 0
        if data == []:
            return CO2e
        
        if country == 'inter':
            df_ef = pd.read_excel('./emission_factors/inter_EF.xlsx', sheet_name='Fuel_EF')
            df = pd.read_csv('Litre_to_GJ.csv')
        elif country == 'aus':
            df_ef = pd.read_excel('./emission_factors/aus_EF.xlsx', sheet_name='Fuel_EF')
        elif country == 'esp':
            df_ef = pd.read_excel('./emission_factors/esp_EF.xlsx', sheet_name='Fuel_EF')
        for d in data:
            fuel_type, fuel_energy = d
            if country == 'inter':
                L_to_GJ = df[df['Fuel Type'] == fuel_type]['Fuel Energy (GJ / Litre)'].values[0]
                EF = df_ef[df_ef['Fuel Type'] == fuel_type]['EFfuel (kg CO2 / GJ)'].values[0]
                CO2e += fuel_energy*L_to_GJ*EF
            elif country == 'aus' or country == 'esp':
                EF = df_ef[df_ef['Fuel Type'] == fuel_type]['Emission factors (kg CO2e/L)'].values[0]
                CO2e += fuel_energy*EF
            
        CO2e = CO2e*0.001
        return CO2e
    
        
        
    def stationary_combustion(self, data, country):
        ''' EmissionsFuel = Fuel*CH4_ef + Fuel*N2O_ef + Fuel*CO2_ef '''
        CO2e = 0
        if data == []:
            return CO2e
        
        if country == 'inter':
            EF = pd.read_excel('./emission_factors/inter_EF.xlsx', sheet_name='combustion_EF')
            GWP = pd.read_excel('./emission_factors/inter_EF.xlsx', sheet_name='GWP')
            for d in data:
                fuel_type, fuel = d
                ef = EF[EF['Fuel Type'] == fuel_type]
                CO2e = fuel * (ef['CH4 (kg/GJ)']*GWP[GWP['Gas']=='CH4']['CO2e'].values[0] + ef['N2O (kg/GJ)']*GWP[GWP['Gas']=='N2O']['CO2e'].values[0] + ef['CO2e (kg/GJ)'].values[0])
        
        elif country == 'esp':
            EF = pd.read_excel('./emission_factors/esp_EF.xlsx', sheet_name='combustion_EF')
            for d in data:
                fuel_type, fuel = d
                CO2e += fuel*EF[EF['Fuel Type'] == fuel_type]['EF (kgCO2e/kg)'].values[0]
        CO2e = CO2e*0.001
        return CO2e
    
    
    
    def purchased_power(self, data, country):
        CO2e = 0
        if data == []:
            return CO2e
        if country == 'inter':
            ef = pd.read_excel('./emission_factors/inter_EF.xlsx', sheet_name='electricity_EF')
        elif country == 'aus':
            ef = pd.read_excel('./emission_factors/aus_EF.xlsx', sheet_name='electricity_EF')
        elif country == 'esp':
            ef = pd.read_excel('./emission_factors/esp_EF.xlsx', sheet_name='electricity_EF')
        for d in data:
            grid, power_purchased = d
            region_ef = ef[ef['Grid'] == grid]['Emission factors'].values[0]
            CO2e += power_purchased*region_ef/1000
        return CO2e
        
        
    

    def renewable_energy(self, data):
        CO2e = 0
        if data == []:
            return CO2e
       
        df = pd.read_excel('./emission_factors/inter_EF.xlsx', sheet_name='renewable_EF')
        for d in data:
            source, power = d
            ef = df[df['Source'] == source]['Emission factor (tCO2e/MWhe)'].values[0]
            CO2e += ef*power
        
        return CO2e
    




class Inter(Vineyard):
    def __init__(self, name, area, t_grapes_harvested):
        super(Inter, self).__init__(name, area, t_grapes_harvested)
        self.path = './emission_factors/inter_EF.xlsx'
        
        



    def transport(self, data, transport_type):
        CO2e = 0
        if data == []:
            return CO2e
        if transport_type == 'road':
            df = pd.read_excel(self.path, sheet_name='road_EF')
        elif transport_type == 'rail':
            df = pd.read_excel(self.path, sheet_name='rail_EF')
        elif transport_type == 'ship':
            df = pd.read_excel(self.path, sheet_name='ship_EF')
        elif transport_type == 'air':
            df = pd.read_excel(self.path, sheet_name='air_EF')
        
        for d in data:
            vehicle_type, freight_weight, freight_distance = d
            CO2e += freight_weight*freight_distance*df[df['Vehicle Type'] == vehicle_type]['Emission factors'].values[0]*0.001
        return CO2e



    def C(self, data):
        CO2e = 0
        if data == []:
            return CO2e
        
        for d in data:
            kg_prunings_per_plant, plants_per_ha = d
            EF_CO2_capture = 0.92                                               #tons CO2/ha/year
            CO2_capture_CO2e = EF_CO2_capture * self.area                         #tons CO2e/year
            EF_prunings = 0.01                                                  #kg CO2e/kg of prunings
            kg_of_prunings_per_ha = kg_prunings_per_plant * plants_per_ha         #kg CO2e/ha
            prunings_CO2e = EF_prunings * kg_of_prunings_per_ha * self.area         #kg CO2e/year
            CO2e += (CO2_capture_CO2e + prunings_CO2e)
        CO2e = CO2e*0.001
        return CO2e


    def machinery(self, data):
        CO2e = 0
        if data == []:
            return CO2e
        ef = pd.read_excel(self.path, sheet_name='Fuel_EF')
        df = pd.read_excel(self.path, sheet_name='helicopter_size')
        
        for d in data:
            size, fuel_type = d
            if fuel_type == 'Gasoline/petrol':
                fuel_consumed = df[df['Size']==size]['PTO(lbs)'].values[0] * 0.2274                             
                CO2e += fuel_consumed * ef[ef['Fuel Type'] == 'Gasoline / petrol']['EFfuel (kg CO2 / GJ)'].values[0]*unit_convert('mass_conv.csv', 'lbs', 'kg')                          
            elif fuel_type == 'Diesel':
                fuel_consumed = df[df['Size']==size]['PTO(lbs)'].values[0] * 0.1667                             
                CO2e += fuel_consumed * ef[ef['Fuel Type'] == 'Diesel']['EFfuel (kg CO2 / GJ)'].values[0]*unit_convert('mass_conv.csv', 'lbs', 'kg')
        CO2e = CO2e*0.001
        return CO2e


    def waste_disposal(self, data):
        if data == []:
            return 0
        for d in data:
            total_mass_of_waste, landfill, incinerated, recycled, composted = d
            waste = pd.read_excel(self.path, sheet_name='waste_disposal_EF')
            landfill = total_mass_of_waste*landfill*waste[waste['waste treatment']=='Landfill']['emission factors (kg CO2e/tonne)'].values[0]
            incinerated = total_mass_of_waste*incinerated*waste[waste['waste treatment']=='Incinerated']['emission factors (kg CO2e/tonne)'].values[0]
            recycled = total_mass_of_waste*recycled*waste[waste['waste treatment']=='Recycled']['emission factors (kg CO2e/tonne)'].values[0]
            composted = total_mass_of_waste*composted*waste[waste['waste treatment']=='Composted']['emission factors (kg CO2e/tonne)'].values[0]
            CO2e = landfill + incinerated + recycled + composted
        return CO2e
        
    
    
    def solid_waste(self, data):
        '''Q Quantity of solid waste expressed in tonnes
        DOC Degradable Organic Carbon 
        R Recovered methane (tonnes)'''
        CO2e = 0
        if data == []:
            return CO2e
        
        doc = pd.read_excel(self.path, sheet_name='DOC')
        for d in data:
            waste_type, Q, R = d
            DOC = doc[doc['Waste Type'] == waste_type]['Default DOC'].values[0]
            CO2e += ((Q*DOC)/3-R)*(18.9)
        
        return CO2e


    def waste_water(self, data):
        '''W_gen : Waste water generation in kL or cubic meters
          COD_con : Chemical Oxygen Demand in kg per kL
          R : Recovered methane (tonnes)'''
        CO2e = 0
        if data == []:
            return CO2e
        
        for d in data:
             W_gen, COD_con, R = d
             CO2e += (W_gen * COD_con * (0.1949) - R) * (21/1000)
        
        return CO2e





class Aus(Vineyard):
    def __init__(self, name, area, t_grapes_harvested, unharvested_area, irrigated_area):
        super(Aus, self).__init__(name, area, t_grapes_harvested)
        self.unharvested_area = unharvested_area
        self.irrigated_area = irrigated_area
        self.path = './emission_factors/aus_EF.xlsx'
        

    

    def fertilisers(self, synthetic, organic, nitrogen):
        syn_N = 0
        org_N = 0
        urea = 0
        for d in synthetic:
            syn_N += d[1]*d[2]
        if syn_N == 0:
            syn_N = nitrogen[0][1]
        for d in synthetic:
            urea += d[1]*d[3]
        if urea == 0:
            urea = nitrogen[2][1]
        for d in organic:
            org_N += d[1]*d[2]
        if org_N == 0:
            org_N = nitrogen[1][1]
        
        df = pd.read_excel(self.path, sheet_name='fertiliser_EF')
        factors = df[:].values
        N2O_emissions = syn_N*(self.irrigated_area*factors[0][1] + (1-self.irrigated_area)*factors[2][1]) + org_N*(self.irrigated_area*factors[1][1] + (1-self.irrigated_area)*factors[3][1]) + urea*factors[4][1]
        
        return N2O_emissions
            


class Esp(Vineyard):
    def __init__(self, name, area, t_grapes_harvested):
        super(Esp, self).__init__(name, area, t_grapes_harvested)
        self.path = './emission_factors/esp_EF.xlsx'
        
        


    def fugitive(self, data):
        ''' Emissions = sum(gas*amount) '''
        CO2e = 0
        if data == []:
            return CO2e
        
        df = pd.read_excel(self.path, sheet_name='GWP')
        for d in data:
            gas, amount = d
            CO2e += df[df['Gas'] == gas]['CO2e'].values[0]*amount
        
        return CO2e


        
    
 


        



