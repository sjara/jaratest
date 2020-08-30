# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 11:50:56 2020

@author: devin

100 NumPy challanges:
"""
#### 1. Import the numpy package under the name `np` (★☆☆)
import numpy as np

#### 2. Print the numpy version and the configuration (★☆☆)
# print(np.__version__, np.show_config())

#### 3. Create a null vector of size 10 (★☆☆)
v1 = np.zeros(10)
#print(v1)

#### 4. How to find the memory size of any array (★☆☆)
# print(v1.size, v1.itemsize)

#### 5. How to get the documentation of the numpy add function from the command line? (★☆☆)
# Need Help 

#### 6. Create a null vector of size 10 but the fifth value which is 1 (★☆☆)
v2 = np.zeros(10)
v2[4] = 1
# print(v2)

#### 7. Create a vector with values ranging from 10 to 49 (★☆☆)
v3 = np.arange(10,50)
# print(v3)

#### 8. Reverse a vector (first element becomes last) (★☆☆)
v4 = np.array(v3[::-1])
# print(v4)

#### 9. Create a 3x3 matrix with values ranging from 0 to 8 (★☆☆)
v5 = np.arange(9).reshape((3, 3))
# print(v5)

#### 10. Find indices of non-zero elements from [1,2,0,0,4,0] (★☆☆)
v6 = np.nonzero([1, 2, 0, 0, 4, 0])
# print(v6)

#### 11. Create a 3x3 identity matrix (★☆☆)
v7 = np.eye(3)
# print(v7)

#### 12. Create a 3x3x3 array with random values (★☆☆)
v8 = np.random.random((3,3,3))
# print(v8)

#### 13. Create a 10x10 array with random values and find the minimum and maximum values (★☆☆)
v9 = np.random.random((10,10))
max1, min1 = v9.max(), v9.min()
# print(v9, max1, min1)


#### 14. Create a random vector of size 30 and find the mean value (★☆☆)
v10 = np.random.random(30)
mean1 = v10.mean()
# print(v10, mean1)

#### 15. Create a 2d array with 1 on the border and 0 inside (★☆☆)
v11 = np.ones((10,10))
v11[1:-1, 1:-1] = 0
# print(v11)

#### 16. How to add a border (filled with 0's) around an existing array? (★☆☆)
v12 = np.pad(v11, 1)
# print(v12)

#### 17. What is the result of the following expression? (★☆☆)


# print(0 * np.nan) #nan
# print(np.nan == np.nan) #False
# print(np.inf > np.nan) #False
# print(np.nan - np.nan) #nan
# print(np.nan in set([np.nan])) #True
# print(0.3 == 3 * 0.1) #False

#### 18. Create a 5x5 matrix with values 1,2,3,4 just below the diagonal (★☆☆)
v13 = np.arange(1,5)
v14 = np.diag(v13, k=-1)
# print(v13, v14)
# can put arange in the diag function

#### 19. Create a 8x8 matrix and fill it with a checkerboard pattern (★☆☆)
v15 = np.zeros((8,8))
v15[1::2,::2] = 1
v15[::2,1::2] = 1
# print(v15)

#### 20. Consider a (6,7,8) shape array, what is the index (x,y,z) of the 100th element?
ind1 = np.unravel_index(99, (6,7,8))
# print(ind1)

#### 21. Create a checkerboard 8x8 matrix using the tile function (★☆☆)
v16 = np.tile(np.array([[0,1],[1,0]]), (4,4))
# print(v16)

#### 22. Normalize a 5x5 random matrix (★☆☆)
v17 = np.random.random((5,5))
v17 = (v17 - np.mean(v17)) / (np.std(v17))
# print(v17)

#### 23. Create a custom dtype that describes a color as four unsigned bytes (RGBA) (★☆☆)
#color = np.dtype([("r", np.ubyte, 1),
#                  ("g", np.ubyte, 1),
#                  ("b", np.ubyte, 1),
#                  ("a", np.ubyte, 1)])

#### 24. Multiply a 5x3 matrix by a 3x2 matrix (real matrix product) (★☆☆)
#v18 = np.dot(np.ones((5,3)), np.ones((3,2)))
v18 = np.arange(15).reshape((5,3))
v19 = np.arange(6).reshape((3,2))
v20 = v18 @ v19
# print(v18, v19, v20)

#### 25. Given a 1D array, negate all elements which are between 3 and 8, in place. (★☆☆)
v21 = np.arange(25)
v21[(3 < v21) & (v21 < 8)] *= -1
# print(v21)

#### 26. What is the output of the following script? (★☆☆)
"""
python
# Author: Jake VanderPlas

