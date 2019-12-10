from fractions import*
e=enumerate
def g(a,b):
 x,y=a[0]-b[0],a[1]-b[1]
 return(Fraction(y,x),x>0)if x else y>0
s=set.union(*[{(x,y)for x,v in e(l)if v=='#'} for y,l in e(open('i').readlines())])
print(sorted((len({g(a,o)for o in s if o!=a}),a) for a in s)[-1])
