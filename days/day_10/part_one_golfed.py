from fractions import Fraction as F
e=enumerate
def g(a,b):
 x,y=a[0]-b[0],a[1]-b[1]
 return(F(y,x),x>0)if x!=0 else y>0
with open('i')as f:
 s=set.union(*[{(x,y)for x,v in e(l)if v=='#'} for y,l in e(f.readlines())])
 print(sorted([(len(set(g(a,o)for o in s if o!=a)),a) for a in s],reverse=True)[0])
