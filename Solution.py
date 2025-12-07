import json
import random

from util.qualityMeassure import *

class solution:
    def __init__(self):
        with open('./data/dataset_mappings.json', 'r', encoding='utf-8') as file:
            self.data = json.load(file)

        self.keys = list(self.data.keys())

        self.perfect_rules = list()

        self.initChromosome()
        self.def_XY()
        self.calc_meassures()
                    
    def initChromosome(self):
        self.a_chr = list()
        self.b_chr = list()     
        for i in self.data:
            max = len(self.data[i])
            val = random.randint(0, 2)
            self.a_chr.append(val)
            if val == 0:
                self.b_chr.append(0)
            else:
                self.b_chr.append(random.randint(1, max))
              
    def def_XY(self):
        self.X = list()
        self.Y = list()
        for i in range(len(self.a_chr)):
            if self.a_chr[i] == 1:
                self.X.append([self.keys[i], self.b_chr[i]])
            elif self.a_chr[i] == 2:
                self.Y.append([self.keys[i], self.b_chr[i]])
        
    def count_fix_intersection(self):
        self.x_size = intersection_count(self.X)
        self.y_size = intersection_count(self.Y)
        self.sum_size = intersection_count(self.X + self.Y)
        
        #todo Hay que corregir varias condiciones
        # 1. |X| > 0
        # 2. |Y| > 0
        # 3. |X| < N
        # 4. |Y| < N
        # 5. |Z| != |X n Y|
        
        error_count = 0
        
        while (
            not (0 < self.x_size < df_len) or
            not (0 < self.y_size < df_len) or
            self.x_size == self.sum_size
        ):
            error_count += 1
            # Se corrige para que |X| > 0 y |Y| > 0
            if self.x_size == 0:
                index = [i for i, x in enumerate(self.a_chr) if x == 1]
                pos = random.choice(index)
                
                self.a_chr[pos] = 0
                self.b_chr[pos] = 0
                
                self.def_XY()
                self.x_size = intersection_count(self.X)
            
            if self.y_size == 0:
                index = [i for i, y in enumerate(self.a_chr) if y == 2]
                pos = random.choice(index)
                
                self.a_chr[pos] = 0
                self.b_chr[pos] = 0
                
                self.def_XY()
                self.y_size = intersection_count(self.Y)
                
            # Se corrige para que |X| < N y |Y| < N
            if self.x_size == df_len:
                index = [i for i, x in enumerate(self.a_chr) if x == 0]
                # Caso excepcional: todos son 2 y no esta vacio
                if len(index) != 0:
                    pos = random.choice(index)
                else:
                    pos = random.randint(0, len(self.keys) - 1)
                
                self.a_chr[pos] = 1
                self.b_chr[pos] = random.randint(1, len(self.data[self.keys[pos]]))
            
                self.def_XY()
                self.x_size = intersection_count(self.X)
                
            if self.y_size == df_len:
                index = [i for i, x in enumerate(self.a_chr) if x == 0]
                # Caso excepcional: todos son 1 y no esta vacio
                if len(index) != 0:
                    pos = random.choice(index)
                else:
                    pos = random.randint(0, len(self.keys) - 1)
                
                self.a_chr[pos] = 2
                self.b_chr[pos] = random.randint(1, len(self.data[self.keys[pos]]))
            
                self.def_XY()
                self.y_size = intersection_count(self.Y)     
                
            self.sum_size = intersection_count(self.X + self.Y)
            
            # Se corrige |X| != |X n Y|
            if self.x_size == self.sum_size:
                self.perfect_rules.append([self.a_chr, self.b_chr])
                index = [i for i, x in enumerate(self.a_chr) if x == 0]
                if len(index) != 0:
                    pos = random.choice(index)
                else:
                    pos = random.randint(0, len(self.keys) - 1)
            
                self.a_chr[pos] = 2
                self.b_chr[pos] = random.randint(1, len(self.data[self.keys[pos]]))
                
                self.def_XY()
                self.y_size = intersection_count(self.Y)

                self.sum_size = intersection_count(self.X + self.Y)

    def calc_meassures(self):
        self.count_fix_intersection()
        
        self.supp_x = self.x_size / df_len
        self.supp_y = self.y_size / df_len
        self.supp = self.sum_size / df_len
        self.conf = self.sum_size / self.x_size
        self.lift = self.supp / (self.supp_x * self.supp_y) 
        self.conv = (1 - self.supp_y) / (1 - self.conf)