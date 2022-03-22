import numpy as np
from fractions import Fraction

fuel = [[0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
       [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
       [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
       [0,0,0,0,0,0],  # s3 is terminal
       [0,0,0,0,0,0],  # s4 is terminal
       [0,0,0,0,0,0]]       
    
    

def convert(fuel,rows,columns,terminal):

    convert = np.matrix(fuel, dtype = float) #, dtype=object)  #Converts list into a numnpy matrix
    
    
    for i in range(terminal):
        count = 0
        for ii in range(columns):
            if fuel[i,ii] != 0:
                count += fuel[i,ii] #counts the total sum of a row as long as it is not a terminal node
        
        for ii in range(columns):
            convert[i,ii] = convert[i,ii] / count #Fraction(convert[i,ii], count)   #divides the denominator on each   
            
    for i in range(terminal , rows): #converts the 0's in to 1's where needed for markov chain
        convert[i,i] = 1
     
            
                           
    
    return convert
    
    
def subtraction(I,Q):
    
    min = 0
    
    if np.size(I, 0) > np.size(Q, 0):
        min = np.size(Q, 0)
    else:
        min = np.size(I,0)             #measures the size of matrix so subtraction can occur
        
    

    subtract = np.matrix((np.subtract(I[:min,:min] , Q[:min,:min])), dtype = float)   #Subtracts the correct size matrix and makes it s float
    
    return(subtract)

    
    
    
def fracConvertToCommonDenom(pBar):
    fracConvert = []
    denom = []
    numer = []
    lcm = 0
    
    for i in range(np.size(pBar,1)):
        num = pBar[0,i]
        fracConvert.append (Fraction(num).limit_denominator()) 
        numer.append(fracConvert[i].numerator)
        denom.append(fracConvert[i].denominator)
        print(str(numer[i])+" : "+str(denom[i]))
 
    lcm = np.lcm.reduce(denom)
    
    converted = []
    for i in range(len(numer)+1):
        if i < len(numer):
            numerator = numer[i]*(lcm/denom[i])  #converts numerator to correct number and leaves it if its correct            
            converted.append(int(numerator))
        else:
            converted.append(lcm)
    
    return(converted)
    
    
    
    
def solution(fuel):

    terminal = 0   
    
    states= np.matrix(fuel)
    rows , columns = states.shape

    for i in range(rows):
        count = 0
        for ii in range(columns):
            if states[i,ii] == 0:
                count += 1
        if count == len(states):
            terminal = i
            break    
    
    states = np.matrix(convert(states,rows,columns, terminal), dtype=float) #converting to Markov chain 
    
    I = states[terminal:,terminal:]
    R = states[:terminal, terminal:]
    Q = states[:terminal, :terminal]
    
    
    InverseF = subtraction(I,Q)    
    F=np.linalg.inv(InverseF) 
    FRBar=np.matmul(F, R)
    
    
    probabilities = fracConvertToCommonDenom(FRBar)
    
    
    return(probabilities)



print(solution(fuel))
    





    
 