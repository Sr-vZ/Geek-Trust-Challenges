import json

# define the family with required properties
class Lengaburu:
    family = {}
    def initialize_family(self):
        f = open("family.json", "r")
        data = json.load(f)
        # for p in data:
            # print(p)
            # for key in data["gender"]:
                # print (str(key)+'->'+str(''))
        f.close()
        self.add_member('King Shan',None,'Male','Queen Anga')
        # print(self.family[0].values().key('Queen Anga'))
        self.add_member('Chit', 'Queen Anga', 'Male', 'Amba')
        self.add_member('Dritha', 'Amba', 'Female', 'Jaya')

    
    def __init__(self):
        # self.name = name
        # self.gender = gender
        self.initialize_family()
        print(self.family)
        # print(self.family[0].keys())
        self.search_value('Amba')
    
    

    def search_value(self,val):
        # for keys in self.self.family[0].keys():
        for key in self.family:
            if val == self.family[key]:
                    # print(i, key, val)
                    print(self.family[key])
                    return [0, key]
        if len(self.family) > 0 and isinstance(self.family['children'], list):
            for i in range(len(self.family['children'])):
                for key in self.family['children'][i]:
                    if val == self.family['children'][i][key]:
                        print(i,key,val)
                        print(self.family['children'][i][key])
                        return [i,key]
                    else:
                        return False

    def add_member(self,name,mother,gender,spouse):
        res = self.search_value(mother)
        print(res)
        if len(self.family) > 0 and res!=False:
            if len(self.family['children']) > 0:
                self.family['children'][res[0]].append(dict({
                    "name": name,
                    "mother": mother,
                    "gender":gender,
                    "spouse":spouse,
                    "children":[]
                }))
            else:
                self.family['children'].append(dict({
                    "name": name,
                    "mother": mother,
                    "gender": gender,
                    "spouse": spouse,
                    "children": []
                }))
        else:
            self.family.update({
                "name": name,
                "mother": mother,
                "gender": gender,
                "spouse": spouse,
                "children": []
            })

         












f = open("test_file.txt", "r")
for lines in f:
  print(lines)
# print(f.readline())

l = Lengaburu()
