import pandas as pd
import random
import sys

#sys.argv[1]
Stu_file = sys.argv[1]
dept_file = sys.argv[2]
result_file = sys.argv[3]

class student():
    '''class to represent a student's information about exam'''
    def __init__(self,ID,G1,G2,G3,wish):
        self.ID = ID
        self.G1 = G1
        self.G2 = G2
        self.G3 = G3
        self.grade = [None]
        self.current_wish = 0
        self.wish = wish
        self.result = 0
        self.ptr = -1
    def __str__(self):
        '''method to print the ID and result of each student to check algorithm'''
        return f'ID: {self.ID},result: {self.result}'
    def __eq__(self,other,dept):
        '''method to determine if self and other have same score to department'''
        if self.grade[dept] == other.grade[dept]:
            return True
    def __gt__(self,other,dept):
        '''method to determine if self has higher score than other'''
        if self.grade[dept] > other.grade[dept]:
            return True
    def __lt__(self,other,dept):
        '''method to determine if self has lower score than other'''
        if self.grade[dept] < other.grade[dept]:
            return True

def takeSecond(elem):
    '''function to change sorting term'''
    return elem[1]
        
#input the data of student
Student = pd.read_csv(Stu_file,header = None,sep = ' ')
Student.columns = ['ID','g1','g2','g3','1','2','3','4','5','6','7','8','9','10']
Student = Student.set_index('ID')

#input the data of department
Department = pd.read_csv(dept_file,header = None,sep = ' ')
Department.columns = ['dept','g1','g2','g3','number']
Department = Department.set_index('dept')

#change all data frame into student object, and there is a list to save all student object
'''
all list below has a not important element which is None when index is 0
this design is for convenience when indexing
'''
Student_list = [None]
for i in range(1,10001):
    L = [None]
    for j in range(1,11):
        L.append(Student.loc[i,str(j)])
    temp = student(i,Student.loc[i,'g1'],Student.loc[i,'g2'],Student.loc[i,'g3'],L)
    Student_list.append(temp)

#calculate the grade of each student in department
for ID in range(1,10001):
    for i in range(1,11):
        Student_list[ID].grade.append(Student_list[ID].G1*Department.loc[i,'g1']
                                      +Student_list[ID].G2*Department.loc[i,'g2']
                                      +Student_list[ID].G3*Department.loc[i,'g3'])
#Get the current remaining number of student each department need
LN = [None]
for dept in list(Department.loc[:,'number']):
    LN.append(dept)
#make ten List to save the current student who is accepted by department i
L1 = [[0,-9999]]
L2 = [[0,-9999]]
L3 = [[0,-9999]]
L4 = [[0,-9999]]
L5 = [[0,-9999]]
L6 = [[0,-9999]]
L7 = [[0,-9999]]
L8 = [[0,-9999]]
L9 = [[0,-9999]]
L10 = [[0,-9999]]
#build a list (List for current students) as the entry to different list
LCS = [None,L1,L2,L2,L4,L5,L6,L7,L8,L9,L10]
#do the distribution
for ID in range(1,10001):
    Stu = Student_list[ID]
    while Stu.result == 0:
        Stu.current_wish += 1
        #if the wish list has end, then this student has no department
        if Stu.current_wish > 10:
            break
        #deal with the condition of this dept is not full
        if LN[Stu.wish[Stu.current_wish]] > 0:
            CD = Stu.wish[Stu.current_wish]   #current department
            Stu.result = CD
            LN[CD] -= 1
            LCS[CD].append((ID,Stu.grade[CD]))
            LCS[CD][0][0] += 1
            LCS[CD].sort(key = takeSecond)
        #deal with the condition of this dept has been full
        if LN[Stu.wish[Stu.current_wish]] == 0:
            CD = Stu.wish[Stu.current_wish]   #current department
            if Stu.grade[CD] > LCS[CD][1][1]:
                Stu.result = CD
                Drop = LCS[CD][1][0]
                Student_list[Drop].result = 0
                LCS[CD][1] = (ID,Stu.grade[CD])
                LCS[CD].sort(key = takeSecond)
                ID = min(ID,Drop)
            #if two students have same score,then use random to determine who can pass
            elif Stu.grade[CD] == LCS[CD][1][1]:
                key = random.randint(1,2)
                if key == 1:
                    Stu.result = CD
                    Drop = LCS[CD][1][0]
                    Student_list[Drop].result = 0
                    LCS[CD][1] = (ID,Stu.grade[CD])
                    LCS[CD].sort(key = takeSecond)
                    ID = min(ID,Drop)
#combine all result to a string and write it into a txt file
S = ''
for i in range(1,10001):
    if Student_list[i].result == 0:
        Student_list[i].result = -1
    if i < 10:
        S += '0000' + str(Student_list[i].ID) + ' ' + str(Student_list[i].result) + ' '
    elif i >= 10 and i < 100:
        S += '000' + str(Student_list[i].ID) + ' ' + str(Student_list[i].result) + ' '
    elif i >= 100 and i < 1000:
        S += '00' + str(Student_list[i].ID) + ' ' + str(Student_list[i].result) + ' '
    elif i >= 1000 and i < 10000:
        S += '0' + str(Student_list[i].ID) + ' ' + str(Student_list[i].result) + ' '
    else:
        S += str(Student_list[i].ID) + ' ' + str(Student_list[i].result)

file = open(result_file,'w')
file.write(S)
file.close()