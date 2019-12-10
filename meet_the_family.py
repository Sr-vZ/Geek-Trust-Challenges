import json
import pprint

# define the family with required properties
class Lengaburu:
    family = {}
    branches = []
    def initialize_family(self):
        f = open("family.json", "r")
        data = json.load(f)
        self.family = data
        # for p in data:
            # print(p)
            # for key in data["gender"]:
                # print (str(key)+'->'+str(''))
        f.close()
        # pprint.pprint(data)
        print(self.family['children'][1]['spouse'])
        # print(self.family.items())
        # self.add_member('King Shan',None,'Male','Queen Anga')
        # # print(self.family[0].values().key('Queen Anga'))
        # self.add_member('Chit', 'Queen Anga', 'Male', 'Amba')
        # self.add_member('Dritha', 'Amba', 'Female', 'Jaya')

    
    def __init__(self):
        # self.name = name
        # self.gender = gender
        self.initialize_family()
        # pprint.pprint(self.family)
        print(self.family.values())
        print(self.get_path(self.family, 'Vasa'))
        self.traverse("root", self.family)
        print(self.branches)
    
    
    def get_path(self,subtree, name,path=None):
        path = []
        if name == subtree['name']:
            path.append('name')
            return path
        elif 'spouse' in subtree.keys() and  name == subtree['spouse']['name']:
            path.append('spouse','name')
            return path
        else:
            if 'children' in subtree.keys() and isinstance(subtree['children'], list):
                for i in range(len(subtree['children'])):
                        self.get_path(subtree['children'][i], name, path)
                    
            else:
                return False

    def traverse(self,path,obj):
        cnt = -1
        if isinstance(obj, dict):
            d = obj
            for k, v in d.items():
                if isinstance(v, dict):
                    self.traverse(path + "." + k, v)
                elif isinstance(v, list):
                    self.traverse(path + "." + k, v)
                else:
                    print(path + "." + k, "=>", v)
                    if 'name' in path + "." + k:
                        self.branches.append((path + "." + k, v))
        if isinstance(obj, list):
            li = obj
            for e in li:
                cnt += 1
                if isinstance(e, dict):
                    self.traverse("{path}[{cnt}]".format(path=path, cnt=cnt), e)
                elif isinstance(e, list):
                    self.traverse("{path}[{cnt}]".format(path=path, cnt=cnt), e)
                else:
                    print("{path}[{cnt}] => {e}".format(path=path, cnt=cnt, e=e))
                    if 'name' in "{path}[{cnt}]".format(path=path, cnt=cnt):
                        self.branches.append(("{path}[{cnt}]".format(path=path, cnt=cnt),e))


    def search_name(self,name):
        if name == self.family['name']:
            return 0, 'name'
        elif name == self.family['spouse']['name']:
            return 0, 'spouse'
        else:
            for c in range(len(self.family['children'])):
                if name == self.family['children'][c]['name']:
                    return c+1, 'name'
                elif 'spouse' in self.family['children'][c].keys() and name == self.family['children'][c]['spouse']['name']:
                    return c+1, 'spouse'
                else:
                    if 'children' in self.family['children'][c].keys() and isinstance(self.family['children'][c]['children'], list):
                        for gc in range(len(self.family['children'][c]['children'])):
                            if name == self.family['children'][c]['name']:
                                return gc+1, 'name'
                            elif 'spouse' in self.family['children'][c].keys() and name == self.family['children'][c]['spouse']['name']:
                                return gc+1, 'spouse'
                    

    def search_value(self,val):
        # for keys in self.self.family[0].keys():
        for key in self.family:
            if val == self.family[key]:
                    # print(i, key, val)
                    print(self.family[key])
                    return [0, key]
            elif len(self.family) > 0 and isinstance(self.family['children'], list):
                for i in range(len(self.family['children'])):
                    for key in self.family['children'][i]:
                        if val == self.family['children'][i][key]:
                            print(i,key,val)
                            print(self.family['children'][i][key])
                            return [i+1,key]
            else:
                return False
    
    def getpath(self,nested_dict, value, prepath=()):
        for k, v in nested_dict.items():
            path = prepath + (k,)
            if v == value:  # found value
                return path
            elif hasattr(v, 'items'):  # v is a dict
                p = self.getpath(v, value, path)  # recursive call
                if p is not None:
                    return p

    def search(self, d, k, path=None):
        if path is None:
            path = []

        # Reached bottom of dict - no good
        if not isinstance(d, dict):
            if not isinstance(d, list):
                return False

            # Found it!
            if isinstance(d, list):
                for i in range(len(d)):
                    if k in d[i].values():
                        path.append(k)
                        return path
            else:
                if k in d.values():
                    path.append(k)
                    return path

        else:
            check = list(d.keys())
            # Look in each key of dictionary
            while check:
                first = check[0]
                # Note which we just looked in
                path.append(first)
                if self.search(d[first], k, path) is not False:
                    break
                else:
                    # Move on
                    check.pop(0)
                    path.pop(-1)
            else:
                return False
            return path
    
    def add_member(self,name,mother,gender,spouse):
        res = self.search_value(mother)
        print(res)
        if len(self.family) > 0 and res!=False:
            if len(self.family['children']) > 0 and res[0] > 0:
                self.family['children']['children'].append(dict({
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
