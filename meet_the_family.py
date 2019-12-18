import json

# define the family with required properties
class family(object):
    def initialize_family(self):
        f = open("family.json", "r")
        data = json.load(f)
        for key in data.keys():
            # print(key)
            if isinstance(data[key], list) == False:
                print(key, data[key])
            else:
                for x in data[key]:
                    if isinstance(x, dict):
                        for childKey in x.keys():
                            if isinstance(x[childKey], list) == False:
                                print(childKey, x[childKey])
                            else:
                                for y in x[childKey]:
                                    if isinstance(x[childKey], list) == False:
                                        print(y, y[childKey])


        f.close()
    
    def __init__(self):
        self.name = None
        self.gender = None
        self.spouse = None
        self.child = []
        self.initialize_family()


    def createChildren(self,amount):
        for i in range(0,amount):
            self.child.append(family())
    
    
    # def setChildrenValues(self,list):
    #     for i in range(0,len(list)):
    #         self.data.append(list[i])

         












f = open("test_file.txt", "r")
for lines in f:
  print(lines)
# print(f.readline())

l = family()