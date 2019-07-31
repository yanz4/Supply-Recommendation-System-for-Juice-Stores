import numpy as np
import json
import time
import os.path
import mysql.connector

# Connect to mysql database
mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               passwd="password",
                               database="test",
                               auth_plugin='mysql_native_password'
                               ##added auth_plugin='mysql_native_password'
                               )

cur = mydb.cursor()

# Query for average profit of each product group by city size the store is in

cur.execute('''
    SELECT
    AVG(GreenPower),
    AVG(LemonDrop),
    AVG(InnerPeach),
    AVG(SquareRoot),
    AVG(ForceField),
    AVG(PinkPom),
    AVG(PumpkinCordial),
    AVG(LeanGreen),
    AVG(StrawberryMintJulep),
    AVG(MangoTango),
    AVG(BerryAPeeling),
    AVG(HangUnder),
    AVG(ArthritisSoother),
    AVG(SplendidSpinach)
    FROM Stores
    GROUP BY citysize
    ''')
# Parse and output result into a string p for Linear Optimization
avg_cost = cur.fetchall()

cost = list()

for row in avg_cost:
    line = list()
    for i in range(len(row)):
        line.append(float(row[i]))
    cost.append(line)

cost_L = cost[0]
cost_M = cost[1]
cost_S = cost[2]

all = cost_L + cost_M + cost_S
str_all = [str(i) + ',' for i in all]
p = ''
for i in str_all:
    p += i

p = p[:-1]

cur.close()
# Start Linear Optimization, set timer

t_threthold = 20
start = time.time()


def create_new_matrix(var, cons):
    tab = np.zeros((cons + 1, var + cons + 2))
    return tab


def go_next_round2(table):
    m = min(table[:-1, -1])
    if m >= 0:
        return False
    else:
        return True


def go_next_round(table):
    m = min(table[len(table[:, 0]) - 1, :-1])
    if m >= 0:
        return False
    else:
        return True


def find_negative_two(table):
    lc = len(table[0, :])
    # search every row (excluding last row) in final column for min value
    m = min(table[:-1, lc - 1])
    if m <= 0:
        # n = row index of m location
        n = np.where(table[:-1, lc - 1] == m)[0][0]
    else:
        n = None
    return n


# returns column index of negative element in bottom row
def find_next_negative(table):
    lr = len(table[:, 0])
    m = min(table[lr - 1, :-1])
    if m <= 0:
        # n = row index for m
        n = np.where(table[lr - 1, :-1] == m)[0][0]
    else:
        n = None
    return n


# locates pivot element in tableu to remove the negative element from the furthest right column.
def location_of_piv2(table):
    total = []
    # r = row index of negative entry
    r = find_negative_two(table)
    # finds all elements in row, r, excluding final column
    row = table[r, :-1]
    # finds minimum value in row (excluding the last column)
    m = min(row)
    # c = column index for minimum entry in row
    c = np.where(row == m)[0][0]
    # all elements in column
    col = table[:-1, c]
    # need to go through this column to find smallest positive ratio
    for i, b in zip(col, table[:-1, -1]):
        # i cannot equal 0 and b/i must be positive.
        if i ** 2 > 0 and b / i > 0:
            total.append(b / i)
        else:
            # placeholder for elements that did not satisfy the above requirements. Otherwise, our index number would be faulty.
            total.append(10000)
    index = total.index(min(total))
    return [index, c]


# similar process, returns a specific array element to be pivoted on.
def location_of_piv(table):
    if go_next_round(table):
        total = []
        n = find_next_negative(table)
        for i, b in zip(table[:-1, n], table[:-1, -1]):
            if b / i > 0 and i ** 2 > 0:
                total.append(b / i)
            else:
                total.append(10000)
        index = total.index(min(total))
        return [index, n]


'''''' '''''' '''''' '''''' '''''' '''''
        ''' '''''' '''''' '''''' '''''' '''''' ''


# String -> coefficient matrix for constraints
def convert(eq):
    eq = eq.split(',')
    if '>=' in eq:
        del eq[eq.index('>=')]
        eq = [float(i) * -1 for i in eq]
        return eq
    if '<=' in eq:
        del eq[eq.index('<=')]
        eq = [float(i) for i in eq]
        return eq


def convert_min(t):
    t[-1, :-2] = [-a for a in t[-1, :-2]]
    t[-1, -1] = -t[-1, -1]
    return t


# Variable generation to denote the optimal solution.
def new_var(table):
    num = len(table[0, :]) - len(table[:, 0]) - 1
    variables = []
    for i in range(num):
        variables.append('x' + str(i + 1))
    return variables


