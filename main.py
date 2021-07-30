from lomr1 import *


request = SampleGameRequest()
response = SampleGameHandler().handle(request)
print(response.winner)
