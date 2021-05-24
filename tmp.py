
import math as m 
import vice 

out = vice.output("./outputs/diffusion/twoinfall_ifrmode") 
mstar = sum([out.zones[_].history["mstar"][-1] for _ in out.zones.keys()]) 
print("mstar = %.5e" % (mstar)) 