print(sum(range(5),-1))
from numpy import *
print(sum(range(5),-1))
"""
# print(sum(range(5), -1))

#### 27. Consider an integer vector Z, which of these expressions are legal? (★☆☆)
"""
python
Z**Z
2 << Z >> 2
Z <- Z
1j*Z
Z/1/1
Z<Z>Z
"""

#### 28. What are the result of the following expressions?
"""
python
np.array(0) / np.array(0) - true divison -> nan
np.array(0) // np.array(0) - floor division -> 0
np.array([np.nan]).astype(int).astype(float) -> [-2.14748365e+09]
"""
#### 29. How to round away from zero a float array ? (★☆☆)
v21a = np.random.uniform(-10,10,10)
# print(v21a)
# print(np.copysign(np.ceil(np.abs(v21a)), v21a))
np.copysign
#### 30. How to find common values between two arrays? (★☆☆)
v22 = np.random.randint(0,10,10)
v23 = np.random.randint(0,10,10)
# print(np.intersect1d(v22, v23))

#### 31. How to ignore all numpy warnings (not recommended)? (★☆☆)
# defaults = np.seterr(all = "ignore")
# back to normal -> defaults = np.seterr(**defaults)

#### 32. Is the following expressions true? (★☆☆)
"""python
np.sqrt(-1) == np.emath.sqrt(-1)
"""
# print(np.sqrt(-1), np.emath.sqrt(-1))

#### 33. How to get the dates of yesterday, today and tomorrow? (★☆☆)
today = np.datetime64('today')
tomorrow = today + np.timedelta64(1)
yesterday = today - np.timedelta64(1)
# print(today, tomorrow, yesterday)

#### 34. How to get all the dates corresponding to the month of July 2016? (★★☆)
v24 = np.arange('2016-07', '2016-08', dtype='datetime64[D]')
# print(v24)

#### 35. How to compute ((A+B)*(-A/2)) in place (without copy)? (★★☆)
v25 = np.ones(3)
v26 = np.ones(3)*2
np.add(v25, v26, out=v25)

#### 36. Extract the integer part of a random array of positive numbers using 4 different methods (★★☆)
v27 = np.random.random(10)
v27 = v27 // 1
v27 = v27 - v27%1
np.floor(v27, out=v27)
v27.astype(int)
np.trunc(v27)

#### 37. Create a 5x5 matrix with row values ranging from 0 to 4 (★★☆)
v28 = np.tile(np.arange(5),5).reshape((5,5))
# print(v28)

#### 38. Consider a generator function that generates 10 integers and use it to build an array (★☆☆)
def first_generator():
    for x in range(10):
        yield x
v29 = np.fromiter(first_generator(), dtype=float)
# print(v29)

#### 39. Create a vector of size 10 with values ranging from 0 to 1, both excluded (★★☆)
v30 = np.linspace(0, 1, 11, endpoint=False)[1:]
# print(v30)

#### 40. Create a random vector of size 10 and sort it (★★☆)
v31 = np.random.random(10)
v31.sort()
# print(v31)

#### 41. How to sum a small array faster than np.sum? (★★☆)
v32 = np.arange(10)
# print(np.add.reduce(v32))

#### 42. Consider two random array A and B, check if they are equal (★★☆)           
equal = np.allclose(np.random.random(10), np.random.random(10))
equal2 = np.array_equal(np.random.random(10), np.random.random(10))   
# print(equal, equal2)

#### 43. Make an array immutable (read-only) (★★☆)
v33 = np.zeros(10)
v33.flags.writeable = False

#### 44. Consider a random 10x2 matrix representing cartesian coordinates, convert them to polar coordinates (★★☆)
v34 = np.random.random((10,2))

#### 45. Create random vector of size 10 and replace the maximum value by 0 (★★☆)
v35 = np.random.random(10)
v35[v35.argmax()] = 0
# print(v35)

#### 46. Create a structured array with `x` and `y` coordinates covering the [0,1]x[0,1] area (★★☆)
v36 = np.zeros((5,5), [('x',float),('y',float)])
v36['x'], v36['y'] = np.meshgrid(np.linspace(0,1,5),
                                 np.linspace(0,1,5))
# print(v36)

#### 47. Given two arrays, X and Y, construct the Cauchy matrix C (Cij =1/(xi - yj))
# New task: Contruct matric C where Cij = 1/(xi - yj)

#### 48. Print the minimum and maximum representable value for each numpy scalar type (★★☆)
#for dtype in [np.int8, np.int32, np.int64]:
#    print(np.iinfo(dtype).min)
#    print(np.iinfo(dtype).max)

#### 49. How to print all the values of an array? (★★☆)
# np.set_printoptions(threshold=float("inf"))
# print(np.zeros((16,16)))

#### 50. How to find the closest value (to a given scalar) in a vector? (★★☆)
v50a = np.arange(100)
v50b = np.random.uniform(0, 100)
# print(np.abs(v50a-v50b).argmin())


#### 51. Create a structured array representing a position (x,y) and a color (r,g,b) (★★☆)
#Skipped 

#### 52. Consider a random vector with shape (100,2) representing coordinates, find point by point distances (★★☆)
v52 = np.random.random((10, 2))
v52x, v52y = np.atleast_2d(v52[:,0], v52[:,1])
v52d = np.sqrt( (v52x-v52x.T)**2 + (v52y-v52y.T)**2 )
# print(v52d)

#### 53. How to convert a float (32 bits) array into an integer (32 bits) in place?
v53 = (np.random.rand(10)**100).astype(np.float32)
v53b = v53.view(np.int32)
v53b[:] = v53
# print(v53b)

#### 54. How to read the following file? (★★☆)
"""
1, 2, 3, 4, 5
6,  ,  , 7, 8
 ,  , 9,10,11
