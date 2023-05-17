import json

from neo4j import GraphDatabase
import format_convert

# 连接neo4j
uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4jneo4j"))


def init_node(tx):
    tx.run("MERGE (n1:OtherNode{name:'交通法规'})"
           "MERGE (n2:OtherNode{name:'地方法规'})"
           "MERGE (n3:OtherNode{name:'全国性法规'})"
           "MERGE (n4:OtherNode{name:'武汉市地方法规'})"
           "MERGE (n5:OtherNode{name:'江永县地方法规'})"
           "MERGE (n6:OtherNode{name:'上海市地方法规'})"
           )

def init_relationships(tx):
    tx.run("MATCH (n1:OtherNode{name:'交通法规'}),(n2:OtherNode{name:'地方法规'})"
           "MERGE (n2)-[:属于]->(n1)"
           )
    tx.run("MATCH (n1:OtherNode{name:'交通法规'}),(n2:OtherNode{name:'全国性法规'})"
           "MERGE (n2)-[:属于]->(n1)"
           )
    tx.run("MATCH (n1:OtherNode{name:'地方法规'}),(n2:OtherNode{name:'江永县地方法规'})"
           "MERGE (n2)-[:属于]->(n1)"
           )
    tx.run("MATCH (n1:OtherNode{name:'地方法规'}),(n2:OtherNode{name:'武汉市地方法规'})"
           "MERGE (n2)-[:属于]->(n1)"
           )
    tx.run("MATCH (n1:OtherNode{name:'地方法规'}),(n2:OtherNode{name:'上海市地方法规'})"
           "MERGE (n2)-[:属于]->(n1)"
           )

def init_act_rule(tx):
    tx.run("match (from:ACT{belong:'上海市地方法规'}),(to:OtherNode{name:'上海市地方法规'})"
           "merge (from)-[:属于]->(to)"
           )
    tx.run("match (from:ACT{belong:'武汉市地方法规'}),(to:OtherNode{name:'武汉市地方法规'})"
           "merge (from)-[:属于]->(to)"
           )
    tx.run("match (from:ACT{belong:'全国性法规'}),(to:OtherNode{name:'全国性法规'})"
           "merge (from)-[:属于]->(to)"
           )
    tx.run("match (from:ACT{belong:'江永县地方法规'}),(to:OtherNode{name:'江永县地方法规'})"
           "merge (from)-[:属于]->(to)"
           )

# 创建节点(ACT)
def merge_act(tx, name, belong):
    result = tx.run("MERGE (a:ACT {name: $name,belong:$belong})", name=name, belong=belong)
    return result


# 创建节点(LAW)
def merge_law(tx, name):
    result = tx.run("MERGE (a:LAW {name: $name})", name=name)
    return result


# 创建节点(PUNISH)
def merge_punish(tx, name):
    result = tx.run("MERGE (a:PUNISH {name: $name})", name=name)
    return result


# 创建节点(SCORE)
def merge_score(tx, name):
    result = tx.run("MERGE (a:SCORE {name: $name})", name=name)
    return result


# 定义创建节点关系(ACT according to LAW)
def merge_relationship_according_to(tx, ACT_name, LAW_name, ACT_belong):
    tx.run("MATCH (act:ACT{name:$ACT_name,belong:$ACT_belong}),(law:LAW{name:$LAW_name})"
           "MERGE (act)-[:根据]->(law)",
           ACT_name=ACT_name, LAW_name=LAW_name, ACT_belong=ACT_belong)


# 定义创建节点关系(ACT punishment PUNISH)
def merge_relationship_punishment_is(tx, ACT_name, PUNISH_name, ACT_belong):
    tx.run("MATCH (act:ACT{name:$ACT_name,belong:$ACT_belong}),(punish:PUNISH{name:$PUNISH_name})"
           "MERGE (act)-[:惩罚措施]->(punish)",
           ACT_name=ACT_name, PUNISH_name=PUNISH_name, ACT_belong=ACT_belong)


# 定义创建节点关系(ACT deduction_of_points SCORE)
def merge_relationship_deduction_of_points(tx, ACT_name, SCORE_name, ACT_belong):
    tx.run("MATCH (act:ACT{name:$ACT_name,belong:$ACT_belong}),(score:SCORE{name:$SCORE_name})"
           "MERGE (act)-[:记分]->(score)",
           ACT_name=ACT_name, SCORE_name=SCORE_name, ACT_belong=ACT_belong)

# 批处理创建节点(上海)
def batch_create_nodes_ShangHai(tx):
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///ShangHai.csv' AS line   "
           "MERGE (n1:ACT{name:line.ACT,belong:line.BELONG})"
           "MERGE (n2:PUNISH{name:line.PUNISH})"
           "MERGE (n3:SCORE{name:line.SCORE})"
           )

# 批处理创建节点(全国性)
def batch_create_nodes_Nation(tx):
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///Nation.csv' AS line    "
           "MERGE (n1:ACT{name:line.ACT,belong:line.BELONG,code:line.CODE})"
           "MERGE (n2:PUNISH{name:line.PUNISH})"
           "MERGE (n3:SCORE{name:line.SCORE})"
           "MERGE (n4:OTHER_PENALTIES{name:line.OTHER_PENALTIES})"
           )

