# -*- coding: utf-8 -*-
#4.
import pandas as pd

managers = pd.read_csv('Data/Part2/004/managers.csv',
                     index_col='Date')

MANA = managers.iloc[:,(0,2,3)]

((MANA.HAM1-MANA.HAM1.mean())**2).sum()

((MANA.HAM3-MANA.HAM3.mean())**2).sum()

((MANA.HAM4-MANA.HAM4.mean())**2).sum()

mu = MANA.mean().mean()

((MANA.HAM1.mean()-mu)**2 + (MANA.HAM3.mean()-mu)**2 +(MANA.HAM4.mean()-mu)**2) * 132

0.0001676679+0.08604549+0.1746452+0.370733

#5.
from statsmodels.formula.api import ols
import statsmodels.stats.anova as anova

returns = pd.DataFrame(pd.concat([MANA.HAM1,MANA.HAM3,MANA.HAM4]))

returns['Class'] = ['HAM1' for i in range(132)]+['HAM3' for i in range(132)]+['HAM4' for i in range(132)]

returns.columns = ['Return','Class']

model = ols('Return~C(Class)',data=returns).fit()

print(anova.anova_lm(model))