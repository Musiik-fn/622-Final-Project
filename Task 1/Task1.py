# If you would like to test the functional code for task 1, go ahead and run this script.
def getUserInputs():
    """A function which will handle getting the inputs from the user: a list of integers. 
    
    Returns:
    - userList, userInt
    
    Entering an empty string will exit the function.
    """
    while True:
        userIntergerInput = input('Enter the integer you would like to search for: ')
        if userIntergerInput == "":
            return None
        try: 
            userInt = int(userIntergerInput)
            break
        except ValueError as er:
            print(f'Error: Could not convert the target into an integer, please try again. Error: {er}')
    
    while True:
        input_string = input(f"Enter elements separated by commas. Your target is {userInt}: ")

        # exit user input function
        if input_string.strip() == "":
            print("No input received. Exiting function.")
            return None  
        
        # handle string to list conversion. checks that each element is an int
        input_list = input_string.split(',')
        try:
            userList = [int(element.strip()) for element in input_list]
            return userList, userInt
        except ValueError as e:
            print(f"Error: Could not convert a value into an integer, please try again. Error: {e}")

def linearSearchIterative(sourceList, target):
    """Finds the target within the `sourceList` using the linear search method iteratively.
    Args:
        sourceList (list): A list of `int` values
        target (int): The `int` value that will be searched for
    Retuns:
        If the `target` is found, the index of the `sourceList` is returned. `False` is returned if otherwise
    """
    for index, each in enumerate(sourceList):
        if each == target:
            return index
    return False

def linearSearchRecursive(sourceList, target, index=0):
    """Finds the target within the `sourceList` using the linear search method recursively. 
    Args:
        sourceList (list): A list of `int` values
        target (int): The `int` value that will be searched for
    Retuns:
        If the `target` is found, the index of the `sourceList` is returned. `False` is returned if otherwise
    """
    if sourceList[0] == target: # target found case
        return index 
    elif len(sourceList) == 1: # target not found case
        return False
    else: # recursion
        return linearSearchRecursive(sourceList[1:], target, index + 1)

def binarySearchIterative(sourceList, target):
    """Uses binary search to find the target within a sorted list. Returns the position of the target, if found, and `False` otherwise. Uses an iterative approach.

    Args:
        sourceList (list): A list of `int` values
        target (int): The `int` value that will be searched for
    """
    left = 0
    right = len(sourceList) - 1

    if target == sourceList[left]:
        return left
    elif target == sourceList[right]:
        return right
    else:
        while left <= right: # ensures that there are numbers in between to still go through
            midpoint_index = (left + right) // 2
            if target == sourceList[midpoint_index]:
                return midpoint_index
            elif target < sourceList[midpoint_index]:
                right = midpoint_index - 1
            else: 
                left = midpoint_index + 1

        return False

def binarySearchRecursive(sourceList, target, left=0, right=None):
    """Uses binary search to find the target within a sorted list. Returns the position of the target, if found, and `False` otherwise. Uses a recursive approach.
    Args:
        sourceList (list): A sorted list of `int` values
        target (int): The `int` value that will be searched for
        left (int, optional): The starting index of the sublist to search within. Default is 0.
        right (int, optional): The ending index of the sublist to search within. Default is the last index of the list.
    """
    if right is None:
        right = len(sourceList) - 1

    if left <= right:
        midpoint_index = (left + right) // 2
        if sourceList[midpoint_index] == target:
            return midpoint_index
        elif target < sourceList[midpoint_index]:
            return binarySearchRecursive(sourceList, target, left, midpoint_index - 1)
        else:
            return binarySearchRecursive(sourceList, target, midpoint_index + 1, right)
    else:
        return False

def main():
    import time

    while True:
        result = getUserInputs()
        if result is None:
            print("No input received, exiting the program.")
            return
        
        userList, userInt = result
        isSorted = userList == sorted(userList)

        print(f'RESULTS REPORT:\n---\nYour inputs were the following:\nSource List: {userList}. Sorted Bool: {isSorted}\nTarget Integer: {userInt}\n---')

        # Measure execution time for linear search iterative
        start_time = time.time()
        linearResultIter = linearSearchIterative(userList, userInt)
        linear_iter_time = time.time() - start_time

        # Measure execution time for linear search recursive
        start_time = time.time()
        linearResultRec = linearSearchRecursive(userList, userInt)
        linear_rec_time = time.time() - start_time

        print(f'Linear Search Results:\n\tLinear Search Iterative: {linearResultIter} (Time: {linear_iter_time}s)\n\tLinear Search Recursive: {linearResultRec} (Time: {linear_rec_time}s)')

        if isSorted:
            # Measure execution time for binary search iterative
            start_time = time.time()
            binaryResultIter = binarySearchIterative(userList, userInt)
            binary_iter_time = time.time() - start_time

            # Measure execution time for binary search recursive
            start_time = time.time()
            binaryResultRec = binarySearchRecursive(userList, userInt)
            binary_rec_time = time.time() - start_time

            print(f'Binary Search Results:\n\tBinary Search Iterative: {binaryResultIter} (Time: {binary_iter_time}s)\n\tBinary Search Recursive: {binaryResultRec} (Time: {binary_rec_time}s)')
        else:
            print("List is not sorted, skipping binary search.")

        # Ask user if they want to continue or exit
        continue_choice = input("---\nThat was exciting! Do you want to perform another search? Enter 'yes' to continue or 'no' to exit: ").strip().lower()
        if continue_choice != 'yes':
            print("Exiting program and shutting off all mission systems. Enjoy the rest of your day, and thanks for everything, Professor Pouyan. We hope to see you again in the next semesters.")
            break

if __name__ == '__main__':
    main()
