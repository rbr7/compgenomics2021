import pandas as pd
import numpy as np; np.random.seed(0)
import seaborn as sns; sns.set_theme()
from matplotlib import pyplot as plt


file=pd.read_csv('/home/Documents/Acads/CompGenomics/Proj_ComparitiveGenomics/report_binary.csv')

genes=list(file.head())
genes.pop(0)
genes=[genes[i][:-6] for i in range(len(genes))]
# print(genes)

isolates=list(file['name'])
isolates=[isolates[i][2:9] for i in range(len(isolates))]
# print(isolates)

data=file.values.tolist()

for i in range(len(data)):
	data[i].pop(0)

genes[0]='ANT_3_IIa+'
genes[1]='APH_3_Ib'
genes[2]='APH_6_Id'
genes[7]='GlpT'
genes[8]='LamB'
genes[9]='UhpA_1'
genes[10]='ampC1'
genes[12]='KpnH+'
genes[-5]='OmpC'


tree=['CGT1837', 'CGT1602', 'CGT1317', 'CGT1447', 'CGT1323', 'CGT1992', 'CGT1976', 'CGT1621', 'CGT1473', 'CGT1327', 'CGT1778', 'CGT1197', 'CGT1238', 'CGT1615', 'CGT1219', 'CGT1020', 'CGT1009', 'CGT1783', 'CGT1394', 'CGT1833', 'CGT1600', 'CGT1408', 'CGT1568', 'CGT1500', 'CGT1342', 'CGT1858', 'CGT1283', 'CGT1991', 'CGT1985', 'CGT1841', 'CGT1459', 'CGT1795', 'CGT1531', 'CGT1436', 'CGT1519', 'CGT1440', 'CGT1834', 'CGT1058', 'CGT1606', 'CGT1511', 'CGT1417', 'CGT1084', 'CGT1777', 'CGT1960', 'CGT1808', 'CGT1428', 'CGT1989', 'CGT1174', 'CGT1946', 'CGT1493']

toplot=[[] for i in range(50)]

for i in range(50):
	index=isolates.index(tree[i])
	toplot[i]=data[index]

print(genes)
print(len(genes))

# xlabels=genes
# ylabels=tree

# ax = sns.heatmap(toplot, xticklabels=xlabels, yticklabels=ylabels)
# plt.show()