# 批处理创建节点(武汉)
def batch_create_nodes_WuHan(tx):
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///WuHan.csv' AS line   "
           "MERGE (n1:ACT{name:line.ACT,belong:line.BELONG,code:line.CODE})"
           "MERGE (n2:PUNISH{name:line.PUNISH})"
           "MERGE (n3:SCORE{name:line.SCORE})"
           "MERGE (n4:LAW{name:line.LAW})"
           "MERGE (n5:PUNISH_BASIS{name:line.PUNISH_BASIS})"
           "MERGE (n6:ENFORCEMENT{name:line.ENFORCEMENT})"
           "MERGE (n7:ENFORCEMENT_BASIS{name:line.ENFORCEMENT_BASIS})"
           "MERGE (n8:OTHER_MEASURES{name:line.OTHER_MEASURES})"
           "MERGE (n9:BELONG{name:line.BELONG})"
           )

# 批处理创建节点(江永)
def batch_create_nodes_JiangYong(tx):
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///JiangYong.csv' AS line    "
           "MERGE (n1:ACT{name:line.ACT,belong:line.BELONG,code:line.CODE})"
           "MERGE (n2:PUNISH{name:line.PUNISH})"
           "MERGE (n3:SCORE{name:line.SCORE})"
           "MERGE (n4:LAW{name:line.LAW})"
           "MERGE (n5:PUNISH_BASIS{name:line.PUNISH_BASIS})"
           "MERGE (n6:ENFORCEMENT{name:line.ENFORCEMENT})"
           "MERGE (n7:ENFORCEMENT_BASIS{name:line.ENFORCEMENT_BASIS})"
           )


def batch_create_relationships_Shanghai(tx):
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///ShangHai.csv' AS line   "
           "match (from:ACT{name:line.ACT,belong:line.BELONG}),(to:PUNISH{name:line.PUNISH})"
           "merge (from)-[r:惩罚措施]->(to)"
           )
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///ShangHai.csv' AS line   "
           "match (from:ACT{name:line.ACT,belong:line.BELONG}),(to:SCORE{name:line.SCORE})"
           "merge (from)-[r:记分]->(to)"
           )
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///ShangHai.csv' AS line   "
           "match (from:ACT{name:line.ACT,belong:line.BELONG}),(to:PUNISH{name:line.PUNISH})"
           "merge (from)-[r:惩罚措施]->(to)"
           )

def batch_create_relationships_WuHan(tx):
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///WuHan.csv' AS line   "
           "match (from:ACT{name:line.ACT,belong:line.BELONG}),(to:PUNISH{name:line.PUNISH})"
           "merge (from)-[:惩罚措施]->(to)"
           )
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///WuHan.csv' AS line   "
           "match (from:ACT{name:line.ACT,belong:line.BELONG}),(to:OTHER_PENALTIES{name:line.OTHER_PENALTIES})"
           "merge (from)-[:惩罚措施]->(to)"
           )
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///WuHan.csv' AS line   "
           "match (from:ACT{name:line.ACT,belong:line.BELONG}),(to:OTHER_MEASURES{name:line.OTHER_MEASURES})"
           "merge (from)-[:惩罚措施]->(to)"
           )
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///WuHan.csv' AS line   "
           "match (from:ACT{name:line.ACT,belong:line.BELONG}),(to:ENFORCEMENT{name:line.ENFORCEMENT})"
           "merge (from)-[:惩罚措施]->(to)"
           )
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///WuHan.csv' AS line   "
           "match (from:ACT{name:line.ACT,belong:line.BELONG}),(to:SCORE{name:line.SCORE})"
           "merge (from)-[:记分]->(to)"
           )
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///WuHan.csv' AS line   "
           "match (from:ACT{name:line.ACT,belong:line.BELONG}),(to:LAW{name:line.LAW})"
           "merge (from)-[:依据]->(to)"
           )
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///WuHan.csv' AS line   "
           "match (from:PUNISH{name:line.PUNISH}),(to:PUNISH_BASIS{name:line.PUNISH_BASIS})"
           "merge (from)-[:依据]->(to)"
           )
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///WuHan.csv' AS line   "
           "match (from:ENFORCEMENT{name:line.ENFORCEMENT}),(to:ENFORCEMENT_BASIS{name:line.ENFORCEMENT_BASIS})"
           "merge (from)-[:依据]->(to)"
           )
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///WuHan.csv' AS line   "
           "match (from:OTHER_MEASURES{name:line.OTHER_MEASURES}),(to:PUNISH_BASIS{name:line.OTHER_MEASURES_BASIS})"
           "merge (from)-[:依据]->(to)"
           )

