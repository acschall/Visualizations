# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 11:24:07 2018

@author: assaf
"""

import geopandas as gpd

import numpy as np
import shapely

import matplotlib.pyplot as plt
from descartes import PolygonPatch

from matplotlib.widgets import Button

BLUE = '#6699cc'
YELLOW = '#FFFF00'
RED = '#FF0000'

df_counties = gpd.read_file('tl_2016_08_cousub/tl_2016_08_cousub.shp')


class DistrictBuild:
    def __init__(self, df):
        self.df = df
        self.district_set = set()
        self.dim = len(df)
        
        print(df['STATEFP'][0])

        fig, ax = plt.subplots(figsize=(10, 10))
        plt.title('Colorado', 
                  fontsize=25, 
                  fontweight='bold', 
                  family='cursive')
        self.t1 = ax.text(.3, 
                          -.2,
                          'Polsby-Popper:', 
                          ha='center',
                          va='center', 
                          transform=ax.transAxes,
                          fontsize=15)
        self.t2 = ax.text(.6, 
                          -.2,
                          '0.00000000000000000', 
                          ha='center',
                          va='center', 
                          transform=ax.transAxes,
                          fontsize=15)
        plt.axis('off')
        self.patches_dict = {}
        self.ax = fig.gca()

        for ind in range(self.dim):
            poly = self.df['geometry'][ind]
            patch = PolygonPatch(poly, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2)
            self.patches_dict.update({ind: patch})
            self.ax.add_patch(self.patches_dict[ind])
        self.ax.axis('scaled')
        plt.show()
        cid = fig.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        # print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
        #      ('double' if event.dblclick else 'single', event.button,
        #       event.x, event.y, event.xdata, event.ydata))
        self.change_district(np.array([event.xdata, event.ydata]))
        self.update_text()

    def compute_score(self):
        df_district = self.df[self.create_index_list_from_set(self.district_set, self.dim)]
        new_district = df_district.dissolve('STATEFP')
        polsby_popper = 4 * np.pi * new_district.iloc[0].geometry.area / (new_district.iloc[0].geometry.length) ** 2
        return polsby_popper
    
    def update_text(self):
        polsby_popper = self.compute_score()
        self.t2.set_text(str(polsby_popper))
        plt.draw()
        print(polsby_popper)

    def create_index_list_from_set(self, myset, list_len):
        mylist = [False] * list_len
        for ind in myset:
            mylist[ind] = True
        return mylist

    def change_district(self, coords):
        lat = coords[0]
        long = coords[1]
        pt = shapely.geometry.Point(lat, long)
        for ind in range(self.dim):
            if pt.within(self.df['geometry'][ind]):
                if ind in self.district_set:
                    self.update_map(ind, 0)
                elif ind not in self.district_set:
                    self.update_map(ind, 1)

    def update_map(self, index, colorize):
        if colorize == 1:
            self.patches_dict[index].remove()
            print('I add')
            self.district_set.add(index)
            poly = self.df['geometry'][index]
            new_patch = PolygonPatch(poly, fc=YELLOW, ec=YELLOW, alpha=0.5, zorder=2)
            self.patches_dict[index] = new_patch
            self.ax.add_patch(self.patches_dict[index])
            plt.draw()
        elif colorize == 0:
            print('I remove')
            self.district_set.remove(index)
            self.patches_dict[index].remove()
            poly = self.df['geometry'][index]
            new_patch = PolygonPatch(poly, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2)
            self.patches_dict[index] = new_patch
            self.ax.add_patch(self.patches_dict[index])
            plt.draw()

# district_counties = set() becomes district_set
# counties becomes patches_dict


DistrictBuild(df_counties)


# plt.show()
