import enchant
import random
import copy
import os

def genrow():
    letters = "abcdefghijklmnopqrstuvwxyz"
    return [letters[random.randint(0,25)],letters[random.randint(0,25)],letters[random.randint(0,25)],letters[random.randint(0,25)]]

class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def return_children(self):
        return self.children

    def return_data(self):
        return self.data

def gos(tree, a, b):
    newchilds = tree.return_data()
    last = newchilds[len(newchilds) - 1]
    rest = copy.deepcopy(newchilds)
    new = (last[0] + a, last[1] + b)
    rest.append(new)
    tree.add_child(Node(rest))

def addlayer(tree):
    gos(tree, -1, 0)
    gos(tree, 1, 0)
    gos(tree, 0, 1)
    gos(tree, 0, -1)
    gos(tree, 1, 1)
    gos(tree, -1, -1)
    gos(tree, 1, -1)
    gos(tree, -1, 1)


def addlayertwo(tree):
    if tree.return_children() == []:
        addlayer(tree)
    else:
        for x in tree.return_children():
            addlayertwo(x)


def allchildren(tree):
    datas = []
    if tree.return_children() == []:
        return ([tree.return_data()])
    else:
        for x in tree.return_children():
            datas += (allchildren(x))
    return datas

def dup_check(listOfElems):
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True

def inside_check(lists):
    for x in lists:
        if x[0] > 3 or x[0] < 0:
            return False
        if x[1] > 3 or x[1] <0:
            return False
    return True


def generate(x,y,lcv):
    moves = Node([(x,y)])
    for asss in range(0,lcv):
        addlayertwo(moves)
    theory = allchildren(moves)
    version2 = []
    for x in theory:
        if not dup_check(x):
            version2.append(x)

    version3 = []
    for x in version2:
        if inside_check(x):
            version3.append(x)

    return version3

def start(lens,board,xcoord, ycoord):
    lens = lens -1
    possible_words = ((generate(xcoord,ycoord,lens)))
    dicts = {}
    words = []
    for x in possible_words:
        word = ""
        for a in x:
            word += board[a[0]][a[1]]
        dicts.update({word:x})
    DIC = enchant.Dict("en_US")
    realwords = {}
    for x in dicts:
        if DIC.check(x):
            realwords.update({x:dicts[x]})
    return realwords



def creat(board,num):
    alls = start(num, board, 0, 0) | start(num, board, 1, 0)| start(num, board, 2, 0)| start(num, board, 3, 0)
    alls = alls |start(num, board, 0, 1) | start(num, board, 1, 1)| start(num, board, 2, 1)| start(num, board, 3, 1)
    alls = alls |start(num, board, 0, 2) | start(num, board, 1, 2)| start(num, board, 2, 2)| start(num, board, 3, 2)
    alls = alls |start(num, board, 0, 3) | start(num, board, 1, 3)| start(num, board, 2, 3)| start(num, board, 3, 3)
    return alls

def create(board,num):
    num = num + 1
    all = {}
    for x in range(1,num):
        all = all | creat(board,x)
    return all

board = [genrow(),genrow(), genrow(),genrow()]
board = [["o","b","i","g"],["r","e","n","t"],["t","s",'a',"e"],["e","t","m","d"]]
board = [["h","o","e","u"],["o","t","r","o"],["o","e",'r',"a"],["n","t","p","x"]]

#edit the second number for depth.
alls = create(board, 5)

for x in alls:
    print(x, alls[x])
print(len(alls))

try:
    os.remove("words.txt")
except:
    pass

texts = open("words.txt", "w")
texts.write("There are " + str(len(alls)) + " words in this grid" + "\n")
for x in alls:

    texts.write(str(x) + " " + str(alls[x]) + "\n")
texts.close()

