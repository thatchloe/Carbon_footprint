# -*- coding: utf-8 -*-


import pandas as pd
import xlrd 
import csv
import os
import matplotlib.pyplot as plt
from fpdf import FPDF

def unit_convert(file, unit1, unit2):
        df = pd.read_csv(file)
        multiply_by = df.loc[(df['Convert From'] == unit1) & (df['Convert To'] == unit2)]['Multiply By'].values[0]
        
        return multiply_by
    
    


def data(filename, sheetname):
    df = pd.read_excel(os.path.join(os.getcwd(), 'input_data' + '/' + filename), sheet_name = sheetname)
    data = df[:].values
    return data



def plotting(labels, shares, colors, explodes, title, file_name):
    fig, ax = plt.subplots(figsize=(10, 7))
    pie = ax.pie(shares, colors = colors, autopct='%1.1f%%', startangle=90, pctdistance=0.85, explode = explodes)
    
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.legend(pie[0], labels, bbox_to_anchor=(1,0), loc="lower right", bbox_transform=fig.transFigure)
    plt.title(title)
    ax.axis('equal')  
    plt.tight_layout()
    plt.savefig(file_name)
    plt.show()


class PDF(FPDF):
    def charts(self, plot):
        self.image(plot,  link='', type='', w=700/5, h=450/5)
        
    
    def titles(self, txt):
        self.set_xy(0.0,0.0)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 50, 50)
        self.cell(w=210.0, h=40.0, align='C', txt=txt, border=0) 
    
    def texts(self,txt):
        self.set_xy(10.0,240.0)    
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', '', 12)
        self.multi_cell(0,10,txt)

