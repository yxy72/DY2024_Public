from py2neo import Node,Relationship,Graph,Path,Subgraph,NodeMatcher,RelationshipMatcher
import base64

import configs 


graph = None


def getTotalNums():
    try:
        graph = Graph(configs.neo4j_url, auth=(configs.neo4j_username, configs.neo4j_password))
        return {
            "status":True,
            }
    except:
        return {"status":False,"url":configs.neo4j_url}


def getGrphInfo():
    try:

        graph = Graph(configs.neo4j_url, auth=(configs.neo4j_username, configs.neo4j_password))
        nodes = list(graph.schema.node_labels)
        relations = list(graph.schema.relationship_types)
        return {
            "status":True,
            "neo4j_username":configs.neo4j_username,
            "neo4j_password":str(base64.b64encode(str.encode(configs.neo4j_password)))[2:-1],
            "url":configs.neo4j_url,
            "allNodesNum":graph.run("MATCH(n) RETURN count(n)").data()[0]["count(n)"],
            "nodes":nodes,
            "relations":relations,
            "totalNums": graph.run("MATCH n=()-->() RETURN count(n)").data()[0]["count(n)"],
            }
    except:
        return {"status":False,"url":configs.neo4j_url}
def query(class_):
    try:
        graph = Graph(configs.neo4j_url, auth=(configs.neo4j_username, configs.neo4j_password))
        data = graph.run("MATCH(n:`"+class_+"`) RETURN n").data()
        list_ = [ item['n']['name'] for item in data ]
        return list_
    except:
        return []
def getAllTriples():
    try:
        graph = Graph(configs.neo4j_url, auth=(configs.neo4j_username, configs.neo4j_password))
        A = (graph.run("MATCH n=()-->() RETURN n").data())
        TRIPLELIST = []
        for index,item in enumerate(A):
            TRIPLELIST.append({})
            TRIPLELIST[index]["start_node"] = item['n'][0].start_node["name"]
            TRIPLELIST[index]["end_node"] = item['n'][0].end_node["name"]
            TRIPLELIST[index]["relationship"] = [a for a in (item['n'][0].types())][0]
        return True,TRIPLELIST
    except:
        return False,None

def ifNodeExist(label,name):
    try:
        graph = Graph(configs.neo4j_url, auth=(configs.neo4j_username, configs.neo4j_password))
        query = f"MATCH(n:`{label}`) where n.name='{name}' RETURN n"
        length = len(graph.run(query).data())
        return {
            "status":True,
            "exist":length>0,
            }
    except:
        return {"status":False,"url":configs.neo4j_url}
    
def addNode(label,name,usr="default"):
    try:
        graph = Graph(configs.neo4j_url, auth=(configs.neo4j_username, configs.neo4j_password))
        query = "CREATE (n:%s {name:'%s', FROM: '%s'})"%(label,name,usr)
        graph.run(query)
        return {
            "status":True
            }
    except:
        return {"status":False,"url":configs.neo4j_url}
def delNode(label,name):
    try:
        graph = Graph(configs.neo4j_url, auth=(configs.neo4j_username, configs.neo4j_password))
        query = f"MATCH (n:{label}) WHERE n.name = '{name}' DETACH DELETE n"
        graph.run(query)
        return {
            "status":True
            }
    except:
        return {"status":False,"url":configs.neo4j_url}
def getNeighborNode(label,name):
    try:
        graph = Graph(configs.neo4j_url, auth=(configs.neo4j_username, configs.neo4j_password))
        data = graph.run(f"MATCH(n:`{label}`)-[r]->(nn) where n.name='{name}' RETURN nn").data()
        bb = [{"label":label,"name":name}]
        for i in data:
            bb.append({"label":str(i['nn'].labels)[1:],"name":(i['nn'])["name"]})
        return {
            "status":True,
            "data":bb
            }
    except:
        return {"status":False,"data":[],"url":configs.neo4j_url}
    
def autoTriplesToKG(target,triples):
    try:
        graph = Graph(configs.neo4j_url, auth=(configs.neo4j_username, configs.neo4j_password))
        if(target not in list(graph.schema.node_labels)):
            hList = []
            tList = []
            nodes = []
            relations = []
            for item in triples:
                if(item["head"] not in hList):
                    hList.append(item["head"])
                if(item["tail"] not in tList):
                    tList.append(item["tail"])
            for item in hList:
                nodes.append(Node(target,name = item,FROM = "createTriplet",color="#F56C6C"))
            for item in tList:
                nodes.append(Node(target,name = item,FROM = "createTriplet",color="#409EFF"))

            for item in triples:
                for node in nodes:
                    if(node["name"] == item["head"]):
                        HEAD = node
                        break
                for node in nodes:
                    if(node["name"] == item["tail"]):
                        TAIL = node
                        break
                relations.append(Relationship(HEAD, item["relation"], TAIL,name = item["relation"]))
            subgraph = Subgraph(nodes, relations)
            tx = graph.begin() 
            tx.create(subgraph)
            graph.commit(tx)
            
        else:
            for item in triples:
                HEAD = Node(target, name = item["head"],FROM = "createTriplet",color="#F56C6C")
                TAIL = Node(target, name = item["tail"],FROM = "createTriplet",color="#409EFF")
                graph.merge(Relationship(HEAD, item["relation"], TAIL,name = item["relation"]), target, "name")
        return {
            "status":True
        }
    except:
        return {"status":False,"data":[],"url":configs.neo4j_url}
