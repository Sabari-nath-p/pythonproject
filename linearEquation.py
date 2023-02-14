def minor(matrix, i, j):
    return [[matrix[r][c] for c in range(len(matrix[r])) if c != j]
            for r in range(len(matrix)) if r != i]


def det(matrix):
    if len(matrix) == len(matrix[0]) == 1:
        return matrix[0][0]
    return sum(matrix[0][i] * cofac(matrix, 0, i) for i in range(len(matrix[0])))


cofac = lambda matrix, i, j: (-1) ** ((i + j) % 2) * det(minor(matrix, i, j))

transpose = lambda matrix: [[matrix[r][c] for r in range(len(matrix))] for c in range(len(matrix[0]))]


def adj(matrix):
    return transpose([[cofac(matrix, r, c) for c in range(len(matrix[r]))] for r in range(len(matrix))])


def div_and_store(a, d):
    toPrint = []
    for i in a:
        toPrint.append([])
        for j in i:
            if j % d == 0:
                toPrint[-1].append(f'{j//d}')
            else:
                h = hcf(j, d)
                denominator = d//h
                numerator = j//h
                if denominator > 0:
                    toPrint[-1].append(f'{numerator}/{denominator}')
                else:
                    toPrint[-1].append(f'{-numerator}/{-denominator}')
    return toPrint


hcf = lambda x, y: y if x == 0 else hcf(y % x, x)


def product(A, B):
    if len(A[0]) != len(B):
        return
    Bt = transpose(B)
    return [[sum(a * b for a, b in zip(i, j)) for j in Bt] for i in A]


from tkinter import *
root = Tk()
root.resizable(width=False, height=False)  # not resizable in both directions
root.title('Linear Equation Solver')
my_label = Label(root, text='How many variables?')
my_label.grid(row=0, column=0)
e = Entry(root, width=10, borderwidth=5)


def done():
    global row, n
    try:
        A = []
        S = []
        for record in entries:
            A.append([])
            for i in range(0, len(record)-1):
                entry = record[i].get()
                if entry:
                    A[-1].append(int(entry))
                else:
                    A[-1].append(0)
            entry = record[-1].get()
            S.append([int(entry)])
    except ValueError:
        new_label = Label(root, text='Invalid. Try again!')
        new_label.grid(row=row, columnspan=n * 3, sticky='W')
        new_label.after(1000, lambda: new_label.destroy())
        return
    for record in entries:
        for entry in record:
            entry['state'] = DISABLED
    new_button['state'] = DISABLED
    determinant = det(A)
    if determinant == 0:
        new_label = Label(root, text='No unique solution set!')
        new_label.grid(row=row, columnspan=n * 3, sticky='W')
        return
    adjoin = adj(A)
    solution = div_and_store(product(adjoin, S), determinant)
    for i in range(n):
        new_label = Label(root, text=chr(97+i) + ' = '+solution[i][0])
        new_label.grid(row=row, columnspan=2, sticky='W')
        row += 1


def submit():
    try:
        global n
        n = int(e.get())
    except ValueError:
        label = Label(root, text="You're supposed to enter a number, Try again")
        label.grid(row=1, column=0, columnspan=3)
        label.after(1000, lambda: label.destroy())
        return
    if n < 2:
        label = Label(root, text="At least two variables are required!")
        label.grid(row=1, column=0, columnspan=3)
        label.after(1000, lambda: label.destroy())
        return
    e['state'] = DISABLED
    my_label.grid_forget()
    my_button.grid_forget()
    e.grid_forget()
    global row, entries
    row = 0
    entries = []
    for i in range(n):
        Label(root, text='').grid(row=row, columnspan=3*n+1)
        row += 1
        entries.append([])
        col = 0
        for j in map(chr, range(97, 97+n)):
            entry = Entry(root, width=5, borderwidth=2, justify='right')
            entries[i].append(entry)
            entry.grid(row=row, column=col)
            col += 1
            Label(root, text=j).grid(row=row, column=col, padx=5, sticky='W')
            col += 1
            if col == 3*n-1:
                Label(root, text='=').grid(row=row, column=col)
                col += 1
                entry = Entry(root, width=5, borderwidth=2, justify='right')
                entries[i].append(entry)
                entry.grid(row=row, column=col)
            else:
                Label(root, text='+').grid(row=row, column=col)
            col += 1
        row += 1
    Label(root, text='').grid(row=row)
    row += 1
    txt = 'May leave the blank empty if the coefficient is 0!'
    Label(root, text=txt).grid(row=row, columnspan=3*n-1, sticky='W')
    row += 1
    global new_button
    new_button = Button(root, text='Submit', command=done)
    new_button.grid(row=row, column=3*n)
    row += 1


my_button = Button(root, text='Submit', command=submit)
e.grid(row=0, column=2)
my_button.grid(row=0, column=3)
root.mainloop()