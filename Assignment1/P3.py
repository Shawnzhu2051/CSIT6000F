import random

class TLU(object):
    w1 = 0
    w2 = 0
    w3 = 0
    x1 = 0
    x2 = 0
    x3 = 1
    threshold = 0
    d = 0
    def __init__(self):
        pass

    def input_train(self,x1,x2):
        self.x1 = x1
        self.x2 = x2

    def active(self):
        vector = self.x1 * self.w1 + self.x2 * self.w2 + self.x3 * self.w3
        if(vector - self.threshold >= 0):
            return 1
        else:
            return 0

    def error_correction(self,old_output):
        if(self.x1|self.x2):
            self.d = 1
        else:
            self.d = 0
        self.w1 = self.w1 + (self.d - old_output) * self.x1
        self.w2 = self.w2 + (self.d - old_output) * self.x2
        self.w3 = self.w3 + (self.d - old_output) * self.x3

    def print_weight(self):
        print("weight is " + str(self.w1) + " " + str(self.w2) + " " + str(self.w3))

tlu = TLU()

input = [0,0,1,0,0,1,1,1]
for time in range(20):
    print("Round " + str(time//4) + ", epoch " + str(time%4))
    #tlu.print_weight()
    input1 = input[2*(time)%8]
    input2 = input[2*(time)%8+1]
    tlu.input_train(input1, input2)
    print("input is " + str(input1) + " " + str(input2) + " 1")
    output = tlu.active()
    print("output is " + str(output))
    #if(input1 | input2 == tlu.active()):
    #    print("Right!")
    #else:
    #    print("Wrong!")
    tlu.error_correction(output)
    tlu.print_weight()
    print("-------------------------------")
# we want
# TLU(1,1).output = 1
# TLU(1,0).output = 1
# TLU(0,1).output = 1
# TLU(0,0).output = 0
