def myfunction(k):
    if k>0:
        result = k + myfunction(k-1)
        print(result)
    else:
        result = 0
    return result
myfunction(4)