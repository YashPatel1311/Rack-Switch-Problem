# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 20:51:03 2020

@author: india
"""
import sys

print('Rack Switch Problem')

print('Enter Dimensions of Rack: ')
R_x=50 #int(input('Enter Length of rack: '))
R_y=30 #int(input('Enter Height of rack: '))
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

switches={'A':[5, 25, 20, 10, 20, 2000], 'B':[7, 30, 30, 10, 15, 4500], 'C':[3, 20, 20, 7, 15, 2100], 'D':[5, 35, 25, 10, 20, 5000], 'E':[20, 15, 10, 5, 8, 800]}

Quantity={'A':1,'B':1,'C':1,'D':1,'E':1}
min_height=5
min_height_key='E'


global_max_height=0
def knapsack(x,y,z,max_height,Quantity):
    global switches,global_max_height

    # if x<=10:
    #     return {'quantity':Quantity,'score':0}

    # if z<=8:
    #     return {'quantity':Quantity,'score':0}
    

    
    # print("\nQuantity : ",Quantity)
    # print(" X: ",x," Y: ",y," Z: ",z," max_height: ",max_height)
    #Iterating through the list of switches to find if they can fit or not

    flag=False
    result=[]
    for key,val in switches.items():

        if (val[2]<=x and val[3]<=y and val[4]<=z and Quantity[key]>0):
            flag=True
            copy_of_Quantity=Quantity.copy()
            copy_of_Quantity[key]-=1
            if val[3]>max_height:
                max_height=val[3]

            w_horizontal_left=knapsack(x,y,z-val[4],max_height,copy_of_Quantity)
            # print("\nHorizontal left completed")
            # print(w_horizontal_left)
            w_horizontal_right=knapsack(x-val[2],y,val[4],max_height,w_horizontal_left['quantity'])
            # print("\nHorizontal Right completed")
            # print(w_horizontal_right)
            w_horizontal=val[1]+w_horizontal_left['score']+w_horizontal_right['score']
            # print("\nHorizontal completed")
            # print(w_horizontal)
            w_vertical_left=knapsack(val[2],y,z-val[4],max_height,copy_of_Quantity)
            # print("\nVertical Left completed")
            # print(w_vertical_left)
            w_vertical_right=knapsack(x-val[2],y,z,max_height,w_vertical_left['quantity'])
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
    global_max_height=max_height
    return result[max_index]

def knapsack_height(R_x,R_y,R_z,Quantity):
    global min_height,min_height_key,switches

    final_score=0
    while(R_y>=min_height):

        if Quantity[min_height_key]==0:
            temp_val=R_y+1
            temp_key=-1
            for key,val in switches.items():
                if val[3]<temp_val and val[3]>min_height:
                    temp_val=val[3]
                    temp_key=key


            min_height=temp_val
            print('updated min_heigth: ',min_height)
            min_height_key=temp_key
            print('updated min_heigth_key: ',min_height_key)

        ans=knapsack(R_x,R_y,R_z,0,Quantity)
        R_y=R_y-global_max_height
        # print('R_y: ',R_y)
        final_score+=ans['score']
        Quantity=ans['quantity']

    return {'quantity':Quantity, 'score':final_score}


print(knapsack_height(R_x,R_y,R_z,Quantity))