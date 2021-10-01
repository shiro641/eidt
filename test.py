import sys
'''a = int(sys.argv[1])
b = int(sys.argv[2])'''
file = open(sys.argv[1])
str = file.read().split()
print(str[0] + str[1])
#print(sys.argv)
