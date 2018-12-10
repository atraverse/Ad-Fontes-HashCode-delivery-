import math


def file_read():
    lst = []
    with open('redundancy.in', 'r') as f:
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


class Drone():
    def __init__(self):
        self.drone_amount = drones()
        self.max_weight = max_weight()


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

    def check(self, w, pt):
        if pt in self.warehouse_lst[w][1]:
            return True
        else:
            return False


class Order():
    def __init__(self):
        self.fread_lst = file_read()
        self.index = Warehouse().index
        self.count = int(self.fread_lst[self.index][0])
        self.order_list = self.read()
        self.amount = [i[1] for i in self.order_list]

    def read(self):
        lst = []
        for i in range(self.index + 1, self.index + self.count * 3, 3):
            lst_1 = [[int(j) for j in self.fread_lst[i]], [int(j) for j in self.fread_lst[i + 1]],
                     [int(j) for j in self.fread_lst[i + 2]]]
            lst.append(lst_1)
        return lst


class Delivery():
    def __init__(self):
        self.warehouse = Warehouse().warehouse_lst
        self.order = Order().order_list
        self.distance_wo = self.distance()
        self.dev_order = self.dev_order()
        self.wait = []
        self.wo = self.t()

    def dev_order(self):
        if len(self.warehouse) > 1:
            lst = [[] for _ in range(len(self.warehouse))]
            for i in range(1, len(self.distance_wo)):
                for j in range(len(self.distance_wo[0])):
                    if self.distance_wo[i - 1][j] < self.distance_wo[i][j]:
                        lst[i - 1].append(j)
                    else:
                        lst[i].append(j)
            return lst
        else:
            return self.distance_wo

    def t(self):
        lst = [[] for _ in range(len(self.warehouse))]
        w = [i[1] for i in Warehouse().warehouse_lst]
        order = self.dev_order
        o = [i[2] for i in Order().order_list]
        for i in range(len(lst)):
            lst[i].append(w[i])
        for i in range(len(order)):
            for j in order[i]:
                lst[i].append(o[j])
            lst[i].append(order[i])
        return lst

    def check(self):
        lst = [[] for _ in range(len(self.wo))]
        war = [self.wo[i][0] for i in range(len(self.wo))]
        for i in self.wo:
            i.remove(i[0])
        for i in self.wo:
            item = i[:len(i) - 1]
            for j in item:
                for k in j:
                    if war[self.wo.index(i)][k] == 0:
                        n = item.index(j)
                        lst[self.wo.index(i) - 1].append(
                            self.wo[self.wo.index(i)][len(self.wo[self.wo.index(i)]) - 1][n])
                    else:
                        n = item.index(j)
                        lst[self.wo.index(i)].append(self.wo[self.wo.index(i)][len(self.wo[self.wo.index(i)]) - 1][n])
        return lst

    def deliver(self):
        step = -1
        dev_step = []
        ord = [i[2] for i in self.order]
        lst = self.check()
        for lst_c_num in lst:
            for c_num in lst_c_num:
                for k in self.order[c_num][2]:
                    if self.warehouse[lst.index(lst_c_num)][1][k] == 0:
                        print(lst.index(lst_c_num), 'L', lst.index(lst_c_num), k, 1)
                        step += 1
                    else:
                        print(lst.index(lst_c_num), 'L', lst.index(lst_c_num), k, 1)
                        print(lst.index(lst_c_num), 'D', c_num, k, 1)
                        step += 2
                        ord[c_num].remove(k)
                    if len(ord[c_num]) == 0:
                        print()
                        dev_step.append(step)

        return step, dev_step

    def score(self):
        step, dev_step = self.deliver()
        score = 0
        for i in dev_step:
            score += ((step - i) / step) * 100
        return round(score)

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


def main():
    print(Delivery().score())


if __name__ == "__main__":
    main()
