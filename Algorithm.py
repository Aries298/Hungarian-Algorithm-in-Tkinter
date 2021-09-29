import tkinter as tk
import numpy as np
from tkinter import messagebox
from math import ceil
def min_zero_row(zero_mat, mark_zero):

    # Find the row
    min_row = [99999, -1]

    for row_num in range(zero_mat.shape[0]):
        if np.sum(zero_mat[row_num] == True) > 0 and min_row[0] > np.sum(zero_mat[row_num] == True):
            min_row = [np.sum(zero_mat[row_num] == True), row_num]

    # Marked the specific row and column as False
    zero_index = np.where(zero_mat[min_row[1]] == True)[0][0]
    mark_zero.append((min_row[1], zero_index))
    zero_mat[min_row[1], :] = False
    zero_mat[:, zero_index] = False


def mark_matrix(mat):

    # Transform the matrix to boolean matrix(0 = True, others = False)
    cur_mat = mat
    zero_bool_mat = (cur_mat == 0)
    zero_bool_mat_copy = zero_bool_mat.copy()

    # Recording possible answer positions by marked_zero
    marked_zero = []
    while (True in zero_bool_mat_copy):
        min_zero_row(zero_bool_mat_copy, marked_zero)

    # Recording the row and column positions seperately.
    marked_zero_row = []
    marked_zero_col = []
    for i in range(len(marked_zero)):
        marked_zero_row.append(marked_zero[i][0])
        marked_zero_col.append(marked_zero[i][1])

    # Step 2-2-1
    non_marked_row = list(set(range(cur_mat.shape[0])) - set(marked_zero_row))

    marked_cols = []
    check_switch = True
    while check_switch:
        check_switch = False
        for i in range(len(non_marked_row)):
            row_array = zero_bool_mat[non_marked_row[i], :]
            for j in range(row_array.shape[0]):
                # Step 2-2-2
                if row_array[j] == True and j not in marked_cols:
                    # Step 2-2-3
                    marked_cols.append(j)
                    check_switch = True

        for row_num, col_num in marked_zero:
            # Step 2-2-4
            if row_num not in non_marked_row and col_num in marked_cols:
                # Step 2-2-5
                non_marked_row.append(row_num)
                check_switch = True
    # Step 2-2-6
    marked_rows = list(set(range(mat.shape[0])) - set(non_marked_row))

    return (marked_zero, marked_rows, marked_cols)


def adjust_matrix(mat, cover_rows, cover_cols):
    cur_mat = mat
    non_zero_element = []

    # Step 4-1
    for row in range(len(cur_mat)):
        if row not in cover_rows:
            for i in range(len(cur_mat[row])):
                if i not in cover_cols:
                    non_zero_element.append(cur_mat[row][i])
    min_num = min(non_zero_element)

    # Step 4-2
    for row in range(len(cur_mat)):
        if row not in cover_rows:
            for i in range(len(cur_mat[row])):
                if i not in cover_cols:
                    cur_mat[row, i] = cur_mat[row, i] - min_num
    # Step 4-3
    for row in range(len(cover_rows)):
        for col in range(len(cover_cols)):
            cur_mat[cover_rows[row], cover_cols[col]] = cur_mat[cover_rows[row], cover_cols[col]] + min_num
    return cur_mat


def hungarian_algorithm(mat):
    dim = mat.shape[0]
    cur_mat = mat

    # Step 1 - Every column and every row subtract its internal minimum
    for row_num in range(mat.shape[0]):
        cur_mat[row_num] = cur_mat[row_num] - np.min(cur_mat[row_num])

    for col_num in range(mat.shape[1]):
        cur_mat[:, col_num] = cur_mat[:, col_num] - np.min(cur_mat[:, col_num])
    zero_count = 0
    while zero_count < dim:
        # Step 2 & 3
        ans_pos, marked_rows, marked_cols = mark_matrix(cur_mat)
        zero_count = len(marked_rows) + len(marked_cols)

        if zero_count < dim:
            cur_mat = adjust_matrix(cur_mat, marked_rows, marked_cols)

    return ans_pos


def ans_calculation(mat, pos):
    total = 0
    ans_mat = np.zeros((mat.shape[0], mat.shape[1]))
    for i in range(len(pos)):
        total += mat[pos[i][0], pos[i][1]]
        ans_mat[pos[i][0], pos[i][1]] = mat[pos[i][0], pos[i][1]]
    return total, ans_mat

def ParseInt(str):
    try:
        if(int(str)<0):
            return None
        else:
            return int(str)
    except:
        return None


