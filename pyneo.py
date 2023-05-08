from neo4j import GraphDatabase
import format_convert
# 连接neo4j
uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4jneo4j"))


# 创建节点(ACT)
def merge_act(tx, name):
    tx.run("MERGE (a:ACT {name: $name})", name=name)


# 创建节点(LAW)
def merge_law(tx, name):
    tx.run("CREATE (a:LAW {name: $name})", name=name)


# 创建节点(PUNISH)
def merge_punish(tx, name):
    tx.run("CREATE (a:PUNISH {name: $name})", name=name)


# 创建节点(SCORE)
def merge_score(tx, name):
    tx.run("CREATE (a:SCORE {name: $name})", name=name)


# 定义创建节点关系(ACT according to LAW)
def merge_relationship_according_to(tx, ACT_name, LAW_name):
    tx.run("MATCH (act:ACT{name:$ACT_name}),(law:LAW{name:$LAW_name})"
           "MERGE (act)-[:根据]->(law)",
           ACT_name=ACT_name, LAW_name=LAW_name)


# 定义创建节点关系(ACT punishment PUNISH)
def merge_relationship_punishment_is(tx, ACT_name, PUNISH_name):
    tx.run("MATCH (act:ACT{name:$ACT_name}),(punish:PUNISH{name:$PUNISH_name})"
           "MERGE (act)-[:惩罚措施]->(punish)",
           ACT_name=ACT_name, PUNISH_name=PUNISH_name)


# 定义创建节点关系(ACT deduction_of_points SCORE)
def merge_relationship_deduction_of_points(tx, ACT_name, SCORE_name):
    tx.run("MATCH (act:ACT{name:$ACT_name}),(score:SCORE{name:SCORE_name})"
           "MERGE (act)-[:记分]->(score)",
           ACT_name=ACT_name, SCORE_name=SCORE_name)


def create_nodes(nodes_list):
    for node in nodes_list:
        with driver.session() as session:
            if node.has_key('ACT'):
                session.execute_write(merge_act, node.get('ACT'))
            if node.has_key('LAW'):
                session.execute_write(merge_law, node.get('LAW'))
            if node.has_key('PUNISH'):
                session.execute_write(merge_punish, node.get('PUNISH'))
            if node.has_key('SCORE'):
                session.execute_write(merge_score, node.get('SCORE'))

def create_relationship(nodes_list):
    for node in nodes_list:
        with driver.session() as session:
            if node.has_key('ACT') and node.has_key('LAW'):
                session.execute_write(merge_relationship_according_to, node.get('ACT'), node.get('LAW'))
            if node.has_key('ACT') and node.has_key('PUNISH'):
                session.execute_write(merge_relationship_punishment_is, node.get('ACT'), node.get('PUNISH'))
            if node.has_key('ACT') and node.has_key('SCORE'):
                session.execute_write(merge_relationship_deduction_of_points, node.get('ACT'), node.get('SCORE'))

if __name__ == '__main__':
    list_predict = []
    create_nodes(format_convert.w2ner2(list_predict))
    create_relationship(format_convert.w2ner2(list_predict))
