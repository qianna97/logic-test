# test
n = 50
result = []
for x in range(1, n+1):
    if x % 3 == 0 and x % 5 == 0:
        result.append('Frontend\nBackend')
    elif x%3 == 0 and x%5 !=0:
        result.append('Frontend')
    elif x%5 == 0 and x%3 != 0:
        result.append('Backend')
    else:
        result.append(str(x))

print(','.join(result))
