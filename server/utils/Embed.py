import codecs
import numpy as np
import copy
import time
import random
from sklearn.preprocessing import LabelEncoder


def norm_l1(h, r, t):
    return np.sum(np.fabs(h + r - t))
def norm_l2(h, r, t):
    return np.sum(np.square(h + r - t))

class TransE:
    def __init__(self, username,entity, relation, triple_list, embedding_dim=50, lr=0.01, margin=1.0, norm=1):
        self.username = username
        self.entities = entity
        self.relations = relation
        self.triples = triple_list
        self.dimension = embedding_dim
        self.learning_rate = lr
        self.margin = margin
        self.norm = norm
        self.loss = 0.0

    def data_initialise(self):
        entityVectorList = {}
        relationVectorList = {}
        for entity in self.entities:
            entity_vector = np.random.uniform(-6.0 / np.sqrt(self.dimension), 6.0 / np.sqrt(self.dimension),self.dimension)
            entityVectorList[entity] = entity_vector

        for relation in self.relations:
            relation_vector = np.random.uniform(-6.0 / np.sqrt(self.dimension), 6.0 / np.sqrt(self.dimension),self.dimension)
            relation_vector = self.normalization(relation_vector)
            relationVectorList[relation] = relation_vector

        self.entities = entityVectorList
        self.relations = relationVectorList

    def normalization(self, vector):
        return vector / np.linalg.norm(vector)

    def training_run(self, epochs=10, nbatches=100, out_file_title = ''):

        batch_size = int(len(self.triples) / nbatches)
        # print("batch size: ", batch_size)
        for epoch in range(epochs):
            start = time.time()
            self.loss = 0.0
            # Normalise the embedding of the entities to 1
            for entity in self.entities.keys():
                self.entities[entity] = self.normalization(self.entities[entity]);

            for batch in range(nbatches):
                batch_samples = random.sample(self.triples, batch_size)

                Tbatch = []
                for sample in batch_samples:
                    corrupted_sample = copy.deepcopy(sample)
                    pr = np.random.random(1)[0]
                    if pr > 0.5:
                        # change the head entity
                        corrupted_sample[0] = random.sample(self.entities.keys(), 1)[0]
                        while corrupted_sample[0] == sample[0]:
                            corrupted_sample[0] = random.sample(self.entities.keys(), 1)[0]
                    else:
                        # change the tail entity
                        corrupted_sample[2] = random.sample(self.entities.keys(), 1)[0]
                        while corrupted_sample[2] == sample[2]:
                            corrupted_sample[2] = random.sample(self.entities.keys(), 1)[0]

                    if (sample, corrupted_sample) not in Tbatch:
                        Tbatch.append((sample, corrupted_sample))

                self.update_triple_embedding(Tbatch)
            end = time.time()
            # print("epoch: ", epoch, "cost time: %s" % (round((end - start), 3)))
            # print("running loss: ", self.loss)

        returnE = []
        returnR = []

        # with codecs.open(out_file_title +"TransE_entity_" + str(self.dimension) + "dim_batch" + str(batch_size), "w") as f1:
        for e in self.entities.keys():
                # f1.write(e + "\t")
                # f1.write(str(list(self.entities[e])))
                # f1.write("\n")
            returnE.append(list(self.entities[e]))
        # with codecs.open(out_file_title +"TransE_relation_" + str(self.dimension) + "dim_batch" + str(batch_size), "w") as f2:
        for r in self.relations.keys():
                # f2.write(r + "\t")
                # f2.write(str(list(self.relations[r])))
                # f2.write("\n")
            returnR.append(list(self.relations[r]))

        return returnE,returnR

    def update_triple_embedding(self, Tbatch):
        # deepcopy 可以保证，即使list嵌套list也能让各层的地址不同， 即这里copy_entity 和
        # entitles中所有的elements都不同
        copy_entity = copy.deepcopy(self.entities)
        copy_relation = copy.deepcopy(self.relations)

        for correct_sample, corrupted_sample in Tbatch:

            correct_copy_head = copy_entity[correct_sample[0]]
            correct_copy_tail = copy_entity[correct_sample[2]]
            relation_copy = copy_relation[correct_sample[1]]

            corrupted_copy_head = copy_entity[corrupted_sample[0]]
            corrupted_copy_tail = copy_entity[corrupted_sample[2]]

            correct_head = self.entities[correct_sample[0]]
            correct_tail = self.entities[correct_sample[2]]
            relation = self.relations[correct_sample[1]]

            corrupted_head = self.entities[corrupted_sample[0]]
            corrupted_tail = self.entities[corrupted_sample[2]]

            # calculate the distance of the triples
            if self.norm == 1:
                correct_distance = norm_l1(correct_head, relation, correct_tail)
                corrupted_distance = norm_l1(corrupted_head, relation, corrupted_tail)

            else:
                correct_distance = norm_l2(correct_head, relation, correct_tail)
                corrupted_distance = norm_l2(corrupted_head, relation, corrupted_tail)

            loss = self.margin + correct_distance - corrupted_distance
            if loss > 0:
                self.loss += loss

                correct_gradient = 2 * (correct_head + relation - correct_tail)
                corrupted_gradient = 2 * (corrupted_head + relation - corrupted_tail)

                if self.norm == 1:
                    for i in range(len(correct_gradient)):
                        if correct_gradient[i] > 0:
                            correct_gradient[i] = 1
                        else:
                            correct_gradient[i] = -1

                        if corrupted_gradient[i] > 0:
                            corrupted_gradient[i] = 1
                        else:
                            corrupted_gradient[i] = -1

                correct_copy_head -= self.learning_rate * correct_gradient
                relation_copy -= self.learning_rate * correct_gradient
                correct_copy_tail -= -1 * self.learning_rate * correct_gradient

                relation_copy -= -1 * self.learning_rate * corrupted_gradient
                if correct_sample[0] == corrupted_sample[0]:
                    # if corrupted_triples replaces the tail entity, the head entity's embedding need to be updated twice
                    correct_copy_head -= -1 * self.learning_rate * corrupted_gradient
                    corrupted_copy_tail -= self.learning_rate * corrupted_gradient
                elif correct_sample[2] == corrupted_sample[2]:
                    # if corrupted_triples replaces the head entity, the tail entity's embedding need to be updated twice
                    corrupted_copy_head -= -1 * self.learning_rate * corrupted_gradient
                    correct_copy_tail -= self.learning_rate * corrupted_gradient

                # normalising these new embedding vector, instead of normalising all the embedding together
                copy_entity[correct_sample[0]] = self.normalization(correct_copy_head)
                copy_entity[correct_sample[2]] = self.normalization(correct_copy_tail)
                if correct_sample[0] == corrupted_sample[0]:
                    # if corrupted_triples replace the tail entity, update the tail entity's embedding
                    copy_entity[corrupted_sample[2]] = self.normalization(corrupted_copy_tail)
                elif correct_sample[2] == corrupted_sample[2]:
                    # if corrupted_triples replace the head entity, update the head entity's embedding
                    copy_entity[corrupted_sample[0]] = self.normalization(corrupted_copy_head)
                # the paper mention that the relation's embedding don't need to be normalised
                copy_relation[correct_sample[1]] = relation_copy
                # copy_relation[correct_sample[1]] = self.normalization(relation_copy)

        self.entities = copy_entity
        self.relations = copy_relation

