# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 20:51:03 2020

@author: india
"""
import sys

print('Rack Switch Problem')

print('Enter Dimensions of Rack: ')
R_x=40 #int(input('Enter Length of rack: '))
R_y=10 #int(input('Enter Height of rack: '))
R_z=30 #int(input('Enter Depth of rack: '))
R_v=120000000 #R_x*R_y*R_z

sys.stdout=open("Output.txt","w")

print('\nThere are 5 Switches A,B,C,D,E enter dimensions of each')

'''
lt=['A','B','C','D','E']

switches={}
for x in lt:
    
    temp=list(map(int,(input("Enter Quantity(0), Weightage(1), Length(2), Heigth(3) and Depth(4) of each swithch (space seperated):").split())))
    vol=1
    for i in temp[2:]:
        vol=vol*i
    temp.append(vol)
    switches[x]=temp
'''

switches={'A':[5, 25, 20, 5, 20, 2000], 'B':[7, 30, 30, 10, 15, 4500], 'C':[3, 20, 20, 7, 15, 2100], 'D':[5, 35, 25, 10, 20, 5000], 'E':[20, 15, 10, 10, 8, 800]}

Quantity={'A':5,'B':7,'C':3,'D':5,'E':1}

global_max_height=0
def knapsack(x,z,max_height=0,Quantity={}):
    global R_x,R_z
    global switches

    # if x<=10:
    #     return {'quantity':Quantity,'score':0}

    # if z<=8:
    #     return {'quantity':Quantity,'score':0}
    

    
    print("\nQuantity : ",Quantity)
    print(" X: ",x," Z: ",z," max_height: ",max_height)
    #Iterating through the list of switches to find if they can fit or not

    flag=False
    result=[]
    for key,val in switches.items():
        # 9898772134

        if (val[2]<=x and val[4]<=z and Quantity[key]>0):
            flag=True
            copy_of_Quantity=Quantity.copy()
            copy_of_Quantity[key]-=1
            if val[3]>max_height:
                max_height=val[3]

            w_horizontal_left=knapsack(x,z-val[4],max_height=max_height,Quantity=copy_of_Quantity)
            print("\nHorizontal left completed")
            print(w_horizontal_left)
            w_horizontal_right=knapsack(x-val[2],val[4],max_height=max_height,Quantity=w_horizontal_left['quantity'])
            print("\nHorizontal Right completed")
            print(w_horizontal_right)
            w_horizontal=val[1]+w_horizontal_left['score']+w_horizontal_right['score']
            print("\nHorizontal completed")
            print(w_horizontal)
            w_vertical_left=knapsack(val[2],z-val[4],max_height=max_height,Quantity=copy_of_Quantity)
            print("\nVertical Left completed")
            print(w_vertical_left)
            w_vertical_right=knapsack(x-val[2],z,max_height=max_height,Quantity=w_vertical_left['quantity'])
            print("\nVertical Right completed")
            print(w_vertical_right)

            w_vertical=val[1]+w_vertical_left['score']+w_vertical_right['score']
            print("\nvertical completed")
            print(w_vertical)
            
            if w_horizontal<w_vertical:
                ans= {'quantity':w_vertical_right['quantity'],'score':w_vertical}

            else:
                ans= {'quantity':w_horizontal_right['quantity'],'score':w_horizontal}

            result.append(ans)
            print("result: ",result)

    if not flag:
        return {'quantity':Quantity,'score':0}
    
    list_max=0
    max_index=0

    for i in range(0,len(result)):
        if result[i]['score']>list_max:
            list_max =result[i]['score']
            max_index=i

    print("\nmax_index: ",max_index)
    print(result)
    global_max_height=max_height
    return result[max_index]

# def knapsack_height(R_x,R_y,R_z,Quantity=Quantity):
#     while(R_y>5):
#         ans=knapsack(R_x,R_z,max_height=0,Quantity=Quantity)


   
print(knapsack(R_x,R_z,max_height=0,Quantity=Quantity))