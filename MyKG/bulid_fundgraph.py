import os
import json
from py2neo import Graph,Node

class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])# 获取当前绝对路径的上层目录 linux中应用'/'split和join
        self.data_path = os.path.join(cur_dir, 'data/fund_data2.json')# 获取json文件路径
        # self.g = Graph("http://localhost:7474", username="neo4j", password="123456")#老版本neo4j
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123456"))
    '''读取文件'''
    def read_nodes(self):
        # 共７类节点，节点的设置与业务相关

        funds = [] # 基金代码
        managers = [] # 基金经理名字
        managements = []  # 基金名字（管理人）"大成基金"
  
        fund_infos = [] # 基金信息
        manager_infos = [] # 基金经理信息

        # 构建节点实体关系,共三类
        rels_manage_by_who = [] #　基金-基金经理
        rels_belong_to = [] # 基金-管理人
        rels_served_at = [] # 基金经理-管理人

        count = 0
        for data in open(self.data_path):
            fund_dict = {}
            manager_dict = {}
            count += 1
            print(count)
            data_json = json.loads(data)#读取数据
            # 基金
            fund_code = data_json['ts_code']
            fund_dict['ts_code'] = fund_code
            funds.append(fund_code)
            fund_dict['name'] = ''
            fund_dict['type'] = ''
            fund_dict['fund_type'] = ''
            fund_dict['benchmark'] = ''
            fund_dict['issue_amount'] = ''
            fund_dict['m_fee'] = ''
            fund_dict['min_amount'] = ''
            # 基金经理
            manager_name = data_json['manager_name']
            manager_dict['manager_name'] = manager_name
            managers.append(manager_name)
            manager_dict['edu'] = ''
            manager_dict['resume'] = ''
            manager_dict['gender'] = ''
            manager_dict['birth_year'] = ''
            # 关系 基金 基金经理
            rels_manage_by_who.append([fund_code, manager_name])
            
            if 'management' in data_json:
                managements += data_json['management']
                # 关系 基金 管理人
                rels_belong_to.append([fund_code,data_json['management']])
                # 关系 基金经理 管理人
                rels_served_at.append([manager_name,data_json['management']])
            
            # 基金属性部分
            if 'name' in data_json:
                fund_dict['name'] = data_json['name']
            
            if 'type' in data_json:
                fund_dict['type'] = data_json['type']
            
            if 'fund_type' in data_json:
                fund_dict['fund_type'] = data_json['fund_type']
            
            if 'benchmark' in data_json:
                fund_dict['benchmark'] = data_json['benchmark']
        
            if 'issue_amount' in data_json:
                fund_dict['issue_amount'] = data_json['issue_amount']
        
            if 'm_fee' in data_json:
                fund_dict['m_fee'] = data_json['m_fee']
        
            if 'min_amount' in data_json:
                fund_dict['min_amount'] = data_json['min_amount']
            fund_infos.append(fund_dict)
            
            # 基金经理属性部分
            if 'edu' in data_json:
                manager_dict['edu'] = data_json['edu']
            
            if 'resume' in data_json:
                manager_dict['resume'] = data_json['resume']
            
            if 'gender' in data_json:
                manager_dict['gender'] = data_json['gender']
            
            if 'birth_year' in data_json:
                manager_dict['gender'] = data_json['birth_year']
            manager_infos.append(manager_dict)
            
        return set(funds),set(managers),set(managements),fund_infos,manager_infos,rels_belong_to,rels_manage_by_who,rels_served_at
    
            
    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱基金的节点'''
    def create_diseases_nodes(self, disease_infos):
        count = 0
        for fund_dict in disease_infos:
            node = Node("Disease", name=disease_dict['name'], desc=disease_dict['desc'],
                        prevent=disease_dict['prevent'], cause=disease_dict['cause'],
                        easy_get=disease_dict['easy_get'], cure_lasttime=disease_dict['cure_lasttime'],
                        cure_department=disease_dict['cure_department']
                        ,cure_way=disease_dict['cure_way'], cured_prob=disease_dict['cured_prob'])#各个疾病节点的属性
            self.g.create(node)
            count += 1
            print(count)
        return
    
    '''创建知识图谱基金经理的节点'''
    def create_diseases_nodes(self, disease_infos):
        count = 0
        forfund_dict in disease_infos:
            node = Node("Disease", name=disease_dict['name'], desc=disease_dict['desc'],
                        prevent=disease_dict['prevent'], cause=disease_dict['cause'],
                        easy_get=disease_dict['easy_get'], cure_lasttime=disease_dict['cure_lasttime'],
                        cure_department=disease_dict['cure_department']
                        ,cure_way=disease_dict['cure_way'], cured_prob=disease_dict['cured_prob'])#各个疾病节点的属性
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型schema,节点个数多，创建过程慢'''
    def create_graphnodes(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos,rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,rels_symptom, rels_acompany, rels_category = self.read_nodes()
        self.create_diseases_nodes(disease_infos)#调用上面的疾病节点创建函数
        self.create_node('Drug', Drugs)#创建药物节点
        print(len(Drugs))
        self.create_node('Food', Foods)#创建食物节点
        print(len(Foods))
        self.create_node('Check', Checks)#创建检查节点
        print(len(Checks))
        self.create_node('Department', Departments)#创建科室节点
        print(len(Departments))
        self.create_node('Producer', Producers)#创建制药厂节点
        print(len(Producers))
        self.create_node('Symptom', Symptoms)#创建症状节点
        return


    '''创建11种实体关系边'''
    def create_graphrels(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug,rels_symptom, rels_acompany, rels_category = self.read_nodes()
        self.create_relationship('Disease', 'Food', rels_recommandeat, 'recommand_eat', '推荐食谱')#调用下面的关系边创建函数
        self.create_relationship('Disease', 'Food', rels_noteat, 'no_eat', '忌吃')
        self.create_relationship('Disease', 'Food', rels_doeat, 'do_eat', '宜吃')
        self.create_relationship('Department', 'Department', rels_department, 'belongs_to', '属于')
        self.create_relationship('Disease', 'Drug', rels_commonddrug, 'common_drug', '常用药品')
        self.create_relationship('Producer', 'Drug', rels_drug_producer, 'drugs_of', '生产药品')
        self.create_relationship('Disease', 'Drug', rels_recommanddrug, 'recommand_drug', '好评药品')
        self.create_relationship('Disease', 'Check', rels_check, 'need_check', '诊断检查')
        self.create_relationship('Disease', 'Symptom', rels_symptom, 'has_symptom', '症状')
        self.create_relationship('Disease', 'Disease', rels_acompany, 'acompany_with', '并发症')
        self.create_relationship('Disease', 'Department', rels_category, 'belongs_to', '所属科室')

    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):#起点节点，终点节点，边，关系类型，关系名字
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))#使用###作为不同关系之间分隔的标志
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')#选取前两个关系，因为两个节点之间一般最多两个关系
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)#match语法，p，q分别为标签，rel_type关系类别，rel_name 关系名字
            try:
                self.g.run(query)#执行语句
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据'''
    def export_data(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug, rels_symptom, rels_acompany, rels_category = self.read_nodes()
        f_drug = open('drug.txt', 'w+')
        f_food = open('food.txt', 'w+')
        f_check = open('check.txt', 'w+')
        f_department = open('department.txt', 'w+')
        f_producer = open('producer.txt', 'w+')
        f_symptom = open('symptoms.txt', 'w+')
        f_disease = open('disease.txt', 'w+')

        f_drug.write('\n'.join(list(Drugs)))
        f_food.write('\n'.join(list(Foods)))
        f_check.write('\n'.join(list(Checks)))
        f_department.write('\n'.join(list(Departments)))
        f_producer.write('\n'.join(list(Producers)))
        f_symptom.write('\n'.join(list(Symptoms)))
        f_disease.write('\n'.join(list(Diseases)))

        f_drug.close()
        f_food.close()
        f_check.close()
        f_department.close()
        f_producer.close()
        f_symptom.close()
        f_disease.close()

        return



if __name__ == '__main__':
    handler = MedicalGraph()#创建图数据库
    #handler.export_data()#输出数据，可以选择不执行
    handler.create_graphnodes()#创建节点
    handler.create_graphrels()#创建关系
