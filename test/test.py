import pandas as pd

df = pd.read_csv("./test/data_test.csv")

class Rule:
    def __init__(self, df, r_from, r_from_v, r_to, r_to_v):
        self.df = df
        self.headers = df.columns.to_list()
        
        self.r_from = r_from
        self.r_from_v = r_from_v
        self.r_to = r_to
        self.r_to_v = r_to_v
        
        self.def_X()
        self.def_Y()
        self.calc_meassures()

    # DEFINICIÓN DE X
    def def_X(self):
        self.X = pd.DataFrame()

        for rule_from, rule_from_values in zip(self.r_from, self.r_from_v):
            inter = self.df.copy()

            for f, v in zip(rule_from, rule_from_values):
                selected = self.df[self.df[f] == v]
                inter = self.df.loc[inter.index.intersection(selected.index)]

            self.X = self.df.loc[self.X.index.union(inter.index)]

    # DEFINICIÓN DE Y
    def def_Y(self):
        self.Y = pd.DataFrame()

        for rule_to, rule_to_values in zip(self.r_to, self.r_to_v):
            inter = self.df.copy()

            for f, v in zip(rule_to, rule_to_values):
                selected = self.df[self.df[f] == v]
                inter = self.df.loc[inter.index.intersection(selected.index)]

            self.Y = self.df.loc[self.Y.index.union(inter.index)]

    # MÉTRICAS
    def calc_meassures(self):
        self.calc_intersection()
        self.calc_union()

        self.supp_x = self.calc_supp_A(self.X)
        self.supp_y = self.calc_supp_A(self.Y)

        self.calc_supp()
        self.calc_conf()
        self.calc_lift()
        self.calc_conv()

    def calc_intersection(self):
        self.intersection = self.df.loc[
            self.X.index.intersection(self.Y.index)
        ]

    def calc_union(self):
        self.union = self.df.loc[
            self.X.index.union(self.Y.index)
        ]

    def calc_supp_A(self, X):
        return len(X) / len(self.df)

    def calc_supp(self):
        self.supp = len(self.intersection) / len(self.df)

    def calc_conf(self):
        if self.supp_x == 0:
            self.conf = 0
        else:
            self.conf = self.supp / self.supp_x

    def calc_lift(self):
        if self.supp_x == 0 or self.supp_y == 0:
            self.lift = 0
        else:
            self.lift = self.supp / (self.supp_x * self.supp_y)

    def calc_conv(self):
        if self.conf == 1:
            self.conv = float("inf")
        else:
            self.conv = (1 - self.supp_y) / (1 - self.conf)

    # SETTERS
    def set_from(self, r_from, r_from_v):
        self.r_from = r_from
        self.r_from_v = r_from_v
        self.def_X()
        self.calc_meassures()

    def set_to(self, r_to, r_to_v):
        self.r_to = r_to
        self.r_to_v = r_to_v
        self.def_Y()
        self.calc_meassures()    


headers = df.columns.to_list()

r = Rule(
    df=df,
    r_from=[[headers[5], headers[6]]],
    r_from_v=[[1, 1]],
    r_to=[[headers[4]]],
    r_to_v=[[1]]
)
print("Soporte X:", r.supp_x)
print("Soporte Y:", r.supp_y)
print("Soporte XY:", r.supp)
print("Confianza:", r.conf)
print("Lift:", r.lift)
print("Convicción:", r.conv)