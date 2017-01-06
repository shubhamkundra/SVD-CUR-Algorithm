import random
from random import randint
import numpy as np
from numpy import linalg
from numpy import mat


#'A' taken as 'matrix'       ise change kar lena original matrix lene ke liye



# matrix = [[1,1,1,0,0],
# 			[3,3,3,0,0],
# 			[4,4,4,0,0],
# 			[5,5,5,0,0],
# 			[0,0,0,4,4],
# 			[0,0,0,5,5],
# 			[0,0,0,2,2]]

num=500 #number of sampling colomns and rows

#'p' is sum of squares of all matrix values
p=0

input_file= open("ratings.txt", "r")
matrix = np.zeros(shape=(2500,2500), dtype=np.float)    #read file in matrix
lines= input_file.read()
row =0
col=0
val=0
for line in lines.split("\n"):
      i=1
      if len(line)!=0:
            for vals in line.split(" "):
                  if(i==1):
                        row=vals
                        i+=1
                  elif(i==2):
                        col = vals
                        i+=1
                  else:
                        val = vals
                        i+=1
      matrix[int(row),int(col)] = val

for i in range(0,len(matrix)):
		for j in range(0,len(matrix[i])-1):
			p=p+matrix[i][j]**2



random.seed(5)
num_c=[]
c=[]
#generating random colomn number
for i in range(0,num):
	num_c.append(randint(0,len(matrix[i])))

#creating 'c' matrix
for i in range(0,len(matrix)):
	temp=[]
	for j in range(0,num):
		temp.append(matrix[i][num_c[j]])
	c.append(temp)

#computing on 'c' matrix			
for i in range(0,num):
	csum=0
	for j in range(0,len(c)):
		csum=csum+c[j][i]**2
	div=csum/p
	div=div*num
	div=div**(0.5)
	for j in range(0,len(c)):
		c[j][i]=c[j][i]/div

print('displaying c matrix')
c1=mat(c)
print(c1)
print()

			

random.seed(1)
num_r=[]
r=[]

#generating random row number
for i in range(num):
	num_r.append(randint(0,len(matrix)-1))

#creating 'r' matrix
for j in range(num):
	temp=[]
	for i in range(0,len(matrix[num_r[j]])):
		temp.append(matrix[num_r[j]][i])
	r.append(temp)

#computin on 'r' matrix		
for i in range(0,num):
		rsum=0
		for j in range(0,len(r[i])):
			rsum=rsum+r[i][j]**2
			
		div=rsum/p
		div=div*num
		div=div**(0.5)
		
		for j in range(0,len(r[i])):
			r[i][j]=r[i][j]/div			
			
print('displaying r matrix')
r1=mat(r)
print(r1)
print()	


w=[] 
			
#creating 'w' matrix		
for i in range(len(num_r)):
	temp=[]
	for j in range(len(num_c)):
		temp.append(matrix[num_r[i]][num_c[j]])
	w.append(temp)



#
#	Apply SVD on 'w' matrix to get 3 matrices
#

print('displaying w matrix\n',mat(w))

x, z1, yt = linalg.svd(w)

xt=x.T
y=yt.T

for i in range(0,len(z1)):
	if(z1[i]!=0):
		z1[i]=1/(z1[i]**2)

z=[]
for i in range(len(y)):
	temp=[]
	for j in range(len(xt)):
		if i==j:
			temp.append(z1[i])
		else:
			temp.append(0)
	z.append(temp)

print()

u=(np.dot(np.dot(y,z),xt))

print('displaying u matrix\n',mat(u))

ans=np.dot(np.dot(c,u),r)

print()
print(ans)

e=0
for i in range(len(matrix)):
	for j in range(len(matrix[i])):
		e=e+(matrix[i][j]-ans[i][j])**2

e=e**.5
print()
print('Error:',e)