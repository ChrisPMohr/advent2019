from fractions import*
e=enumerate
g=lambda x,y: (Fraction(y,x),x>0)if x else y>0
s=set.union(*[{(x,y)for x,v in e(l)if v=='#'} for y,l in e(open('i').readlines())])
print(sorted((len({g(a[0]-o[0],a[1]-o[1])for o in s if o!=a}),a) for a in s)[-1])
