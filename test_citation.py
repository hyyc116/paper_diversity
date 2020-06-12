#coding:utf-8






# a = 50.0
# b = 30.0
# c = 15.0
# d = 5.0
# e = 0.0

# for i in range(1,100):

#     t = a+b+c+d+e

#     print(i,a/t,b/t,c/t,d/t,e/t)

#     a=a+1
#     b=b+1
#     c=c+1
#     d=d+1
#     e=e+1


a = '''
	1,1709
	2,352
	3,123
	4,60
	5,38
	6,15
	7,13
	8,10
	9,3
	10,3
	11,2
	12,2
	13,3
	14,3
	15,2
	17,1
	19,2
	20,1
	27,1
'''

xs = []
ys = []
for line in a.split("\n"):


	line = line.strip()

	if line=='':
		continue

	x,y = line.split(',')

	
	# print(x,y)

	x = int(x)
	y = int(y)

	xs.append(x)
	ys.append(y)

Y = []
for i in sorted(range(len(xs)),key=lambda i:xs[i],reverse=True):
	# print(i,xs[i],ys[i])
	x = xs[i]
	y = ys[i]

	Y.extend([x]*y)

import numpy as np
# print(len(Y))

t = np.sum(Y)
l = len(Y)

print(t,l)
print(np.sum(Y[:int(l/5)])/t)

























import matplotlib.pyplot as plt

citations = [1,10,20,30,40,150,200,200,400,180,40,50,6,7,8,3,2]

fig,axes = plt.subplots(2,1,figsize=(5,8))

xs = []
ys = []

total = []
t = 0
for i,x in enumerate(citations):

	xs.append(i+1)
	ys.append(x)

	t+=x 
	total.append(t)

ax = axes[0]

ax.plot(xs,ys)
ax.plot(xs,total)

ax.set_title('citation curve')


ax2 = axes[1]

xs= total[:-1]
ys = total[1:]



ax2.plot(xs,ys,'o',fillstyle='none')
ax2.plot(xs,xs,'--')


ax2.set_title('total relation')

plt.tight_layout()


plt.savefig('test.png',dpi=200)