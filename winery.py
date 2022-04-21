# -*- coding: utf-8 -*-

from carbon import Carbon
import pandas as pd
from helper import unit_convert

class Winery(Carbon):
    def __init__(self, tonnes_crushed, biodiversity_area, finished_wine):
        self.tonnes_crushed = tonnes_crushed        #unit: t
        self.biodiversity_area = biodiversity_area  #unit: ha
        self.finished_wine = finished_wine          #unit: kL
        self.bottles = int((self.finished_wine/0.75)*1000)
    
    
    def fugitive_emissions(self, data):
        ''' Emissions = sum(gas*amount)
            gas data type: list
            amount data type: list'''
        CO2e = 0
        if data == []:
            return CO2e
        
        df = pd.read_csv('GWP.csv')
        for d in data:
            gas, amount, unit = d
            CO2e += df[df['Gas'] == gas]['CO2e'].values[0]*amount*unit_convert('mass_conv.csv', unit, 'tonnes')
        
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
        
    

    def fermentation(self, data):
        CO2e = 0
        if data == []:
            return CO2e
        
        for d in data:
            malic_acid_mass = d
            CO2e += 0.33*malic_acid_mass
        return CO2e
    
    
    def packaging(self, data):
        CO2e = 0
        if data == []:
            return CO2e
        
        df = pd.read_csv('packaging_EF.csv')
        for d in data:
            material, mass = d
            CO2e += df[df['Packaging Materials']==material]['NET GWP (tCO2e)'].values[0]*mass
        
        return CO2e
    
    # def csv_from_excel(path):
#         xl = pd.ExcelFile('input.xlsx')

#         sheets = xl.sheet_names
#         for sheet in sheets:
#             sh = wb.sheet_by_name(sheet)
#             your_csv_file = open(sheet + '.csv', 'w')
#             wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
        
#             for rownum in range(sh.nrows):
#                 wr.writerow(sh.row_values(rownum))
        
#             your_csv_file.close()
        

# def data_type(phase):
#     path = os.path.join('./input_data/', phase)
#     dirs = os.listdir(path)
#     types = ['unit', 'waste type', 'vehicle type', 'fuel type', 'Gas', 'material', 'region', 'Waste water generation(kL)', 'size', 'Source', 'Project']
#     for d in dirs:
#         df = pd.read_csv(path + '/'+ d)
#         col = list(df.columns.values)
#         for c in col:
#             if c in types:
#                 df[c] = df[c].map(str)
#             else:
#                 df[c] = df[c].map(float)