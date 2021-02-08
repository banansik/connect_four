def wmyrange(start, stop = None, step = 1):
    pass



def myRange(start, stop=None, step=None):

    if stop == None:
        stop = start

    if step == None:
        step = 1

    while start < stop:

        yield start
        start = start+step




for x in myRange(-5,5,2):
    print(x)

print('test')
for z in range(-5,5):
    print(z)