class ChoiceWindow:
    def __init__(self,root):
        self.root = root
        self.window = tk.Toplevel()
        self.rowsize = 0
        self.columnsize = 0

        def invokeWindow():
            self.window.destroy()
            Window(self.root,self.rowsize,self.columnsize)


        self.window.title('Hungarian Algorithm')
        tb = tk.Label(master=self.window,text='Enter rectangle size (rows and columns)')

        l1 = tk.Label(master=self.window, text='Rows')
        e1 = tk.Entry(self.window)

        l2 = tk.Label(master=self.window, text='Columns')
        e2 = tk.Entry(self.window)

        def checkVals():
            try:
                if (ParseInt(e1.get()) is not None and ParseInt(e2.get()) is not None):
                    if (ParseInt(e1.get()) == 0 or ParseInt(e2.get()) == 0):
                        raise ValueError("Rowsize or Columnsize can't be equal to 0.")
                    self.rowsize = e1.get()
                    self.columnsize = e2.get()
                    invokeWindow()
            except:
                pass


        btn = tk.Button(master=self.window,width=10,text='Confirm',command=checkVals)

        tb.grid(row=0,column=0,columnspan=2)

        l1.grid(row=1,column=0)
        e1.grid(row=1, column=1)

        l2.grid(row=2,column=0)
        e2.grid(row=2, column=1)

        btn.grid(row=3,column=0,columnspan=2)

class Window:
    def __init__(self,root,rowsize,columnsize):
        self.root = root
        self.window = tk.Toplevel()
        self.rowsize = int(rowsize)
        self.columnsize = int(columnsize)
        self.window.title('Hungarian algorithm')
        self.window.geometry("600x600")
        self.entries = np.empty((self.rowsize,self.columnsize), dtype=tk.Entry)
        self.matrix = np.empty((self.rowsize, self.columnsize), dtype=int)


        for i in range(self.rowsize):
            for j in range(self.columnsize):
                self.entries[i][j] = tk.Entry(self.window,width=3,font=("",16))
                self.entries[i][j].grid(row=i,column=j,padx=1,pady=1)


        def findMin():
            GoodVals = True
            try:
                for i in range(self.rowsize):
                    for j in range(self.columnsize):
                        if (ParseInt(self.entries[i][j].get()) is None):
                            GoodVals = False
            except:
                GoodVals = False
            if GoodVals:

                # Copying values to the matrix
                for i in range(self.rowsize):
                    for j in range(self.columnsize):
                        self.matrix[i][j] = int(self.entries[i][j].get())


                cost_matrix = (self.matrix).copy()
                ans_pos = hungarian_algorithm(cost_matrix.copy())  # Get the element position.
                ans, ans_mat = ans_calculation(cost_matrix,
                                               ans_pos)  # Get the minimum or maximum value and corresponding matrix.

                # Show the result
                AnswerWindow(self.root, ans_mat)
            else:
                messagebox.showerror("Error", "Wrong input!")

        def findMax():
            GoodVals = True
            try:
                for i in range(self.rowsize):
                    for j in range(self.columnsize):
                        if (ParseInt(self.entries[i][j].get()) is None):
                            GoodVals = False
            except:
                GoodVals = False
            if GoodVals:

                # Copying values to the matrix
                for i in range(self.rowsize):
                    for j in range(self.columnsize):
                        self.matrix[i][j] = int(self.entries[i][j].get())


                profit_matrix = (self.matrix).copy()
                max_value = np.max(profit_matrix)
                cost_matrix = max_value - profit_matrix
                ans_pos = hungarian_algorithm(cost_matrix.copy())  # Get the element position.
                ans, ans_mat = ans_calculation(profit_matrix,
                                               ans_pos)  # Get the minimum or maximum value and corresponding matrix.
                # Show the result
                AnswerWindow(self.root,ans_mat)
            else:
                messagebox.showerror("Error", "Wrong input!")

        btn1 = tk.Button(self.window, width=12, text='Find Minimum', command=findMin)
        btn1.grid(row=self.rowsize + 1, column=0, columnspan=self.columnsize,  sticky = "SW")
        btn2 = tk.Button(self.window, width=12, text='Find Maximum', command=findMax)
        btn2.grid(row=self.rowsize + 1, column=1, columnspan=self.columnsize,  sticky = "SE")

        class AnswerWindow:
            def __init__(self, root, matrix):
                self.root = root
                self.window = tk.Toplevel()
                self.matrix = matrix
                self.window.title('Answer')
                self.window.geometry("600x600")

                self.rowsize = int(self.matrix.shape[0])
                self.columnsize = int(self.matrix.shape[1])
                self.entries = np.empty((self.rowsize, self.columnsize), dtype=tk.Entry)

                for i in range(self.rowsize):
                    for j in range(self.columnsize):
                        #Color answer entries
                        if (self.matrix[i][j] != 0):
                            self.entries[i][j] = tk.Entry(self.window, width=3, font=("", 16),bg = 'green')
                        else:
                            self.entries[i][j] = tk.Entry(self.window, width=3, font=("", 16))

                        self.entries[i][j].insert(0,int(self.matrix[i][j]))
                        self.entries[i][j].grid(row=i, column=j, padx=1, pady=1)

        if __name__ == '__main__':
            main()

        
