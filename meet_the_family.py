import json

# define the family with required properties
class Lengaburu:
    def initialize_family(self):
        f = open("family.json", "r")
        data = json.load(f)
        for p in data:
            print(p)
            for key in data["gender"]:
                print (str(key)+'->'+str(''))
        f.close()
    
    def __init__(self):
        # self.name = name
        # self.gender = gender
        self.initialize_family()
    
    



    def add_child(self,mother,child,gender):
        pass

         












f = open("test_file.txt", "r")
for lines in f:
  print(lines)
# print(f.readline())

l = Lengaburu()