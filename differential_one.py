precision = 1000000000
# =3*B3*(B3-B2) + 2*C2*(B3-B2) + C2
x = 0
y = 4
for a in range(0,precision):
    x += 1/precision
    y += 3* (1/precision) * x + 2*(1/precision)*y
print(y)
print(1/precision)
