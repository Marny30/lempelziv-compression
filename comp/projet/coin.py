from random import random
a=0.887















































































def fairCoin(biasedCoin):
   coin1, coin2 = 0,0
   while coin1 == coin2:
      coin1, coin2 = biasedCoin(), biasedCoin()
   return coin1



def biasedCoin():
   return int(random() < a)


#sum(biasedCoin() for i in range(10000))
#sum(fairCoin(biasedCoin) for i in range(10000))


j=0.0
ll=0.0
for i in range (10000000):
	j+=biasedCoin()
	ll+=fairCoin(biasedCoin)
print "on a base"+str(j/100000)+"contre"+str(ll/100000)
