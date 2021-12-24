import pandas as pd
import numpy as np; np.random.seed(0)
import seaborn as sns; sns.set_theme()
from matplotlib import pyplot as plt


file=pd.read_csv('/home/Documents/Acads/CompGenomics/Proj_ComparitiveGenomics/vf_merged_results.tsv', sep='\t')

VF=list(file['Virulence factor'])
Is=list(file['Isolate'])

genes=['eae', 'iss', 'tir', 'espA', 'espB', 'espJ', 'etpD', 'iha', 'ehxA',  'nleA', 'nleB',  'astA', 'espP', 'gad', 'katP', 'nleC', 'toxB', 'espF','efa1' , 'stx1A', 'stx1B','espI']
isolates=['CGT1009', 'CGT1020', 'CGT1058', 'CGT1084', 'CGT1174', 'CGT1197', 'CGT1219', 'CGT1238', 'CGT1283', 'CGT1317', 'CGT1323', 'CGT1327', 'CGT1342', 'CGT1394', 'CGT1408', 'CGT1417', 'CGT1428', 'CGT1436', 'CGT1440', 'CGT1447', 'CGT1459', 'CGT1473', 'CGT1493', 'CGT1500', 'CGT1511', 'CGT1519', 'CGT1531', 'CGT1568', 'CGT1600', 'CGT1602', 'CGT1606', 'CGT1615', 'CGT1621', 'CGT1777', 'CGT1778', 'CGT1783', 'CGT1795', 'CGT1808', 'CGT1833', 'CGT1834', 'CGT1837', 'CGT1841', 'CGT1858', 'CGT1946', 'CGT1960', 'CGT1976', 'CGT1985', 'CGT1989', 'CGT1991', 'CGT1992']
isolates_tree=['CGT1837', 'CGT1602', 'CGT1317', 'CGT1447', 'CGT1323', 'CGT1992', 'CGT1976', 'CGT1621', 'CGT1473', 'CGT1327', 'CGT1778', 'CGT1197', 'CGT1238', 'CGT1615', 'CGT1219', 'CGT1020', 'CGT1009', 'CGT1783', 'CGT1394', 'CGT1833', 'CGT1600', 'CGT1408', 'CGT1568', 'CGT1500', 'CGT1342', 'CGT1858', 'CGT1283', 'CGT1991', 'CGT1985', 'CGT1841', 'CGT1459', 'CGT1795', 'CGT1531', 'CGT1436', 'CGT1519', 'CGT1440', 'CGT1834', 'CGT1058', 'CGT1606', 'CGT1511', 'CGT1417', 'CGT1084', 'CGT1777', 'CGT1960', 'CGT1808', 'CGT1428', 'CGT1989', 'CGT1174', 'CGT1946', 'CGT1493']


toplot=[[0 for j in range(22)] for i in range(50)]

for i in range(50):
	print(i)
	
	if isolates_tree[i] !='CGT1992':
		neighbour=isolates[isolates.index(isolates_tree[i])+1]
		setofgenes=VF[Is.index(isolates_tree[i]):Is.index(neighbour)]
	else:
		setofgenes=VF[Is.index(isolates_tree[i]):]

	for j in range(22):
		if genes[j] in setofgenes:
			toplot[i][j]=1



xlabels=genes
ylabels=isolates_tree

ax = sns.heatmap(toplot, xticklabels=xlabels, yticklabels=ylabels)
plt.show()

