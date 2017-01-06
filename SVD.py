import numpy as np
import scipy.sparse as sp
from numpy import linalg as LA
from scipy.sparse.linalg import eigsh
from scipy.sparse import *
from scipy import * 
from scipy.sparse import csc_matrix
from timeit import timeit
from scipy.linalg import eigh as E1

MAX_PID = 2500
MAX_UID = 2500

rows = []
cols = []
values = []

#function for reading the data
def read_data():
	f= open("ratings.txt", "r")
	matrix = np.zeros(shape=(MAX_UID,MAX_PID), dtype=np.float32)
	con= f.read()
	row =0
	col=0
	val=0
	for line in con.split("\n"):
		i=1
		if len(line)!=0:
			for vals in line.split(" "):
				if(i==1):
					rows.append(vals)
					row=vals
					i+=1
				elif(i==2):
					cols.append(vals)
					col=vals
					i+=1
				else:
					values.append(vals)
					val=vals
					i+=1
			matrix[int(row),int(col)]=val
	data = csr_matrix(matrix,dtype  = np.float32)
	return matrix, data

#function for finding gram schmidt orthonormal matrix
def gram_schmidt_columns(X):
    q, r = np.linalg.qr(X)
    q*=-1
    return q

#function for returning eigenvalues and eigenvectors
def do_SVD(matrix):
	trans = matrix.transpose()
	prod = np.dot(matrix, trans)
	e_val, e_vec = LA.eig(prod)
	e_vec = e_vec.transpose()
	combo = zip(e_val.real , e_vec.real)
	combo.sort(key = lambda x: x[0], reverse=True)
	e_val, e_vec = zip(*combo)
	e_vec = np.array(e_vec)
	e_vec_trans = e_vec.transpose()
	return e_val,e_vec_trans

#reading the data file
mat, csr_mat= read_data() 

print mat
#finding the eigen values and U_matrix using A*A' 
evalues, U_matrix = do_SVD(mat)

mat_trans = mat.transpose()

#finding V_matrix using A'*A
e,V_matrix = do_SVD(mat_trans)

#making sigma matrix by putting eigen values in diagonal
sigma_matrix = np.zeros((len(evalues),len(evalues)))

i = 0
for x in evalues:
	sigma_matrix[i,i] = np.sqrt(abs(x))
	i+=1

u,s,v = LA.svd(mat, full_matrices=True)
# print np.sqrt(evalues[:50]) #just for checking purpose
# print u.shape
# print s[:50] #just for checking purpose
# print v.shape



#reconstructing the original matrix again by multiplying all 3 matrices
shape = (U_matrix.shape[1], V_matrix.shape[1])
zeros = np.zeros(shape, dtype=np.float32)
zeros[:sigma_matrix.shape[0], :sigma_matrix.shape[1]] = sigma_matrix

recon_matrix = np.dot(U_matrix,np.dot(zeros,V_matrix))

shape = (u.shape[1],v.shape[0])
x = u.shape[1]
S = np.zeros((2500,2500), dtype = float32)


S[:x,:x] = np.diag(s)
#finding sse of the reconstructing matrix and actual matrix
print np.sqrt(np.sum((mat - recon_matrix)**2))
print recon_matrix
print np.sqrt(np.sum((mat - np.dot(u,np.dot(S,v)))**2))
print np.dot(u,np.dot(S,v))