"""
# v54 = np.genfromtxt(filename, delimiter=",", dtype=np.int)

#### 55. What is the equivalent of enumerate for numpy arrays? (★★☆)
v55 = np.random.uniform(0, 100, 5)
#for index, value in np.ndenumerate(v55):
 #   print(index, value)
#for index in np.ndindex(v55.shape):
 #   print(index, v55[index])

#### 56. Generate a generic 2D Gaussian-like array (★★☆)
# skipped for now 

#### 57. How to randomly place p elements in a 2D array? (★★☆)
n = 10
p = 3
arr = np.zeros((n,n))
np.put(arr, np.random.choice(range(n*n), p, replace=False), 1)   
# print(arr)

#### 58. Subtract the mean of each row of a matrix (★★☆)
v58 = np.random.uniform(0, 10, 20).reshape((5,4))
# print(v58)
v58 = v58 - v58.mean(axis=1, keepdims=True)
 #print(v58)

#### 59. How to sort an array by the nth column? (★★☆)
v59 = np.random.uniform(0, 10, 30).reshape((5,6))
# print(v59)
n = 4
v59ind = np.argsort(v59[:,n])
# print(v59ind)
v59sorted = v59[v59ind]
# print(v59sorted)

#### 60. How to tell if a given 2D array has null columns? (★★☆)
v60 = np.random.randint(0, 3, (3,10))
print((~v60.any(axis=0)).any())

#### 61. Find the nearest value from a given value in an array (★★☆)


#### 62. Considering two arrays with shape (1,3) and (3,1), how to compute their sum using an iterator? (★★☆)


#### 63. Create an array class that has a name attribute (★★☆)


#### 64. Consider a given vector, how to add 1 to each element indexed by a second vector (be careful with repeated indices)? (★★★)


#### 65. How to accumulate elements of a vector (X) to an array (F) based on an index list (I)? (★★★)


#### 66. Considering a (w,h,3) image of (dtype=ubyte), compute the number of unique colors (★★★)


#### 67. Considering a four dimensions array, how to get sum over the last two axis at once? (★★★)


#### 68. Considering a one-dimensional vector D, how to compute means of subsets of D using a vector S of same size describing subset  indices? (★★★)


#### 69. How to get the diagonal of a dot product? (★★★)


#### 70. Consider the vector [1, 2, 3, 4, 5], how to build a new vector with 3 consecutive zeros interleaved between each value? (★★★)


#### 71. Consider an array of dimension (5,5,3), how to mulitply it by an array with dimensions (5,5)? (★★★)


#### 72. How to swap two rows of an array? (★★★)


#### 73. Consider a set of 10 triplets describing 10 triangles (with shared vertices), find the set of unique line segments composing all the  triangles (★★★)


#### 74. Given an array C that is a bincount, how to produce an array A such that np.bincount(A) == C? (★★★)


#### 75. How to compute averages using a sliding window over an array? (★★★)


#### 76. Consider a one-dimensional array Z, build a two-dimensional array whose first row is (Z[0],Z[1],Z[2]) and each subsequent row is  shifted by 1 (last row should be (Z[-3],Z[-2],Z[-1]) (★★★)


#### 77. How to negate a boolean, or to change the sign of a float inplace? (★★★)


#### 78. Consider 2 sets of points P0,P1 describing lines (2d) and a point p, how to compute distance from p to each line i (P0[i],P1[i])? (★★★)


#### 79. Consider 2 sets of points P0,P1 describing lines (2d) and a set of points P, how to compute distance from each point j (P[j]) to each line i (P0[i],P1[i])? (★★★)


#### 80. Consider an arbitrary array, write a function that extract a subpart with a fixed shape and centered on a given element (pad with a `fill` value when necessary) (★★★)


#### 81. Consider an array Z = [1,2,3,4,5,6,7,8,9,10,11,12,13,14], how to generate an array R = [[1,2,3,4], [2,3,4,5], [3,4,5,6], ..., [11,12,13,14]]? (★★★)


#### 82. Compute a matrix rank (★★★)


#### 83. How to find the most frequent value in an array?


#### 84. Extract all the contiguous 3x3 blocks from a random 10x10 matrix (★★★)


#### 85. Create a 2D array subclass such that Z[i,j] == Z[j,i] (★★★)


#### 86. Consider a set of p matrices wich shape (n,n) and a set of p vectors with shape (n,1). How to compute the sum of of the p matrix products at once? (result has shape (n,1)) (★★★)


#### 87. Consider a 16x16 array, how to get the block-sum (block size is 4x4)? (★★★)


#### 88. How to implement the Game of Life using numpy arrays? (★★★)


#### 89. How to get the n largest values of an array (★★★)


#### 90. Given an arbitrary number of vectors, build the cartesian product (every combinations of every item) (★★★)


#### 91. How to create a record array from a regular array? (★★★)


#### 92. Consider a large vector Z, compute Z to the power of 3 using 3 different methods (★★★)


#### 93. Consider two arrays A and B of shape (8,3) and (2,2). How to find rows of A that contain elements of each row of B regardless of the order of the elements in B? (★★★)


#### 94. Considering a 10x3 matrix, extract rows with unequal values (e.g. [2,2,3]) (★★★)


#### 95. Convert a vector of ints into a matrix binary representation (★★★)


#### 96. Given a two dimensional array, how to extract unique rows? (★★★)


#### 97. Considering 2 vectors A & B, write the einsum equivalent of inner, outer, sum, and mul function (★★★)


#### 98. Considering a path described by two vectors (X,Y), how to sample it using equidistant samples (★★★)?


#### 99. Given an integer n and a 2D array X, select from X the rows which can be interpreted as draws from a multinomial distribution with n degrees, i.e., the rows which only contain integers and which sum to n. (★★★)


#### 100. Compute bootstrapped 95% confidence intervals for the mean of a 1D array X (i.e., resample the elements of an array with replacement N times, compute the mean of each sample, and then compute percentiles over the means). (★★★)


