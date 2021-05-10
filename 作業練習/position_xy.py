width = 5
height = 5
y = 0
output = ""

while y < height:
    x = 0
    while x < width:
        output = output+"({},{})".format(x, y)
        x = x+1
    output = output+"\n"
    y = y+1

print(output)
