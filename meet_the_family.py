import json
import pprint
from functools import reduce  # forward compatibility for Python 3
import operator

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
        # print(self.family.values())
        # print(self.get_path(self.family, 'Vasa'))
        self.traverse("root", self.family)
        # print(self.branches)
        # path = self.get_branch('Lavnya')
        # print(path.replace('root','family').split('.'))
        print(self.family['children'][2]['children'][0]['children'][0]['name'])
        # self.resolve_branch(path)
        # print(self.search('Lavnya', self.family))
        print(self.family.items())
        print(self.search_member('Vasa', self.family))
    
    
    # def get_path(self,subtree, name,path=None):
    #     path = []
    #     if name == subtree['name']:
    #         path.append('name')
    #         return path
    #     elif 'spouse' in subtree.keys() and  name == subtree['spouse']['name']:
    #         path.append('spouse','name')
    #         return path
    #     else:
    #         if 'children' in subtree.keys() and isinstance(subtree['children'], list):
    #             for i in range(len(subtree['children'])):
    #                     self.get_path(subtree['children'][i], name, path)
                    
    #         else:
    #             return False

    def traverse(self,path,obj):
        cnt = -1
        if isinstance(obj, dict):
            d = obj
            for k, v in d.items():
                if isinstance(v, dict):
                    self.traverse(path + "." + k, v)
                    # self.traverse(path + "['" + k + "']", v)
                elif isinstance(v, list):
                    self.traverse(path + "." + k, v)
                    # self.traverse(path + "['" + k + "']", v)
                else:
                    print(path + "." + k, "=>", v)
                    if 'name' in path + "." + k:
                        self.branches.append((path + "." + k, v))
                        # self.branches.append((path + "['" + k +"']", v))
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

    def search(self,name,obj):
        cnt = -1
        if isinstance(obj, dict):
            d = obj
            for k, v in d.items():
                if isinstance(v, dict):
                    self.search(name, v)
                    # self.traverse(path + "['" + k + "']", v)
                elif isinstance(v, list):
                    self.search(name, v)
                    # self.traverse(path + "['" + k + "']", v)
                else:
                    # print(k,cnt,v)
                    if name in str(v):
                        # self.branches.append((path + "." + k, v))
                        # self.branches.append((path + "['" + k +"']", v))
                        return k, cnt, v
        if isinstance(obj, list):
            li = obj
            for e in li:
                cnt += 1
                if isinstance(e, dict):
                    self.search(name, e)
                elif isinstance(e, list):
                    self.search(name, e)
                else:
                    # print(cnt,e)
                    if name in str(e):
                        return cnt, e
    

    def search_member(self,name,obj):
        nodes = []
        if isinstance(obj,dict):
            for key, val in obj.items():
                if obj['name'] == name:
                    nodes.append(obj['name'])
                    return  nodes
                elif isinstance(obj['children'], dict):
                    nodes.append(obj['children']['name'])
                    self.search_member(name, obj['children'])
        if isinstance(obj, list):
            for e in obj:
                cnt += 1
                if isinstance(e, dict):
                    self.search_member(name, e)
                    nodes.append(obj['children'][cnt]['name'])
                elif isinstance(e, list):
                    self.search_member(name, e)
                    nodes.append(obj['children'][cnt]['name'])
                else:
                    return nodes

    def resolve_branch(self,path):
        subpath = path.replace('root.', '').replace('.','/')
        print(subpath)
        # return reduce(operator.getitem, subpath, self.family)

    def get_branch(self,name):
        for i in range(len(self.branches)):
            if self.branches[i][1] == name:
                print(self.branches[i][0])
                return self.branches[i][0]

    def get_keys(d, to_find):
        for a, b in d.items():
            if to_find in b:
                yield a
            if isinstance(b, dict):
                yield from get_keys(b, to_find)

    

    # def search_name(self,name):
    #     if name == self.family['name']:
    #         return 0, 'name'
    #     elif name == self.family['spouse']['name']:
    #         return 0, 'spouse'
    #     else:
    #         for c in range(len(self.family['children'])):
    #             if name == self.family['children'][c]['name']:
    #                 return c+1, 'name'
    #             elif 'spouse' in self.family['children'][c].keys() and name == self.family['children'][c]['spouse']['name']:
    #                 return c+1, 'spouse'
    #             else:
    #                 if 'children' in self.family['children'][c].keys() and isinstance(self.family['children'][c]['children'], list):
    #                     for gc in range(len(self.family['children'][c]['children'])):
    #                         if name == self.family['children'][c]['name']:
    #                             return gc+1, 'name'
    #                         elif 'spouse' in self.family['children'][c].keys() and name == self.family['children'][c]['spouse']['name']:
    #                             return gc+1, 'spouse'
                    

    # def search_value(self,val):
    #     # for keys in self.self.family[0].keys():
    #     for key in self.family:
    #         if val == self.family[key]:
    #                 # print(i, key, val)
    #                 print(self.family[key])
    #                 return [0, key]
    #         elif len(self.family) > 0 and isinstance(self.family['children'], list):
    #             for i in range(len(self.family['children'])):
    #                 for key in self.family['children'][i]:
    #                     if val == self.family['children'][i][key]:
    #                         print(i,key,val)
    #                         print(self.family['children'][i][key])
    #                         return [i+1,key]
    #         else:
    #             return False
    


    # def search(self, d, k, path=None):
    #     if path is None:
    #         path = []

    #     # Reached bottom of dict - no good
    #     if not isinstance(d, dict):
    #         if not isinstance(d, list):
    #             return False

    #         # Found it!
    #         if isinstance(d, list):
    #             for i in range(len(d)):
    #                 if k in d[i].values():
    #                     path.append(k)
    #                     return path
    #         else:
    #             if k in d.values():
    #                 path.append(k)
    #                 return path

    #     else:
    #         check = list(d.keys())
    #         # Look in each key of dictionary
    #         while check:
    #             first = check[0]
    #             # Note which we just looked in
    #             path.append(first)
    #             if self.search(d[first], k, path) is not False:
    #                 break
    #             else:
    #                 # Move on
    #                 check.pop(0)
    #                 path.pop(-1)
    #         else:
    #             return False
    #         return path
    
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
