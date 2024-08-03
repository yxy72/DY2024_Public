from py2neo import Node,Relationship,Graph,Path,Subgraph,NodeMatcher,RelationshipMatcher
# 运行 python init_kg.py "bolt://127.0.0.1:7687" "neo4j" "Abc123()"


import pandas as pd
import numpy as np
import sys
# datasets = pd.read_excel('data_triplet_189_3.xlsx')

if __name__ == "__main__":
    if(len(sys.argv[:])!=4):
        print("ERROR: parameters should be 3: type this: \npython init_kg.py 'address' 'neo4jUser' 'neo4jPwd'")
        exit(0)
    # 运行 python init_kg.py "127.0.0.1" "neo4j" "Abc123()"

    graph = Graph(sys.argv[1], auth=(sys.argv[2], sys.argv[3]))

    datasets = pd.read_excel('tripletname.xlsx')
    datasets2 = pd.read_excel('tripletname2.xlsx') 
    # 涉密删除 datasets3 = pd.read_excel('tripletname3.xlsx') 

    elist = []
    elist1 = []
    rlist = []
    tlist = []

    for item in (list(datasets['head'])):
        if(item not in elist):
            elist.append(item)
    for item in (list(datasets['tail'])):
        if(item not in elist1):
            elist1.append(item)
            
    tlist = np.array(datasets)


    node = []
    relation = []
    for item in elist:
        node.append(Node("质量因素",name = item,FROM = "default",color="#F56C6C"))
    for item in elist1:
        node.append(Node("质量因素",name = item,FROM = "default",color="#409EFF"))
    for item in tlist:
        for itemNode in node:
            if(itemNode["name"] == item[0]):
                node1 = itemNode
            if(itemNode["name"] == item[2]):
                node2 = itemNode
        relation.append(Relationship(node1, item[1], node2,name=item[1]))


    node2 = []
    elist2 = []
    relation2 = []
    for item in (list(datasets2['tail'])):
        if(item not in elist1):
            elist2.append(item)
            
    node2.append(Node("工艺参数",name = "XX检验-总长",FROM = "default",color="#409EFF"))
    for item in elist2:
        node2.append(Node("工艺参数",name = item,FROM = "default",color="#F56C6C"))
        relation2.append(Relationship(node2[0], "某关系", node2[-1],name="link"))

    graph.run("match (n) detach delete n")

    subgraph2 = Subgraph(node2, relation2)
    tx = graph.begin() 
    tx.create(subgraph2)
    graph.commit(tx)
   

    subgraph = Subgraph(node, relation)
    tx = graph.begin() 
    tx.create(subgraph)
    graph.commit(tx)

 

    print("Complete.")