
def DictinList_duplicate(data_list):
    """
    列表套字典去重
    :return:
    """
    seen = set()
    new_l = []
    for d in data_list:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)
    print(new_l)

x = []
for i in range(1,5):
    a = {"key":"1",
    "v":"dlf"
     }
    x.append(a)
DictinList_duplicate(x)