# tableau pivot
def pivot(row, col, table):
    t = np.zeros((len(table[:, 0]), len(table[0, :])))
    pr = table[row, :]
    if table[row, col] == 0:
        print('No pivot is allowed on this element')
    else:
        e = 1 / table[row, col]
        r = pr * e
        for i in range(len(table[:, col])):
            if list(table[i, :]) == list(pr):
                continue
            else:
                t[i, :] = list(table[i, :] - r * table[i, col])
        t[row, :] = list(r)
        return t


# check whether another constraint is supplementable?
def new_cons(table):
    asa = []
    for i in range(len(table[:, 0])):
        total = 0
        for j in table[i, :]:
            total += j ** 2
        if total == 0:
            asa.append(0)
    if len(asa) > 1:
        return True
    else:
        return False


# adds a constraint to the matrix
def constrain(table, eq):
    if new_cons(table) == True:
        counter = 0
        while counter < len(table[:, 0]):
            total = 0
            for i in table[counter, :]:
                total += float(i ** 2)
            if total == 0:
                row = table[counter, :]
                break
            counter += 1

        converted_eq = convert(eq)
        i = 0

        while i < len(converted_eq) - 1:
            row[i] = converted_eq[i]
            i += 1

        row[-1] = converted_eq[-1]

        # add slack variable
        row[len(table[0, :]) - len(table[:, 0]) - 1 + counter] = 1
    else:
        print('No more constraint is addable.')


def add_obj(table):
    empty = []
    for i in range(len(table[:, 0])):
        total = 0
        for j in table[i, :]:
            total += j ** 2
        if total == 0:
            empty.append(0)

    if len(empty) - 1 == 0:
        return True
    else:
        return False


def obj(table, eq):
    if add_obj(table):
        eq = [float(i) for i in eq.split(',')]
        row = table[len(table[:, 0]) - 1, :]
        i = 0
        while i < len(eq) - 1:
            row[i] = eq[i] * -1
            i += 1
        row[-2] = 1
        row[-1] = eq[-1]
    else:
        print('Finish adding constraints first!')


def maxz(table, output='summary'):
    while go_next_round2(table) == True:
        end = time.time()
        if end - start > t_threthold:
            return ('Optimal Solutions Do Not Exist!')
        table = pivot(location_of_piv2(table)[0], location_of_piv2(table)[1], table)
    while go_next_round(table) == True:
        end = time.time()
        if end - start > t_threthold:
            return ('Optimal Solutions Do Not Exist!')
        table = pivot(location_of_piv(table)[0], location_of_piv(table)[1], table)

    var = len(table[0, :]) - len(table[:, 0]) - 1

    values = {}
    for i in range(var):
        if float(sum(table[:, i])) == float(max(table[:, i])):
            loc = np.where(table[:, i] == max(table[:, i]))[0][0]
            values[new_var(table)[i]] = table[loc, -1]
        else:
            values[new_var(table)[i]] = 0
    values['max'] = table[-1, -1]
    if output == 'table':
        return table
    else:
        return values


def mass_code_fk():
    print('14 stores test:')
    a = '1'
    for i in range(13):
        a += ',1'
    for i in range(28):
        a += ',0'

    b = '0'
    for i in range(13):
        b += ',0'
    for i in range(14):
        b += ',1'
    for i in range(14):
        b += ',0'

    c = '0'
    for i in range(27):
        c += ',0'
    for i in range(14):
        c += ',1'

    m = create_new_matrix(42, 42 + 10 + 14)

    constrain(m, a + ',<=,120')
    constrain(m, b + ',<=,120')
    constrain(m, c + ',<=,60')

    constrain(
        m,
        '1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,>=,0'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,>=,0'
    )
    ''''''

    constrain(
        m,
        '206,0,0,0,0,0,0,200,0,213,0,0,0,0,206,0,0,0,0,0,0,200,0,213,0,0,0,0,206,0,0,0,0,0,0,200,0,213,0,0,0,0,<=,900'
    )
    constrain(
        m,
        '0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,<=,20'
    )
    constrain(
        m,
        '0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,<=,30'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,<=,10'
    )
    constrain(
        m,
        '0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,12'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,>=,12'
    )
    constrain(
        m,
        '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,>=,6'
    )
    #   old constraints
    #    constrain(m, '0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,<=,0.001')
    #    constrain(m, '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,<=,0.001')
    #    constrain(m, '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,<=,0.001')
    #    constrain(m, '0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,<=,0.001')
    #    constrain(m, '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,<=,0.001')
    #    constrain(m, '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,<=,0.001')
    '''
    '''
    return m


