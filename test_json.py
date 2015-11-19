import json


#with open('test.json','w') as outfile:
    #json.dump({'xxxx':0}, outfile)
    #outfile.close()


with open('new.json','r+') as outfile:

    outfile.write(json.dumps({'xxx':0}))

    #print(outfile.read())
    outfile.close()