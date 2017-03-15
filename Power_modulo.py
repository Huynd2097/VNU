# x = (b**n) % m

b = 6531678
n = 11947181
m = 14755801


a = bin(n)[2:] #bin = '0b...'
k = len(a)
x = 1
p = b % m
for i in xrange(0, k):
	if a[k-i-1] == '1':
		x = (x*p) % m
	p = (p*p) % m

	print x , p

print 'x=', x
