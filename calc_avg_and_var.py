import sys
import math

def calculate(file):
	with open(file) as f:
		content = f.readlines() 
	content = [x.strip() for x in content]
	#print('\n' + "----Results----" + '\n')
	#print("content: " + str(content) + '\n')

	mean = 0
	for i in content:
		mean += float(i)

	mean = mean/len(content)

	var = 0
	for i in content:
		var += ((float(i) - mean) ** 2)

	var = var/len(content)

	std = math.sqrt(var)

	res = [mean,var,std]

	#print(res)
	return res
	#print("mean: " + str(mean) + '\n')
	#print("variance: " + str(var) + '\n')
	#print("standard deviation: " + str(std))

#calculate(sys.argv[1])