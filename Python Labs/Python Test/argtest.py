
import sys

if __name__ == '__main__':
    for i,v in enumerate(sys.argv):
        print(f"{i} => {v} type {type(v)}")
    
    print(f"Last Check: {sys.argv[3]}")
    sys.exit(-1)