relation_tph = {}
relation_hpt = {}
class TransH:
    def __init__(self, entity_set, relation_set, triple_list, embedding_dim=50, lr=0.01, margin=1.0, norm=1, C=1.0, epsilon = 1e-5):
        self.entities = entity_set
        self.relations = relation_set
        self.triples = triple_list
        self.dimension = embedding_dim
        self.learning_rate = lr
        self.margin = margin
        self.norm = norm
        self.loss = 0.0
        self.norm_relations = {}
        self.hyper_relations = {}
        self.C = C
        self.epsilon = epsilon

    def data_initialise(self):
        entityVectorList = {}
        relationNormVectorList = {}
        relationHyperVectorList = {}
        for entity in self.entities:
            entity_vector = np.random.uniform(-6.0 / np.sqrt(self.dimension), 6.0 / np.sqrt(self.dimension),self.dimension)
            entityVectorList[entity] = entity_vector

        for relation in self.relations:
            relation_norm_vector = np.random.uniform(-6.0 / np.sqrt(self.dimension), 6.0 / np.sqrt(self.dimension),self.dimension)
            relation_hyper_vector = np.random.uniform(-6.0 / np.sqrt(self.dimension), 6.0 / np.sqrt(self.dimension),self.dimension)
            relation_norm_vector = self.normalization(relation_norm_vector)
            relation_hyper_vector = self.normalization(relation_hyper_vector)
            relationNormVectorList[relation] = relation_norm_vector
            relationHyperVectorList[relation] = relation_hyper_vector

        self.entities = entityVectorList
        self.norm_relations = relationNormVectorList
        self.hyper_relations = relationHyperVectorList


    def training_run(self, epochs=10, nbatches=400):

        batch_size = int(len(self.triples) / nbatches)
        # print("batch size: ", batch_size)
        for epoch in range(epochs):
            start = time.time()
            self.loss = 0.0
            # Normalise the embedding of the entities to 1
            for entity in self.entities:
                self.entities[entity] = self.normalization(self.entities[entity]);

            for batch in range(nbatches):
                batch_samples = random.sample(self.triples, batch_size)

                Tbatch = []
                for sample in batch_samples:
                    corrupted_sample = copy.deepcopy(sample)
                    pr = np.random.random(1)[0]
                    p = relation_tph[corrupted_sample[2]] / (relation_tph[corrupted_sample[2]] + relation_hpt[corrupted_sample[2]])
                    '''
                    这里关于p的说明 tph 表示每一个头结对应的平均尾节点数 hpt 表示每一个尾节点对应的平均头结点数
                    当tph > hpt 时 更倾向于替换头 反之则跟倾向于替换尾实体

                    举例说明 
                    在一个知识图谱中，一共有10个实体 和n个关系，如果其中一个关系使两个头实体对应五个尾实体，
                    那么这些头实体的平均 tph为2.5，而这些尾实体的平均 hpt只有0.4，
                    则此时我们更倾向于替换头实体，
                    因为替换头实体才会有更高概率获得正假三元组，如果替换头实体，获得正假三元组的概率为 8/9 而替换尾实体获得正假三元组的概率只有 5/9
                    '''
                    if pr < p:
                        # change the head entity
                        corrupted_sample[0] = random.sample(self.entities.keys(), 1)[0]
                        while corrupted_sample[0] == sample[0]:
                            corrupted_sample[0] = random.sample(self.entities.keys(), 1)[0]
                    else:
                        # change the tail entity
                        corrupted_sample[1] = random.sample(self.entities.keys(), 1)[0]
                        while corrupted_sample[1] == sample[1]:
                            corrupted_sample[1] = random.sample(self.entities.keys(), 1)[0]

                    if (sample, corrupted_sample) not in Tbatch:
                        Tbatch.append((sample, corrupted_sample))

                self.update_triple_embedding(Tbatch)
            end = time.time()
            # print("epoch: ", epoch, "cost time: %s" % (round((end - start), 3)))
            # print("running loss: ", self.loss)


        returnE = []
        returnR = []

        # with codecs.open("H_entity_" + str(self.dimension) + "dim_batch" + str(batch_size), "w") as f1:

        for e in self.entities:
                # f1.write(e + "\t")
                # f1.write(str(list(self.entities[e])))
                # f1.write("\n")
            returnE.append(list(self.entities[e]))

        # with codecs.open("H_relation_norm_" + str(self.dimension) + "dim_batch" + str(batch_size), "w") as f2:
            # for r in self.norm_relations:
                # f2.write(r + "\t")
                # f2.write(str(list(self.norm_relations[r])))
                # f2.write("\n")

        # with codecs.open("H_relation_hyper_" + str(self.dimension) + "dim_batch" + str(batch_size), "w") as f3:
        for r in self.hyper_relations:
                # f3.write(r + "\t")
                # f3.write(str(list(self.hyper_relations[r])))
                # f3.write("\n")
            returnR.append(list(self.hyper_relations[r]))

        return returnE,returnR


    def normalization(self, vector):
        return vector / np.linalg.norm(vector)

    def norm_l2(self, h, r_norm, r_hyper, t):
        return np.sum(np.square(    h - np.dot(r_norm, h) * r_norm  + r_hyper - t + np.dot(r_norm, t) * r_norm     ))


    # 模长约束对结果收敛有影响，但是正交约束影响很小所以模长约束保留，正交约束可以不加
    def scale_entity(self, h, t, h_c, t_c):
        return np.linalg.norm(h)**2 - 1 +np.linalg.norm(t)**2 - 1+np.linalg.norm(h_c)**2 - 1 + np.linalg.norm(t_c)**2 - 1

    def orthogonality(self, norm, hyper):
        return np.dot(norm, hyper)**2/np.linalg.norm(hyper)**2 - self.epsilon**2

    def update_triple_embedding(self, Tbatch):
        copy_entity = copy.deepcopy(self.entities)
        copy_norm_relation = copy.deepcopy(self.norm_relations)
        copy_hyper_relation = copy.deepcopy(self.hyper_relations)

        for correct_sample, corrupted_sample in Tbatch:

            correct_copy_head = copy_entity[correct_sample[0]]
            correct_copy_tail = copy_entity[correct_sample[1]]
            relation_norm_copy = copy_norm_relation[correct_sample[2]]
            relation_hyper_copy = copy_hyper_relation[correct_sample[2]]

            corrupted_copy_head = copy_entity[corrupted_sample[0]]
            corrupted_copy_tail = copy_entity[corrupted_sample[1]]

            correct_head = self.entities[correct_sample[0]]
            correct_tail = self.entities[correct_sample[1]]
            relation_norm = self.norm_relations[correct_sample[2]]
            relation_hyper = self.hyper_relations[correct_sample[2]]

            corrupted_head = self.entities[corrupted_sample[0]]
            corrupted_tail = self.entities[corrupted_sample[1]]

            # calculate the distance of the triples
            correct_distance = self.norm_l2(correct_head, relation_norm, relation_hyper, correct_tail)
            corrupted_distance = self.norm_l2(corrupted_head, relation_norm, relation_hyper, corrupted_tail)


            loss = self.margin + correct_distance - corrupted_distance
            loss1 = self.scale_entity(correct_head, correct_tail, corrupted_head, corrupted_tail)
            # loss2 = self.orthogonality(relation_norm, relation_hyper)


            if loss > 0:


                self.loss += loss
                i = np.ones(self.dimension)
                correct_gradient = 2 * (correct_head - np.dot(relation_norm, correct_head) * relation_norm  +
                                        relation_hyper - correct_tail +
                                        np.dot(relation_norm, correct_tail) *
                                        relation_norm) * (i - relation_norm**2)
                corrupted_gradient = 2 * (corrupted_head - np.dot(relation_norm, corrupted_head) * relation_norm  +
                                        relation_hyper - corrupted_tail +
                                        np.dot(relation_norm, corrupted_tail) *
                                        relation_norm) * (i - relation_norm**2)
                hyper_gradient= 2 * (correct_head - np.dot(relation_norm, correct_head) * relation_norm  +
                                       - correct_tail + np.dot(relation_norm, correct_tail)
                                     * relation_norm)- 2 * (corrupted_head - np.dot(relation_norm, corrupted_head) * relation_norm  +
                                     - corrupted_tail +
                                        np.dot(relation_norm, corrupted_tail) *
                                        relation_norm)
                norm_gradient = 2 * (correct_head - np.dot(relation_norm, correct_head) * relation_norm  +
                                        relation_hyper - correct_tail +
                                        np.dot(relation_norm, correct_tail) *
                                        relation_norm) * (correct_tail - correct_head) * 2 * relation_norm - 2 * (corrupted_head - np.dot(relation_norm, corrupted_head) * relation_norm  +
                                        relation_hyper - corrupted_tail +
                                        np.dot(relation_norm, corrupted_tail) *
                                        relation_norm) * (corrupted_tail - corrupted_head) * 2 * relation_norm


                correct_copy_head -= self.learning_rate * correct_gradient
                relation_norm_copy -= self.learning_rate * norm_gradient
                relation_hyper_copy -=  self.learning_rate * hyper_gradient
                correct_copy_tail -= -1 * self.learning_rate * correct_gradient

                if correct_sample[0] == corrupted_sample[0]:
                    # if corrupted_triples replaces the tail entity, the head entity's embedding need to be updated twice
                    correct_copy_head -= -1 * self.learning_rate * corrupted_gradient
                    corrupted_copy_tail -= self.learning_rate * corrupted_gradient
                elif correct_sample[1] == corrupted_sample[1]:
                    # if corrupted_triples replaces the head entity, the tail entity's embedding need to be updated twice
                    corrupted_copy_head -= -1 * self.learning_rate * corrupted_gradient
                    correct_copy_tail -= self.learning_rate * corrupted_gradient

                # normalising these new embedding vector, instead of normalising all the embedding together
                copy_entity[correct_sample[0]] = self.normalization(correct_copy_head)
                copy_entity[correct_sample[1]] = self.normalization(correct_copy_tail)
                if correct_sample[0] == corrupted_sample[0]:
                    # if corrupted_triples replace the tail entity, update the tail entity's embedding
                    copy_entity[corrupted_sample[1]] = self.normalization(corrupted_copy_tail)
                elif correct_sample[1] == corrupted_sample[1]:
                    # if corrupted_triples replace the head entity, update the head entity's embedding
                    copy_entity[corrupted_sample[0]] = self.normalization(corrupted_copy_head)
                # the paper mention that the relation's embedding don't need to be normalised
                copy_norm_relation[correct_sample[2]] = self.normalization(relation_norm_copy)
                copy_hyper_relation[correct_sample[2]] = relation_hyper_copy
                # copy_relation[correct_sample[2]] = self.normalization(relation_copy)


        self.entities = copy_entity
        self.norm_relations = copy_norm_relation
        self.hyper_relations = copy_hyper_relation


