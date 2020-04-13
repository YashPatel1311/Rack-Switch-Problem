# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 20:51:03 2020

@author: india
"""
import sys

print('Rack Switch Problem')

print('Enter Dimensions of Rack: ')
R_x=70 #int(input('Enter Length of rack: '))
R_y=30 #int(input('Enter Height of rack: '))
R_z=45 #int(input('Enter Depth of rack: '))
R_v=R_x*R_y*R_z
print('Length of rack: ',R_x,'Height of rack: ',R_y,'Width of rack: ',R_z,'Volume of rack: ',R_v)

sys.stdout=open("Output.txt","w")
print('Length of rack: ',R_x,'Height of rack: ',R_y,'Width of rack: ',R_z,'Volume of rack: ',R_v)
print('\nThere are 5 Switches A,B,C,D,E enter dimensions of each')
'''
lt=['A','B','C','D','E']
print(lt)

#Takes input of all switches
switches={}
for x in lt:
    
    temp=list(map(int,(input("Enter Quantity, Weightage, Length, Heigth and Depth of each swithch (space seperated):").split())))
    vol=1
    for i in temp[2:]:
        vol=vol*i
    temp.append(vol)
    switches[x]=temp
'''
switches={'A':[55, 25, 20, 5, 20, 2000], 'B':[10, 30, 30, 10, 15, 4500], 'C':[14, 20, 20, 7, 15, 2100], 'D':[30, 35, 25, 10, 20, 5000], 'E':[80, 15, 10, 8, 10, 800]}

#Calculates sum of volume of all switches
sum_V_S=0
for key,val in switches.items():
    sum_V_S+=val[5]*val[0]
 
#Case 1 if Volume of Rack is Greater than sum of volume of switches no need to arrange
if R_v>sum_V_S:
    print('Volume of Rack is Greater than sum of volume of switches')
    sys.exit(1)

#Seperate Dictionary for working on Quantity
Quantity={}
for key,val in switches.items():
            Quantity.update({key:val[0]})

guess=[]
height=set()

for val in switches.values():
    height.add(val[3])

print(height)

#This part finds the minimum height of all switches so that in recursion program can terminate if remaining height of rack is less than height of any switch left
temp_val=R_y+1
temp_key=''

for key,val in switches.items():
    if val[3]<temp_val:
        temp_val=val[3]
        temp_key=key
        
min_height=temp_val
min_height_key=temp_key
print('\nMinimum Height from all switches is: ',min_height,' of switch: ',min_height_key)


#global_max_height is used as global for max_height which is used as local variable in knapsack function
#max_height represents height of any level according to the max height switch used in that level
global_max_height=0
def knapsack(x,y,z,Quantity):
    global switches
    
    #Iterating through the list of switches to find if they can fit or not

    flag=False
    result=[]
    for key,val in switches.items():

        if (val[2]<=x and val[3]<=y and val[4]<=z and Quantity[key]>0):
            flag=True
            copy_of_Quantity=Quantity.copy()
            copy_of_Quantity[key]-=1

            w_horizontal_left=knapsack(x,y,z-val[4],copy_of_Quantity)
            # print("\nHorizontal left completed")
            # print(w_horizontal_left)
            w_horizontal_right=knapsack(x-val[2],y,val[4],w_horizontal_left['quantity'])
            # print("\nHorizontal Right completed")
            # print(w_horizontal_right)
            w_horizontal=val[1]+w_horizontal_left['score']+w_horizontal_right['score']
            # print("\nHorizontal completed")
            # print(w_horizontal)
            w_vertical_left=knapsack(val[2],y,z-val[4],copy_of_Quantity)
            # print("\nVertical Left completed")
            # print(w_vertical_left)
            w_vertical_right=knapsack(x-val[2],y,z,w_vertical_left['quantity'])
            # print("\nVertical Right completed")
            # print(w_vertical_right)

            w_vertical=val[1]+w_vertical_left['score']+w_vertical_right['score']
            # print("\nvertical completed")
            # print(w_vertical)
            
            if w_horizontal<w_vertical:
                ans= {'quantity':w_vertical_right['quantity'],'score':w_vertical}

            else:
                ans= {'quantity':w_horizontal_right['quantity'],'score':w_horizontal}

            result.append(ans)
            # print("result: ",result)

    if not flag:
        return {'quantity':Quantity,'score':0}
    
    list_max=0
    max_index=0

    for i in range(0,len(result)):
        if result[i]['score']>list_max:
            list_max =result[i]['score']
            max_index=i

    # print("\nmax_index: ",max_index)
    # print(result)
    return result[max_index]

def knapsack_height(R_x,R_y,R_z,Quantity,result={'score':0,'quantity':{}}):
    global min_height,min_height_key,switches,height,guess
    
    print('\n','parameter R_y: ',R_y)
    print('parameter result: ',result)
    print('parameter guess:',guess)


    if Quantity[min_height_key]==0:
        temp_val=R_y+1
        temp_key=''
        for key,val in switches.items():
            if val[3]<temp_val and val[3]>=min_height and Quantity[key]>0:
                temp_val=val[3]
                temp_key=key
                    
        if temp_val==R_y+1:
            temp_val=min_height
            temp_key=min_height_key

        min_height=temp_val
        min_height_key=temp_key

    if R_y<min_height:
        print('Rack full')
        print('Base condition result: ',result)
        guess.append(result)
        print('updated guess :',guess,'\n')
        return 0

    for x in height:
        if x<=R_y:
            max_height=x
            print('max_height: ',max_height)
            print('R_y: ',R_y)
            copy_quantity=Quantity.copy()
            copy_result=result.copy()
            print('copy_result:', copy_result)
            ans=knapsack(R_x,max_height,R_z,copy_quantity)
            copy_result['quantity']=ans['quantity']
            copy_result['score']+=ans['score']
            print('updated copy_result:', copy_result)
            knapsack_height(R_x,R_y-max_height,R_z,ans['quantity'],copy_result)


knapsack_height(R_x,R_y,R_z,Quantity)
print(guess)