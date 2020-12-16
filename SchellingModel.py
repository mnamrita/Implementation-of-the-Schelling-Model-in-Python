import numpy as np 
import random
import matplotlib.pyplot as plt


def get_neighbours(p, exclude_p=True, shape=(50,50)):

    ndim = len(p)

    # generate an (m, ndims) array containing all combinations of 0, 1, 2
    offset_idx = np.indices((3,) * ndim).reshape(ndim, -1).T

    # use these to index into np.array([-1, 0, 1]) to get offsets
    offsets = np.r_[-1, 0, 1].take(offset_idx)

    # optional: exclude offsets of 0, 0, ..., 0 (i.e. p itself)
    if exclude_p:
        offsets = offsets[np.any(offsets, 1)]

    neighbours = p + offsets    # apply offsets to p

    # optional: exclude out-of-bounds indices
    if shape is not None:
        valid = np.all((neighbours < np.array(shape)) & (neighbours >= 0), axis=1)
        neighbours = neighbours[valid]
    

    x,y=zip(*neighbours)

    return x,y

def get_neighbours2(p, exclude_p=True, shape=(50,50)):

    ndim = len(p)

    # generate an (m, ndims) array containing all combinations of 0, 1, 2
    offset_idx = np.indices((3,) * ndim).reshape(ndim, -1).T

    # use these to index into np.array([-1, 0, 1]) to get offsets
    offsets = np.r_[-1, 0, 1].take(offset_idx)

    # optional: exclude offsets of 0, 0, ..., 0 (i.e. p itself)
    if exclude_p:
        offsets = offsets[np.any(offsets, 1)]

    neighbours = p + offsets    # apply offsets to p

    # optional: exclude out-of-bounds indices
    if shape is not None:
        valid = np.all((neighbours < np.array(shape)) & (neighbours >= 0), axis=1)
        neighbours = neighbours[valid]
    

    

    return neighbours


def get_list_of_empty_cells(x,y):
    global grid
    flag=0
    cell=(x,y)
    x_around,y_around=get_neighbours(cell)
    list_of_empty_cells=[]
    for index in range(len(x_around)):
        if(grid[x_around[index],y_around[index]]==0):
            flag=1
            empty_cell=(x_around[index],y_around[index])
            list_of_empty_cells.append(empty_cell)
        else:
            continue
    return flag,list_of_empty_cells


def check_satisfaction(x,y,agent):
    global grid
    s=0
    cell=(x,y)
    x_neighbours,y_neighbours=get_neighbours(cell)
    number_of_neighbours=len(x_neighbours)
    list_of_neighbors=[]
    for index in range(number_of_neighbours):
                list_of_neighbors.append(grid[x_neighbours[index],y_neighbours[index]])
    count=list_of_neighbors.count(agent)
    if(count>2):
        s=1
    return s


def relocate(index,value,x_empty,y_empty):
    global grid
    
    
    grid[index[0],index[1]]=0
    grid[x_empty,y_empty]=value






# Breadth First Search
def bfs(start,agent):
    global grid
    # keep track of all visited nodes
    explored = []
    # keep track of nodes to be checked
    queue = [start]
 
    # keep looping until there are nodes still to be checked
    while queue:
        # pop shallowest node (first node) from queue
        node = queue.pop(0)

        if node not in explored:
            # add node to list of checked nodes
            explored.append(node)
            
            if(check_satisfaction(node[0],node[1],agent)==1) and grid[node[0],node[1]] == 0:
                print("this should never happen... run")
                break

            else:
                    f,empty_cells=get_list_of_empty_cells(node[0],node[1])
                    if(f==1):
                        x_empty,y_empty=zip(*empty_cells)
                        for i in range(len(x_empty)):
                            s=check_satisfaction(x_empty[i],y_empty[i],agent)
                            if(s==1):
                                    # print("/ ",end="")
                                    node=(x_empty[i],y_empty[i])
                                    return s,node
                            # relocate(index,value,x_empty[i],y_empty[i])
                    
                    neighbours = get_neighbours2(node)
                    neighbours=neighbours.tolist()
 
            # add neighbours of node to queue
                    for neighbour in neighbours:
                        queue.append(neighbour)
    
    
    if(s==1):
        
        return s,node
    else:
        
        return s,start
 
 

def plot(A):
    pointsx=[]
    pointso=[]
    for index, value in np.ndenumerate(A):
        if(value==1):
            pointsx.append(index)
        elif(value==-1):
            pointso.append(index)

    #print(pointsx)
    xx,xy=zip(*pointsx)
    ox,oy=zip(*pointso)
    xx=list(xx)
    ox=list(ox)
    for i in range(len(xy)):
        xx[i]=49-xx[i]

    for i in range(len(oy)):
        ox[i]=49-ox[i]





   
    return xx,xy,ox,oy


def main():
    #Create x-y locations
    global grid
    shape=(50,50)
    data=np.indices((50,50)).swapaxes(0,2).swapaxes(0,1)
    data=data.tolist()
    A=[]
    for element in data:
        for x in element:
            A.append(x)
    #Initialization of grid     
    #Taking 1000 unique random x-y coordinates
    b=random.sample(A,1000)
    #Splitting them into x and 0
    x=b[0:500]
    o=b[500:1000]

    #Zipping for plotting
    xx, xy = zip(*x)
    ox,oy=zip(*o)
    grid=np.zeros((50,50)).astype("int16")
    for x,y in zip(xx,xy):
        grid[49-y,x]=1
    for x,y in zip(ox,oy):
        grid[49-y,x]=-1
    
    
    
    plt.scatter(xx,xy,c='b', marker="x", label='x agents')
    plt.scatter(ox,oy, c='r', marker="o", label='y agents')
    plt.xlim(-0.2,50.2)
    plt.ylim(-0.2,50.2)
    plt.title("Original Positions")
    plt.savefig("Original Positions", dpi=1000)
    plt.show()
    
    list_of_agents=[1,-1]

    #Schelling Model
    for i in range(5):
        for index, _ in np.ndenumerate(grid):
            value=grid[index[0],index[1]]
            current_satisfaction=check_satisfaction(index[0],index[1],value)
            if current_satisfaction == 0:
                grid[index[0],index[1]]=0 #To avoid counting the cell itself while checking satisfaction in other locations
                if value in list_of_agents:
                        start=(index[0],index[1])
                        s,pos=bfs(start,value)
                        if (s==1):
                            
                            relocate(index,value,pos[0],pos[1])
                            
                        else:
                            grid[index[0],index[1]]=value
                            continue


        xx,xy,ox,oy=plot(grid)
        
        
        
        plt.scatter(xy,xx,c='b', marker="x", label='x agents')
        plt.scatter(oy,ox, c='r', marker="o", label='y agents')
        plt.xlim(-0.2,50.2)
        plt.ylim(-0.2,50.2)
        if(i+1<5):
        		title="Positions in Iteration "+str(i+1)
        else:
        	title="Final Positions"
        plt.title(title)
        plt.savefig(title, dpi=1000)
        plt.show()
        



    red_flag=0
    for index,value in np.ndenumerate(grid):
	    if value in list_of_agents:
	    	self_satisfaction=check_satisfaction(index[0],index[1],value)
	    	if(self_satisfaction==0):
	    		red_flag=1
	    		break
	    	else:
	    		continue
    if(red_flag==1):
    	print("UNSATISFIED!!!")


if __name__== "__main__":
  main()

           

                






