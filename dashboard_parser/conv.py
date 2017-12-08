txtstr = []


with open("headers.txt") as f : 
    for line in f:
        line = line.strip("\n")
#        import pdb;pdb.set_trace()
        print("\"{}\"".format(line))
        txtstr.append("\"{}\"".format(line))

with open("headers3.txt","w") as f :
    
    for each in txtstr : 

        f.write(each+"\n")

