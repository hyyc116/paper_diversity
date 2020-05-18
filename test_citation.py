#coding:utf-8

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