def CalTrans(username,entities,edges,triplets,dim,kind):
    


    E_label = list(LabelEncoder().fit(entities).classes_)    
    E_int = LabelEncoder().fit(E_label).transform(E_label)
    
    R_label = list(LabelEncoder().fit(edges).classes_)    
    R_int = LabelEncoder().fit(R_label).transform(R_label)

    entity_set = list()
    relation_set  = list()
    for i in range(len(E_int)):
        entity_set.append(str(E_int[i]))
    for i in range(len(R_int)):
        relation_set.append(str(R_int[i]))

    triple_list = []
    for i in range(len(triplets)):
        a = []
        a1 = triplets[i][0]
        a1 = E_label.index(a1)
        
        a3 = triplets[i][1]
        a3 = R_label.index(a3)
        
        a2 = triplets[i][2]
        a2 = E_label.index(a2)
        a.append(str(a1))
        a.append(str(a3))
        a.append(str(a2))
        triple_list.append((a))
    if(kind == "TransE"):
        transE = TransE(username, entity_set, relation_set, triple_list, embedding_dim=dim, lr=0.01, margin=1.0, norm=2)
        transE.data_initialise()
        resE,resR = transE.training_run()
    elif(kind == "TransH"):
        transH = TransH(entity_set, relation_set, triple_list, embedding_dim=dim, lr=0.01, margin=1.0, norm=2)
        transH.data_initialise()
        resE,resR = transH.training_run()
    else:
        resE,resR = [],[]
    return resE,resR,E_label,R_label

