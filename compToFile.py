import sys
import calc_avg_and_var as c

alg = sys.argv[1]

f = open('compResMean/'+alg,'w')
f1 = open('compResStd/'+alg,'w')
for i in range(2,16):
	res = c.calculate('results/'+alg+'_'+str(i)) 
	f.write(str(i)+' '+str(res[0])+'\n')
	f1.write(str(i)+' '+str(res[2])+'\n')
f.close()
f1.close()