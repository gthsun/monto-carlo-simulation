import math

# useful variables
sequenceX = [1000] # the sequence of numbers used to calculate the random numbers, starting with x0 = 1000

# The "random number generator" - 
def rng():
    a = 24693
    c = 3517
    K = 2**17
    i = 0
    x = ((a * sequenceX[-1]) + c) % K
    u = x/K
    sequenceX.append(x)
    return u

# A CDF of the discrete random variable, Y, which represents the outcome of: 1. busy, 2. unavailable, 3. available
def Fy(y):
    if y < 1:
        return 0
    elif 1 <= y < 2:
        return 0.2
    elif 2 <= y < 3:
        return 0.5
    else:
        return 1

# A function that uses the CDF of discrete random variable Y to generate a value for Y, or in other words, an outcome
def Y_value(u):
    Y = [1,2,3]
    for each in Y:
        if(Fy(each) >= u):
            return each
    return 0

# The inverse CDF, used to find the times spent waiting for ringing
def inverse_cdf(cdf):
    return -12*math.log(1-cdf)

# Calculates the percentage of items in a sorted list that are less than or equal to the input num
def upto(num, sorted_list):
    sum = 0
    i = 0
    while i < 1000 and sorted_list[i] <= num:
        sum += 1
        i += 1
    return sum/len(sorted_list)
    

# The simulation!
def monte_carlo_simulation(n):

    W_sample_space = [] #Stores all W values

    # constants for the calling process
    TD = 6   # time spent dialing
    TB = 3   # time spent detecting busy signal
    TR = 25  # time spent waiting for a ring before ending call
    TE = 1   # time spent ending the call

    # calling process
    for number in range(n):
        D = 0 # num dials
        W = 0 # amount of time spent per calling process

        while D < 4:
            Y = Y_value(rng()) # generate discrete random variable based on the random number
            W += TD
            if Y == 1: # BUSY
                W += TB+TE
                D += 1
            elif Y == 3: # AVAILABLE
                #random number generated and inputted into inverse CDF to get 'X' time
                X = inverse_cdf(rng())
                if X <= TR: # AVAILABLE and SUCCESS
                    W += X
                    break
                else: # AVAILABLE but CUSTOMER TOOK TOO LONG
                    W += TR+TE
                    D += 1
            else: # UNAVAILABLE, Y == 2
                W += TR+TE
                D += 1

        W_sample_space.append(round(W,4))

    for each in W_sample_space:
        print(each)
    
    if(n == 1000): # statistics are designed only for 1000 inputs due to project requirements
        print()
        statistics(W_sample_space)

# Statistics of the generated data, meant for 1000 inputs 
def statistics(sample_space):
    print("Statistics:\n-----------------------------")
    sample = sorted(sample_space)
    print(f'{"Min":20} {sample[0]:.4f}')
    print(f'{"Max":20} {sample[-1]:}')
    print(f'{"Mean":20} {sum(sample) / len(sample):.4f}')
    print(f'{"First Quartile":20} {(sample[249]+ sample[250])/2:.4f}')
    print(f'{"Median":20} {(sample[499]+ sample[500])/2:.4f}')
    print(f'{"Third Quartile":20} {(sample[749]+ sample[750])/2:.4f}\n')
    print("Probabilities:\n-----------------------------")
    print(f'{"P[W <= 15]":20} {upto(15, sample):.4f}')
    print(f'{"P[W <= 20]":20} {upto(20, sample):.4f}')
    print(f'{"P[W <= 30]":20} {upto(30, sample):.4f}')
    print(f'{"P[W > 40]":20} {1-upto(40, sample):.4f}')
    print(f'{"P[W > 84 (w5)]":20} {1-upto(84, sample):.4f}')
    print(f'{"P[W > 106 (w6)]":20} {1-upto(106, sample):.4f}')
    print(f'{"P[W > 127 (w7)]":20} {1-upto(127, sample):.4f}')

def main():
    # asks user how many data points they want and runs the simulation
    n = int(input("Please input sample size: "))    
    monte_carlo_simulation(n)

if __name__ == '__main__':
    main()
