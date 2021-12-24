import pandas as pd
import numpy as np; np.random.seed(0)
import seaborn as sns; sns.set_theme()
from matplotlib import pyplot as plt

filelist=['CGT1837', 'CGT1602', 'CGT1317', 'CGT1447', 'CGT1323', 'CGT1992', 'CGT1976', 'CGT1621', 'CGT1473', 'CGT1327', 'CGT1778', 'CGT1197', 'CGT1238', 'CGT1615', 'CGT1219', 'CGT1020', 'CGT1009', 'CGT1783', 'CGT1394', 'CGT1833', 'CGT1600', 'CGT1408', 'CGT1568', 'CGT1500', 'CGT1342', 'CGT1858', 'CGT1283', 'CGT1991', 'CGT1985', 'CGT1841', 'CGT1459', 'CGT1795', 'CGT1531', 'CGT1436', 'CGT1519', 'CGT1440', 'CGT1834', 'CGT1058', 'CGT1606', 'CGT1511', 'CGT1417', 'CGT1084', 'CGT1777', 'CGT1960', 'CGT1808', 'CGT1428', 'CGT1989', 'CGT1174', 'CGT1946', 'CGT1493']

genes=[]
data=[]


for i in range(len(filelist)):
	file=pd.read_csv('/home/Documents/Acads/CompGenomics/Proj_ComparitiveGenomics/02.AR-output/'+filelist[i]+'-AR-STing.txt', sep='\t', header=None)
	contents=file.values.tolist()
	genes.append(contents[0][1:-4])
	data.append(contents[1][1:-4])	


total=[]
for j in range(len(genes)):
	total=total+genes[j]
net=list(dict.fromkeys(total))
# print(len(net))


toplot=[[0 for p in range(len(net))] for q in range(len(genes))]


for i in range(len(genes)):
	for j in range(len(net)):
		if net[j] in genes[i]:
			index=genes[i].index(net[j])
			toplot[i][j]=int(data[i][index])


tags=pd.read_csv('/home/Documents/Acads/CompGenomics/Proj_ComparitiveGenomics/02.AR-output/card_tags_xRef.tsv', sep='\t')
cardID=list(tags['cardID'])
geneName=list(tags['geneName'])

names=['' for i in range(len(net))]

# print(cardID[0])
# print(geneName[0])

for m in range(len(net)):
	ind=cardID.index(net[m])
	# print(net[m])
	# print(geneName[ind])
	names[m]=geneName[ind][geneName[ind].index('|',29)+1:geneName[ind].index('[')]
	if 'plasmid' in geneName[ind] or 'Plasmid' in geneName[ind]:
		names[m]=names[m]+' '+geneName[ind][geneName[ind].index('[')+1:geneName[ind].index(']')]


for g in range(len(names)):
	if '|' in names[g]:
		names[g]=names[g][names[g].index('|')+1:-1]
	if 'Escherichia coli' in names[g]:
		names[g]=names[g][names[g].index('Escherichia coli ')+17:-1]
	

names[51]='Kp acrA'
#Klebsiella pneumoniae
#Enterobacter cloacae
names[53]='Ec acrA'
names[85]='ANT-Ii-AAC-IId'
names[69]='aadA3 P* NR79'

fig = plt.figure(figsize=(50,30))
xlabels=names
ylabels=filelist

# ax = sns.heatmap(toplot, xticklabels=xlabels, yticklabels=ylabels)
# plt.show()

print(names)
print(len(names))
