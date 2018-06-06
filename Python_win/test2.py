# -*-coding:Latin-1 -*


def print_fibonacci(nb_val):
    a,b,c =1,1,0
    while (c < nb_val):
        print(b)
        a,b,c = b,a+b,c+1
    
if __name__ == "__main__":
    print_fibonacci(5)