import csv
import random

NODE_NUM = 5
SWAP_RATE = 5  # the number of swap feature in crossover function (1 - 9)
MUTATION_THRESHOLD = 0  # the threshold that mutation occurs
MUTATION_RATE = 1  # the number of mutate feature in mutation function (1 - 9)
ITERATIVE_TIME = 10

training_set = []
label_set = []

class Node(object):
    id = 0
    w_list = []  # threshold is w[9]
    fitness_score = 0  # fitness score is the number of correct prediction
    def __init__(self,id):
        temp_w_list = []
        for num in range(10):
            w = 2*random.random()-1
            temp_w_list.append(w)
        self.w_list = temp_w_list
        self.id = id

    def fitness(self):
        self.fitness_score = 0
        for test_num in range(49):
            self.fitness_score += self.is_active(test_num)

    def is_active(self,test_num):
        sum = 0
        for index in range(9):
            sum += float(training_set[test_num][index]) * self.w_list[index]
        if sum > self.w_list[9]:
            return 1
        else:
            return 0

class GeneticAlg(object):
    node_list = []
    node_fitness_dict = {}
    rouletteWheel = []  # used to choose parent based on fitness score
    def __init__(self):
        for index in range(NODE_NUM):
            node = Node(index)
            self.node_list.append(node)

    def compute_fitness(self):
        self.node_fitness_dict.clear()
        ave_fitness_score = 0
        for node in self.node_list:
            node.fitness()
            self.node_fitness_dict[node.id] = node.fitness_score
            ave_fitness_score += node.fitness_score
        print('average fitness score is ' + str(ave_fitness_score/NODE_NUM))


    def choose_parent(self):
        self.rouletteWheel.clear()
        count = 0
        for (node_id, node_score) in self.node_fitness_dict.items():
            share = node_score + 1 # avoid all zero situation
            for time in range(share):
                self.rouletteWheel.append(node_id)
                count += 1
        parent1_id = self.rouletteWheel[random.randint(0, count-1)]
        parent2_id = self.rouletteWheel[random.randint(0, count-1)]
        return parent1_id, parent2_id  # need one more attribute

    def crossover(self):
        (parent1_id, parent2_id) = self.choose_parent()
        parent_node1 = self.find_node_by_id(parent1_id)
        parent_node2 = self.find_node_by_id(parent2_id)
        print(parent_node1.fitness_score)
        print(parent_node2.fitness_score)
        if parent_node1 == -1 or parent_node2 == -1:
            print("node not found !")
        for swap_time in range(SWAP_RATE):
            swap_location = random.randint(0, 9)
            temp = parent_node1.w_list[swap_location]
            parent_node1.w_list[swap_location] = parent_node2.w_list[swap_location]
            parent_node2.w_list[swap_location] = temp
        self.mutation(parent_node1)
        self.mutation(parent_node2)

    def find_node_by_id(self, id):
        for node in self.node_list:
            if node.id == id:
                return node
        return -1

    def mutation(self, node):
        if random.random() > MUTATION_THRESHOLD:
            for mutation_time in range(MUTATION_RATE):
                mutation_location = random.randint(0,9)
                node.w_list[mutation_location] = 2 * random.random() - 1

    def replace(self):  # use new son to replace the last one in fitness score
        pass

if __name__ == '__main__':
    with open('training-set.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            training_set.append(row[:-1])
            label_set.append(int(row[-1]))

    GA = GeneticAlg()
    for num in range(ITERATIVE_TIME):
        GA.compute_fitness()
        GA.crossover()
    #print(GA.rouletteWheel)

    #for (key,value) in GA.node_fitness_dict.items():
    #    print(key)
    #    print(value)