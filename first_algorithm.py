import math


def file_read():
    lst = []
    with open("mother_of_all_warehouses.in", 'r') as f:
        line = [i.replace('\n', '') for i in f]
    for i in line:
        lst.append(i.split(" "))
    return lst


def row_columns():
    lst = file_read()
    rc = [int(lst[0][0]), int(lst[0][1])]
    return rc


def drones():
    lst = file_read()
    drone = int(lst[0][2])
    return drone


def turns():
    lst = file_read()
    turn = int(lst[0][3])
    return turn


def max_weight():
    lst = file_read()
    weigth = int(lst[0][4])
    return weigth


def products_tw():
    lst = file_read()
    prod_list = []
    for i in range(0, int(lst[1][0])):
        lst_1 = [i + 1, int(lst[2][i])]
        prod_list.append(lst_1)
    return prod_list


def distance(lst1, lst2):
    distances = round(math.sqrt(abs(lst1[0] - lst2[0]) ** 2 + abs(lst1[1] - lst2[1]) ** 2))
    return distances

def write_to_file(i):
    with open('result1.txt', 'a') as f:
        f.write(i)
        f.write("\n")

class Warehouse():
    def __init__(self):
        self.fread_lst = file_read()
        self.count = int(self.fread_lst[3][0])
        self.index = 4 + self.count * 2
        self.warehouse_lst = self.read()

    def read(self):
        lst = []
        for i in range(4, 4 + self.count * 2, 2):
            lst_1 = [[int(j) for j in self.fread_lst[i]], [int(j) for j in self.fread_lst[i + 1]]]
            lst.append(lst_1)
        return lst
    def check(self, prod, w):
        if self.warehouse_lst[w][1][prod] != 0:
            return True
        else:
            return False

class Order():
    def __init__(self):
        self.fread_lst = file_read()
        self.index = Warehouse().index
        self.count = int(self.fread_lst[self.index][0])
        self.order_list = self.read()

    def read(self):
        lst = []
        for i in range(self.index + 1, self.index + self.count * 3, 3):
            lst_1 = [[int(j) for j in self.fread_lst[i]], [int(j) for j in self.fread_lst[i + 1]],
                     [int(j) for j in self.fread_lst[i + 2]]]
            lst.append(lst_1)
        return lst

def load(d, w, pt, a):
    a = '{} L {} {} {}'.format(d, w, pt, a)
    write_to_file(a)

def delivery(d, w, pt, am):
    a = '{} D {} {} {}'.format(d, w, pt, am)
    write_to_file(a)

class Delivery():
    def __init__(self):
        self.warehouse = Warehouse().warehouse_lst
        self.order = Order().order_list
        self.distance_wo = self.distance()
        self.dev_order = self.dev_order()
        self.score = []
        self.wait = []

    def distance(self):
        lst_1 = []
        w_distance = [self.warehouse[i][0] for i in range(0, len(self.warehouse))]
        o_distance = [self.order[i][0] for i in range(0, len(self.order))]
        for i in w_distance:
            lst = []
            for j in o_distance:
                d = distance(i, j)
                lst.append(d)
            lst_1.append(lst)
        return lst_1

    def dev_order(self):
        if len(Warehouse().warehouse_lst)>1:
            lst = [[] for _ in range(len(self.distance_wo))]
            for i in range(1, len(self.distance_wo)):
                for j in range(len(self.distance_wo[0])):
                    if self.distance_wo[i - 1][j] < self.distance_wo[i][j]:
                        lst[i - 1].append(j)
                    else:
                        lst[i].append(j)
            return lst
        else:
            return self.distance_wo
    def dev(self):
        step = 0
        print(self.dev_order)
        for i in range(len(self.dev_order)):
            for j in self.dev_order[i]:
                for k in self.order[j][2]:
                    if Warehouse().check(k, i):
                        # load(i, i, k, self.order[j][1][0])
                        step +=1
                        # delivery(i, j, k, self.order[j][1][0])
                        step +=1
                        self.score.append(step)
                    else:
                        w = i+1
                        # load(i, w, k, self.order[j][1][0])
                        step += 1
                        # delivery(i, w, k, self.order[j][1][0])
                        step+=1
                        self.score.append(step)
        return step, self.score



def score():
    sc, st = Delivery().dev()
    lst_sum = []
    for i in st:
        a = ((sc-i)*100/sc)
        lst_sum.append(a)
    with open("result.txt", 'a')as f:
        f.write(str(sum(lst_sum)))
        f.write("\n")

score()
# print(len(Warehouse().warehouse_lst))