def batch_create_relationships_Nation(tx):
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///Nation.csv' AS line   "
           "match (from:ACT{name:line.ACT,belong:line.BELONG}),(to:PUNISH{name:line.PUNISH})"
           "merge (from)-[:惩罚措施]->(to)"
           )
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///Nation.csv' AS line   "
           "match (from:ACT{name:line.ACT,belong:line.BELONG}),(to:OTHER_PENALTIES{name:line.OTHER_PENALTIES})"
           "merge (from)-[:惩罚措施]->(to)"
           )
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///Nation.csv' AS line   "
           "match (from:ACT{name:line.ACT,belong:line.BELONG}),(to:SCORE{name:line.SCORE})"
           "merge (from)-[:记分]->(to)"
           )

def batch_create_relationships_JiangYong(tx):
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///JiangYong.csv' AS line   "
           "match (from:ACT{name:line.ACT,belong:line.BELONG}),(to:PUNISH{name:line.PUNISH})"
           "merge (from)-[:惩罚措施]->(to)"
           )
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///JiangYong.csv' AS line   "
           "match (from:ACT{name:line.ACT,belong:line.BELONG}),(to:ENFORCEMENT{name:line.ENFORCEMENT})"
           "merge (from)-[:惩罚措施]->(to)"
           )
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///JiangYong.csv' AS line   "
           "match (from:ACT{name:line.ACT,belong:line.BELONG}),(to:SCORE{name:line.SCORE})"
           "merge (from)-[:记分]->(to)"
           )
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///JiangYong.csv' AS line   "
           "match (from:ACT{name:line.ACT,belong:line.BELONG}),(to:LAW{name:line.LAW})"
           "merge (from)-[:依据]->(to)"
           )
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///JiangYong.csv' AS line   "
           "match (from:PUNISH{name:line.PUNISH}),(to:PUNISH_BASIS{name:line.PUNISH_BASIS})"
           "merge (from)-[:依据]->(to)"
           )
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///JiangYong.csv' AS line   "
           "match (from:ENFORCEMENT{name:line.ENFORCEMENT}),(to:ENFORCEMENT_BASIS{name:line.ENFORCEMENT_BASIS})"
           "merge (from)-[:依据]->(to)"
           )

def create_nodes(nodes_list, belong):
    i = 0
    for node in nodes_list:
        with driver.session() as session:
            print(i)
            if 'ACT' in node:
                session.execute_write(merge_act, node.get('ACT'), belong)
            if 'LAW' in node:
                session.execute_write(merge_law, node.get('LAW'))
            if 'PUNISH' in node:
                session.execute_write(merge_punish, node.get('PUNISH'))
            if 'SCORE' in node:
                session.execute_write(merge_score, node.get('SCORE'))
            session.close()
            i = i + 1


def create_relationship(nodes_list, belong):
    i = 0
    for node in nodes_list:
        with driver.session() as session:
            print(i)
            if 'ACT' in node and 'LAW' in node:
                res = session.execute_write(merge_relationship_according_to, node.get('ACT'), node.get('LAW'), belong)
            if 'ACT' in node and 'PUNISH' in node:
                res = session.execute_write(merge_relationship_punishment_is, node.get('ACT'), node.get('PUNISH'),
                                            belong)
            if 'ACT' in node and 'SCORE' in node:
                res = session.execute_write(merge_relationship_deduction_of_points, node.get('ACT'), node.get('SCORE'),
                                            belong)
            print(res)
            session.close()
        i = i + 1

def removal(tx):
    tx.run("LOAD CSV WITH HEADERS  FROM 'file:///Nation.csv' AS line   "
           "match (node1:Act{name:line.ACT})"
           "where node1.belong <> '全国性法规'"
           "delete node1"
    )


if __name__ == '__main__':
    # # 结构化数据
    # list_struct_data = []
    # with open('./resources/struct_res.json', 'r', encoding='utf-8') as f:
    #     list_struct_data = json.load(f)
    # struct_nodes_list = list_struct_data
    # # 非机构化数据
    # with open('./resources/output.txt', 'r', encoding='GBK') as f:
    #     content = f.read()
    # content = eval(content)
    # unstruct_nodes_list = format_convert.w2ner2list(content)
    #
    # create_nodes(struct_nodes_list)
    # create_nodes(unstruct_nodes_list, "上海市地方法规")
    # create_relationship(struct_nodes_list)
    # create_relationship(unstruct_nodes_list, "上海市地方法规")
    # driver.close()
    with driver.session() as session:
        # session.execute_write(init_node)
        # session.execute_write(init_relationships)
        # # 上海
        # session.execute_write(batch_create_nodes_ShangHai)
        # session.execute_write(batch_create_relationships_Shanghai)
        # # 武汉
        # session.execute_write(batch_create_nodes_WuHan)
        # session.execute_write(batch_create_relationships_WuHan)
        # # 江永
        # session.execute_write(batch_create_nodes_JiangYong)
        # session.execute_write(batch_create_relationships_JiangYong)
        # 全国性
        # session.execute_write(batch_create_nodes_Nation)
        # session.execute_write(batch_create_relationships_Nation)
        #
        # session.execute_write(init_act_rule)
        session.execute_write(removal)
    driver.close()
