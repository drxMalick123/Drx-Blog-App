# Quick Sort function
def quick_sort(arr):
    # Base case: if the list has one or zero elements, it's already sorted
    if len(arr) <= 1:
        return arr
    
    # Choose a pivot element (you can choose any element; here we choose the last one)
    pivot = arr[-1]
    
    # Lists to hold values less than, equal to, and greater than the pivot
    less_than_pivot = [x for x in arr[:-1] if x <= pivot]
    greater_than_pivot = [x for x in arr[:-1] if x > pivot]
    
    # Recursively apply quick sort to the sublists and combine the results
    return quick_sort(less_than_pivot) + [pivot] + quick_sort(greater_than_pivot)
if __name__ == '__main__':
# Example usage
    unsorted_list = [12, 4, 7, 9, 2, 5, 1, 6]
    sorted_list = quick_sort(unsorted_list)
    print("Sorted List:", sorted_list)
    