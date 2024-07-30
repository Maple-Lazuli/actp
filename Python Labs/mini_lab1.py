class BackRoll(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg
    def __str__(self):
        return f"Error: {self.msg}"
    def __repr__(self):
        return f"Error: {self.msg}"

class Vehicle:

    miles_traveled = 0

    def __init__(self, top_speed, wheels, color):
        self.top_speed = top_speed
        self.wheels = wheels
        self.color = color

    def __str__(self):
        return f'Top Speed:{self.top_speed}, Wheels:{self.wheels}, Color:{self.color}, Miles: {self.miles_traveled}'
    
    def drive(self, hours):
        if hours < 0:
            raise BackRoll("Cannot Drive Negative Hours")
        self.miles_traveled += self.top_speed * hours

    def honk(self):
        print("Honk\a")

class Motorcycle(Vehicle):
    def __init__(self, top_speed, color):
        super().__init__(top_speed, 2, color)
    
    def honk(self):
        print("Beep\a")

if __name__ == "__main__":
    v = Vehicle(top_speed=60, wheels=3, color='Red')
    print(v)
    v.drive(8)
    v.honk()
    print(v)

    m = Motorcycle(top_speed=160, color='Black')
    m.drive(18)
    print(m)
    m.honk()
    try :
        m.drive(-10)
    except BackRoll as e:
        print(e)
