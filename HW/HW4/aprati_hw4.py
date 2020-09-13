# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 10:54:13 2020

@author: miame
"""

import matplotlib.pyplot as plt
import time
import numpy as np
import statistics
import os

os.chdir('C:/Users/miame/Documents/GitHub/python_summer2020/HW/HW4')

# different efficiencies reference:
# https://www.geeksforgeeks.org/time-complexities-of-all-sorting-algorithms/

# =============================================================================
# selection sort - O(n^2)
# code taken from lecture notes
# =============================================================================

def selection_sort(numbers):
    # Answer object 
    numbers = numbers.copy()  # to not modify the original input
    answer = []
    while len(numbers) > 0:
        answer.append(min(numbers))
        del numbers[numbers.index(answer[-1])]    
    return answer

# =============================================================================
# testing selection sort
# =============================================================================

number_list = [10, 1, 3, 4, 5, 2, 7]
print(selection_sort(number_list))

# =============================================================================
# heap sort - O(n log(n)) (conceptually similar to selection sort)
# def of algorithm: https://en.wikipedia.org/wiki/Heapsort
# =============================================================================

def heap_sort(num_list):
    numbers_list = num_list.copy() #don't overwrite original
    count = len(numbers_list)
    end = count - 1 # because you index at 0
    #building original heap
    original_heap = heapify(numbers_list, count)
    while end > 0:
        swap(original_heap, end, 0)
        end = end - 1
        sift_down(original_heap, 0, end)
    return numbers_list

# https://www.geeksforgeeks.org/python-program-to-swap-two-variables/
def swap(numbers_list, pos1, pos2):
    numbers_list[pos1], numbers_list[pos2] = numbers_list[pos2], numbers_list[pos1]
    return numbers_list

# put elements of the array in heap order
def heapify(num_list, len_num_list):
    # finding the last parent node to be the starting point:
    start = ((len_num_list-1)-1) // 2
    #sift down the node at index start s.t. all nodes below start are in heap order
    while start >= 0:
        heaped_list = sift_down(num_list, start, (len_num_list-1))
        # go to the next parent
        start = start - 1
        # when done, should be in heap order
    return heaped_list

# repair the heap that was ruined with the swap
def sift_down(num_list, start, end):
    root = start # for naming clarity
    #while root has at least one left child:
    while (2*root + 1) <= end: #left child of the root is <= to end
        child = 2*root + 1 # child is the left child
        swap_child = root #tracking child to swap with

    # now determining which children to swap: one child must be the largest node
        # if the swap child is less than the left child, swap
        if num_list[swap_child] < num_list[child]:
            swap_child = child
        # if there is a right child and it is greater, swap
        if child + 1 <= end and num_list[swap_child] < num_list[child + 1]:
            swap_child = child + 1
        # root needs to be the largest; if that is the case, then we are done
        if swap_child == root:
            break
        else:
            num_list = swap(num_list, root, swap_child)
            root = swap_child
    return num_list
# =============================================================================
# testing heaped sort
# =============================================================================

print(heap_sort(number_list))

# =============================================================================
# simulations
# lists of different lenghts to be sorted, each list to be sorted 5 times
# =============================================================================

# creating the test lists to be sorted, of different lengths, up to 'total'

total = 5 #max number of 0s for length of list to be simulated
N = [i for i in range(1, total+1)]
simulations = []
x_axis = [] # for the plot

for i in N:
    new_list = list(np.random.permutation(10**N[i-1]))
    simulations.append(new_list)
    x_axis.append(10**N[i-1])

print(x_axis)

# selection sort simulations

sim_select = simulations
min_times_select = []
max_times_select = []
mean_times_select = []

print("Starting selection sort simulations: ")

for sim_list in sim_select:
    print("List #: " + str(len(str(len(sim_list))) - 1))
    all_times = []
    for i in range(5):
        print("Simulation #: " + str(i + 1))
        start_time = time.time()
        selection_sort(sim_list)
        all_times.append(round((time.time() - start_time), 3))

    min_times_select.append(min(all_times))
    max_times_select.append(max(all_times))
    mean_times_select.append(round(statistics.mean(all_times), 3))

#heap sort simulations

sim_heap = simulations
min_times_heap = []
max_times_heap = []
mean_times_heap = []

print("Starting heap sort simulations: ")

for sim_list in sim_heap:
    print("List #: " + str(len(str(len(sim_list))) - 1))
    all_times = []
    for i in range(5):
        print("Simulation #: " + str(i + 1))
        start_time = time.time()
        selection_sort(sim_list)
        all_times.append(round((time.time() - start_time), 3))

    min_times_heap.append(min(all_times))
    max_times_heap.append(max(all_times))
    mean_times_heap.append(round(statistics.mean(all_times), 3))

# =============================================================================
# plotting
# =============================================================================

# mean run times
plt.figure(figsize=(10,5))

plt.plot(x_axis, mean_times_select, color = 'red')
plt.plot(x_axis, mean_times_heap, color = 'blue')
plt.legend(['Selection Sort: O(n^2)','Heapsort: O(n log(n))'],
           loc = "upper left", prop = {"size":10})
plt.ylabel("Mean Time (seconds)")
plt.xlabel("Length of List")
plt.title("Mean Execution Time vs List Length")
#plt.show()

plt.savefig('mean_times.png')

# min run times
plt.figure(figsize=(10,5))

plt.plot(x_axis, min_times_select, color = 'red')
plt.plot(x_axis, min_times_heap, color = 'blue')
plt.legend(['Selection Sort: O(n^2)','Heapsort: O(n log(n))'],
           loc = "upper left", prop = {"size":10})
plt.ylabel("Best Time (seconds)")
plt.xlabel("Length of List")
plt.title("Best Execution Time vs List Length")
#plt.show()

plt.savefig('min_times.png')

# max run times
plt.figure(figsize=(10,5))

plt.plot(x_axis, max_times_select, color = 'red')
plt.plot(x_axis, max_times_heap, color = 'blue')
plt.legend(['Selection Sort: O(n^2)','Heapsort: O(n log(n))'],
           loc = "upper left", prop = {"size":10})
plt.ylabel("Worst Time (seconds)")
plt.xlabel("Length of List")
plt.title("Worst Execution Time vs List Length")
#plt.show()

plt.savefig('max_times.png')

# all times
plt.figure(figsize=(10,5))

plt.plot(x_axis, mean_times_select, color = 'red')
plt.plot(x_axis, mean_times_heap, color = 'blue')

plt.plot(x_axis, min_times_select, ':', color = 'red')
plt.plot(x_axis, max_times_select, ':', color = 'red')
plt.plot(x_axis, mean_times_select, color = 'red')
plt.plot(x_axis, min_times_heap, ':', color = 'blue')
plt.plot(x_axis, max_times_heap, ':', color = 'blue')
plt.plot(x_axis, mean_times_heap, color = 'blue')
plt.legend(['Selection Sort: O(n^2)','Heapsort: O(n log(n))'],
           loc = "upper left", prop = {"size":10})
plt.ylabel("Time (seconds)")
plt.xlabel("Length of List")
plt.title("Execution Times (min, mean, max) vs List Length")
#plt.show()

plt.savefig('all_times.png')


