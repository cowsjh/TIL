import numpy as np

arr1 = np.array([[[0,1],
                [2,3],
                [4,5]],
                
                [[1,5],
                [6,4],
                [5,2]]])

print(arr1.sum(axis=0))
print(arr1.sum(axis=1))
print(arr1.sum(axis=2))

scan = np.array([3, 4, 2, 6, 1,10])
near = scan<5
middle = near & (scan > 2)
valid = scan[middle]

print(valid)