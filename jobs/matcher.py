import random

def random_pair(foo):
    '''
    A function to randomly pair people in a list
    :param foo: the list of people
    :param result: resulting pairs
    '''
    random.shuffle(foo)
    length = len(foo)//2
    return list(zip(foo[:length], foo[length:]))

list_people = ['a', 'b', 'c', 'd', 'e', 'f']
print("the list of pairs are:----")
print(random_pair(list_people))