def main(input1, input2):
    print(input1, input2)
    m = mass_code_fk()
    if input == '':
        input1 = 50

    max1 = input1
    max2 = input1
    max3 = input1
    max4 = input1
    max5 = input1
    max6 = input1
    max7 = input1
    max8 = input1
    max9 = input1
    max10 = input1
    max11 = input1
    max12 = input1
    max13 = input1
    max14 = input1

    content = input2.split(',')
    if content == ['']:
        max1 = 50
        max2 = 50
        max3 = 50
        max4 = 50
        max5 = 50
        max6 = 50
        max7 = 50
        max8 = 50
        max9 = 50
        max10 = 50
        max11 = 50
        max12 = 50
        max13 = 50
        max14 = 50
    else:
        if 'P1' in content:
            index = content.index('P1')
            max1 = content[index + 1]

        if 'P2' in content:
            index = content.index('P2')
            max2 = content[index + 1]

        if 'P3' in content:
            index = content.index('P3')
            max3 = content[index + 1]

        if 'P4' in content:
            index = content.index('P4')
            max4 = content[index + 1]

        if 'P5' in content:
            index = content.index('P5')
            max5 = content[index + 1]

        if 'P6' in content:
            index = content.index('P6')
            max6 = content[index + 1]

        if 'P7' in content:
            index = content.index('P7')
            max7 = content[index + 1]

        if 'P8' in content:
            index = content.index('P8')
            max8 = content[index + 1]

        if 'P9' in content:
            index = content.index('P9')
            max9 = content[index + 1]

        if 'P10' in content:
            index = content.index('P10')
            max10 = content[index + 1]

        if 'P11' in content:
            index = content.index('P11')
            max11 = content[index + 1]

        if 'P12' in content:
            index = content.index('P12')
            max12 = content[index + 1]

        if 'P13' in content:
            index = content.index('P13')
            max13 = content[index + 1]

        if 'P14' in content:
            index = content.index('P14')
            max14 = content[index + 1]

    print(content)

    newmax = [
        max1, max2, max3, max4, max5, max6, max7, max8, max9, max10, max11,
        max12, max13, max14
    ]
    newmax = list(map(lambda x: float(x) if float(x) > 0 else 0.001, newmax))

    for i in range(14):
        con = list('0,' * 42)
        con[2 * i] = '1'
        con[2 * i + 28] = '1'
        con[2 * i + 56] = '1'
        con = ''.join(con) + '<=,' + str(newmax[i])
        constrain(m, con)

    # p is the string of numbers acquired from mysql queries, entered here as constraint

    obj(m, p)

    result = maxz(m)

    for key in result.keys():
        result[key] = round(float(result[key]), 2)

    print(json.dumps(result, indent=1))

    output_fk = ''

    def str_fk(res_fk):
        return res_fk

    for keys, val in result.items():
        if (keys == 'x1'):
            output_fk += str_fk("Green Power" + "_" + "L" + ': ' + str(val) +
                                '\n')
        if (keys == 'x2'):
            output_fk += str_fk("Lemon Drop" + "_" + "L" + ': ' + str(val) +
                                '\n')
        if (keys == 'x3'):
            output_fk += str_fk("Inner Peach" + "_" + "L" + ': ' + str(val) +
                                '\n')
        if (keys == 'x4'):
            output_fk += str_fk("Square Root" + "_" + "L" + ': ' + str(val) +
                                '\n')
        if (keys == 'x5'):
            output_fk += str_fk("Force Field" + "_" + "L" + ': ' + str(val) +
                                '\n')
        if (keys == 'x6'):
            output_fk += str_fk("Pink Pom" + "_" + "L" + ': ' + str(val) +
                                '\n')
        if (keys == 'x7'):
            output_fk += str_fk("Pumpkin Cordial" + "_" + "L" + ': ' +
                                str(val) + '\n')
        if (keys == 'x8'):
            output_fk += str_fk("Lean Green" + "_" + "L" + ': ' + str(val) +
                                '\n')
        if (keys == 'x9'):
            output_fk += str_fk("Strawberry Mint Julep" + "_" + "L" + ': ' +
                                str(val) + '\n')
        if (keys == 'x10'):
            output_fk += str_fk("Mango Tango" + "_" + "L" + ': ' + str(val) +
                                '\n')
        if (keys == 'x11'):
            output_fk += str_fk("Berry A-Peeling" + "_" + "L" + ': ' +
                                str(val) + '\n')
        if (keys == 'x12'):
            output_fk += str_fk("Hang Under" + "_" + "L" + ': ' + str(val) +
                                '\n')
        if (keys == 'x13'):
            output_fk += str_fk("Arthritis Soother" + "_" + "L" + ': ' +
                                str(val) + '\n')
        if (keys == 'x14'):
            output_fk += str_fk("Splendid Spinach" + "_" + "L" + ': ' +
                                str(val) + '\n')
        if (keys == 'x15'):
            output_fk += str_fk("Green Power" + "_" + "M" + ': ' + str(val) +
                                '\n')
        if (keys == 'x16'):
            output_fk += str_fk("Lemon Drop" + "_" + "M" + ': ' + str(val) +
                                '\n')
        if (keys == 'x17'):
            output_fk += str_fk("Inner Peach" + "_" + "M" + ': ' + str(val) +
                                '\n')
        if (keys == 'x18'):
            output_fk += str_fk("Square Root" + "_" + "M" + ': ' + str(val) +
                                '\n')
        if (keys == 'x19'):
            output_fk += str_fk("Force Field" + "_" + "M" + ': ' + str(val) +
                                '\n')
        if (keys == 'x20'):
            output_fk += str_fk("Pink Pom" + "_" + "M" + ': ' + str(val) +
                                '\n')
        if (keys == 'x21'):
            output_fk += str_fk("Pumpkin Cordial" + "_" + "M" + ': ' +
                                str(val) + '\n')
        if (keys == 'x22'):
            output_fk += str_fk("Lean Green" + "_" + "M" + ': ' + str(val) +
                                '\n')
        if (keys == 'x23'):
            output_fk += str_fk("Strawberry Mint Julep" + "_" + "M" + ': ' +
                                str(val) + '\n')
        if (keys == 'x24'):
            output_fk += str_fk("Mango Tango" + "_" + "M" + ': ' + str(val) +
                                '\n')
        if (keys == 'x25'):
            output_fk += str_fk("Berry A-Peeling" + "_" + "M" + ': ' +
                                str(val) + '\n')
        if (keys == 'x26'):
            output_fk += str_fk("Hang Under" + "_" + "M" + ': ' + str(val) +
                                '\n')
        if (keys == 'x27'):
            output_fk += str_fk("Arthritis Soother" + "_" + "M" + ': ' +
                                str(val) + '\n')
        if (keys == 'x28'):
            output_fk += str_fk("Splendid Spinach" + "_" + "M" + ': ' +
                                str(val) + '\n')
        if (keys == 'x29'):
            output_fk += str_fk("Green Power" + "_" + "S" + ': ' + str(val) +
                                '\n')
        if (keys == 'x30'):
            output_fk += str_fk("Lemon Drop" + "_" + "S" + ': ' + str(val) +
                                '\n')
        if (keys == 'x31'):
            output_fk += str_fk("Inner Peach" + "_" + "S" + ': ' + str(val) +
                                '\n')
        if (keys == 'x32'):
            output_fk += str_fk("Square Root" + "_" + "S" + ': ' + str(val) +
                                '\n')
        if (keys == 'x33'):
            output_fk += str_fk("Force Field" + "_" + "S" + ': ' + str(val) +
                                '\n')
        if (keys == 'x34'):
            output_fk += str_fk("Pink Pom" + "_" + "S" + ': ' + str(val) +
                                '\n')
        if (keys == 'x35'):
            output_fk += str_fk("Pumpkin Cordial" + "_" + "S" + ': ' +
                                str(val) + '\n')
        if (keys == 'x36'):
            output_fk += str_fk("Lean Green" + "_" + "S" + ': ' + str(val) +
                                '\n')
        if (keys == 'x37'):
            output_fk += str_fk("Strawberry Mint Julep" + "_" + "S" + ': ' +
                                str(val) + '\n')
        if (keys == 'x38'):
            output_fk += str_fk("Mango Tango" + "_" + "S" + ': ' + str(val) +
                                '\n')
        if (keys == 'x39'):
            output_fk += str_fk("Berry A-Peeling" + "_" + "S" + ': ' +
                                str(val) + '\n')
        if (keys == 'x40'):
            output_fk += str_fk("Hang Under" + "_" + "S" + ': ' + str(val) +
                                '\n')
        if (keys == 'x41'):
            output_fk += str_fk("Arthritis Soother" + "_" + "S" + ': ' +
                                str(val) + '\n')
        if (keys == 'x42'):
            output_fk += str_fk("Splendid Spinach" + "_" + "S" + ': ' +
                                str(val) + '\n')
        # add_fk(keys + ': ' + str(val) + '\n')
        if (keys == 'max'):
            output_fk += str_fk("Maximum Profits = $" + str(val) + '(k)' +
                                '\n')

    return output_fk


if __name__ == "__main__":
    output = main('', '')
    print(output)
