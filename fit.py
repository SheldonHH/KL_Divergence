y = [11, 20, 19, 17, 10]
y_bar = [12, 18, 19.5, 18, 9]
summation = 0  # variable to store the summation of differences
n = len(y)  # finding total number of items in list
for i in range(0, n):  # looping through each element of the list
    # finding the difference between observed and predicted value
    difference = y[i] - y_bar[i]
    squared_difference = difference**2  # taking square of the differene
    # taking a sum of all the differences
    summation = summation + squared_difference
MSE = summation/n  # dividing summation by total values to obtain average
print("The Mean Square Error is: ", MSE)
