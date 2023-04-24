import math



def f_prime(f, epsilon, D, R, A,B):
    if f <= 0:
        return float('inf')
    else:
        return (1+((2*B)/((math.log(10))*(A+B*f))))

def newtons_method(epsilon, D, R,A,B, tolerance=1e-120, max_iterations=100):
    f = 0.01 # Initial guess
    for i in range(max_iterations):
        f_old = f
        fp = f_prime(f, epsilon, D, R,A,B)
        if fp == math.inf:
            f = "inf"
            return f
        else:
            print("f = {:.6f}, f_prime = {:.6f}".format(f, fp))
            f = f - ((f+2*math.log10(A+B*f))/fp)
            if abs(f - f_old) < tolerance:
                return 1/(f**2)
            
        
    raise ValueError("Failed to converge after {} iterations".format(max_iterations))



def solvef(D,R):
    epsilon = 0.015
    
    rel_e = epsilon/D
    A = rel_e/3.7
    B = 2.51/R
    print("l")
    f = newtons_method(epsilon, D, R,A,B)
    print(f)
    if f == "inf":
        print(f)
    else:
        print("The solution is f = {:.10f}".format(f))
    return f

f = solvef(40,40000000)
print(f)