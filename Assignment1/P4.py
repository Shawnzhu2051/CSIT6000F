import csv
import random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

NODE_NUM = 100
# SWAP_RATE = 5  # the number of swap feature in crossover function (1 - 9)
MUTATION_THRESHOLD = 0.1  # the threshold that mutation occurs
MUTATION_RATE = 1  # the number of mutate feature in mutation function (1 - 9)
CROSSOVER_TIME = 60 # the number of crossover occur in one generation
ITERATIVE_TIME = 2500

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
            if self.is_active(test_num) == label_set[test_num]:
                self.fitness_score += 1

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
        ave_fitness_score = ave_fitness_score / NODE_NUM
        return ave_fitness_score


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
        knockout_id = min(self.node_fitness_dict, key=self.node_fitness_dict.get)
        return parent1_id, parent2_id, knockout_id



    def crossover(self, CROSSOVER_TIME):
        for time in range(CROSSOVER_TIME):
            (parent1_id, parent2_id, knockout_id) = self.choose_parent()
            parent_node1 = self.find_node_by_id(id=parent1_id)
            parent_node2 = self.find_node_by_id(id=parent2_id)
            knockout_node = self.find_node_by_id(id=knockout_id)
            if parent_node1 == -1 or parent_node2 == -1 or knockout_node == -1:
                print("node not found !")
            if parent_node1.fitness_score > parent_node2.fitness_score:
                crossover_location = random.randint(5,9)
            else:
                crossover_location = random.randint(1,5)
            for swap_location in range(10):  # single crossover point
                if swap_location <= crossover_location:
                    knockout_node.w_list[swap_location] = parent_node1.w_list[swap_location]
                else:
                    knockout_node.w_list[swap_location] = parent_node2.w_list[swap_location]
            self.mutation(node=knockout_node)

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

if __name__ == '__main__':
    with open('training-set.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            training_set.append(row[:-1])
            label_set.append(int(row[-1]))

    GA = GeneticAlg()
    last_ave_score = 0

    #plt.figure(figsize=(8, 6), dpi=80)
    #plt.ion()
    #plot_x = []
    #plot_y = []

    for num in range(ITERATIVE_TIME):
        ave_score = GA.compute_fitness()

        #plt.cla()
        #plt.title("Converage Graph")
        #plt.grid(True)
        #plot_x.append(num)
        #plot_y.append(ave_score)

        #plt.plot(plot_x, plot_y, "b-", linewidth=2.0, label="average correct rate")

        #plt.xlabel("Generation")
        #plt.xlim(0, ITERATIVE_TIME)
        #plt.ylabel("Average fitness score")
        #plt.ylim(0, 50)
        #plt.pause(0.1)

        print("Epoch " + str(num) + ', average fitness score is ' + str(ave_score))
        GA.crossover(CROSSOVER_TIME=CROSSOVER_TIME)
        if ave_score == 49 and ave_score - last_ave_score < 0.0001:
            break
        else:
            last_ave_score = ave_score

    #plt.ioff()
    #plt.show()

    final_w_list = GA.node_list[0].w_list
    print("The final weight list is " + str(final_w_list))
