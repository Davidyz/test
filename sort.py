"""
A custom module contaaining some sorting algorithms.
Recursion is widely used.
"""
def quicksort(array):
    if len(array) < 2:
        return array

    mid = array[0]
    more = []
    less = []
    for i in array[1:]:
        if i >= mid:
            more.append(i)
        elif i < mid:
            less.append(i)

    return quicksort(less) + [mid] + quicksort(more)

def bubblesort(array):
    if len(array) < 2:
        return array

    def switch(ls, index = 0):
        if index >= len(ls) - 2:
            return ls

        elif ls[index] > ls[index + 1]:
            ls[index], ls[index + 1] = ls[index + 1], ls[index]
            
        return switch(ls, index + 1)
    
    switch(array)

    return bubblesort(array[:-1]) + [array[-1]]
