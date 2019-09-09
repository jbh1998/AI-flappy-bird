import neural_network
import aigame_config as config
import copy
import random


class Genome(object):  # 描述个体的类
    # 每一个个体基因当中所携带的基因数据（神经网络的数据）
    def __init__(self, network_data, score):
        """

        :param network_data:这个个体的神经网络数据模型
        :param score: 这个个体获得的分数
        """
        self.data = network_data
        self.score = score


class Generation(object):
    def __init__(self):
        self.genomes = []

    def add_genome(self, genome):
        """
        将个体按照分数从大到小顺序插入到一代个体的列表中
        :param genome: 个体
        :return:
        """
        for temp in self.genomes:
            if genome.score > temp.score:
                index = self.genomes.index(temp)
                self.genomes.insert(index, genome)
                return
        self.genomes.append(genome)

    def create_next_generation(self):
        """
        创建一个由精英、杂种、子代组成的后代列表
        :return:
        """
        network_data_list = []
        # 1.选取精英个体直接遗传:把精英个体的数据模型放入列表中
        for i in range(round(config.population * config.elite)):
            network_data_list.append(self.genomes[i].data)
        # 2.创建一部分随机个体：创建一些随机个体的数据模型放入列表中
        for i in range(round(config.population * config.new_bron)):
            network = neural_network.NeuralNetwork(config.network[0], config.network[1], config.network[2])
            network_data_list.append(network.getNetwork())
        # 3.选取2个个体进行繁衍：将前一半后后一半的杂交后放入下一组数据中
        while True:
            if len(network_data_list) == config.population:
                break
            father = self.genomes[random.randint(0, round(config.population / 2) - 1)]
            mother = self.genomes[random.randint(round(config.population / 2), config.population - 1)]
            child = self.breed(father, mother)
            network_data_list.append(child.data)
        return network_data_list

    def breed(self, father, mother):
        """
        杂交生成子代
        :param father:父系数据模型
        :param mother: 母系数据结构
        :return: 子系数据结构
        """
        child = copy.deepcopy(father)
        # 交叉
        for i in range(len(child.data['weights'])):
            if random.random() < 0.5:
                child.data['weights'][i] = mother.data['weights'][i]
        # 变异
        for i in range(len(child.data['weights'])):
            if random.random() < config.variation:
                child.data['weights'][i] = neural_network.random_weight()
        return child


class GenerationManager(object):
    """
    世代管理者：用来管理个体列表
    """
    def __init__(self):
        self.generations = []

    def create_generation(self):
        """
        创建世代
        :return:世代中所有个体的神经网络数据模型
        """
        if len(self.generations) == 0:
            network_data_list = self.__first_generation()
        else:
            network_data_list = self.__next_generation()
        self.generations.append(Generation())
        if len(self.generations) > 2:
            del self.generations[:-2]
        return network_data_list

    def __first_generation(self):
        """
        创建第一个世代:随机创建population个神经模型，将他们添加到列表中
        :return:世代中所有个体的神经网络数据
        """
        network_data_list = []
        for i in range(config.population):
            network = neural_network.NeuralNetwork(config.network[0], config.network[1], config.network[2])
            network_data_list.append(network.getNetwork())
        return network_data_list

    def __next_generation(self):
        """
        创建下一个世代
        :return: 世代中所有个体的神经网络数据
        """
        network_data_list = self.generations[-1].create_next_generation()
        return network_data_list

    def add_genome(self, genome):
        self.generations[-1].add_genome(genome)


if __name__ == '__main__':
    manager = GenerationManager()
    manager.create_generation()
