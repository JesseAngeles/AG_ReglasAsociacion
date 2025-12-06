import json
import random

from util.qualityMeassure import *

class solution:
    def __init__(self):
        with open('./data/dataset_mappings.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        self.initChromosome(data)
        self.def_XY(list(data.keys()))
        self.calc_meassures()
                    
    def initChromosome(self, data):
        self.a_chr = list()
        self.b_chr = list()     
        for i in data:
            max = len(data[i])
            val = random.randint(0, 2)
            self.a_chr.append(val)
            if val == 0:
                self.b_chr.append(0)
            else:
                self.b_chr.append(random.randint(1, max))
                
    def def_XY(self, keys):
        self.X = list()
        self.Y = list()
        for i in range(len(self.a_chr)):
            if self.a_chr[i] == 1:
                self.X.append([keys[i], self.b_chr[i]])
            elif self.a_chr[i] == 2:
                self.Y.append([keys[i], self.b_chr[i]])

    def calc_meassures(self):
        self.x_size = intersection_count(self.X)
        self.y_size = intersection_count(self.Y)
        self.sum_size = intersection_count(self.X + self.Y)
        
        self.supp_x = self.x_size / df_len
        self.supp_y = self.y_size / df_len
        self.supp = self.sum_size / df_len
        
        self.conf = self.sum_size / self.x_size if self.x_size > epsilon else float("inf")
        
        self.lift = self.supp / (self.supp_x * self.supp_y) if self.supp_x > epsilon and self.supp_y > epsilon else 0

        self.conv = (1 - self.supp_y) / (1 - self.conf)

s = solution()

save_memory()

print("Soporte X:", s.supp_x)
print("Soporte Y:", s.supp_y)
print("Soporte XY:", s.supp)
print("Confianza:", s.conf)
print("Lift:", s.lift)
print("Convicción:", s.conv)