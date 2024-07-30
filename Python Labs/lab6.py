class SuperList(list):
    def __init__(self,*args):
        super().__init__(args)
    
    def __iadd__(self, val):
        for index in range(len(self)):
            super().__setitem__(index, self[index]+ val)
        return self
    
    def __setitem__(self, index, val):
        super().__setitem__(index, val * 4)

if __name__ == "__main__":
    l = SuperList(1,2,1,2,2,3,4,5,6,4,4,3,2,2,1,1,1,3)

    print(l)
    l += 16
    print(l)
    l[4] = 20
    print(l)
