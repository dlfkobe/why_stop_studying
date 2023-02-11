import os
import json
from py2neo import Graph,Node

class FundGraph:
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
        for data in open(self.data_path,encoding='utf-8'):
            print(data)
            fund_dict = {}
            manager_dict = {}
            count += 1
            print(count)
            data_json = json.loads(data) #读取数据
            # 基金
            fund_code = data_json['ts_code']
            fund_dict['name'] = fund_code
            funds.append(fund_code)
            fund_dict['chinese_name'] = ''
            fund_dict['type'] = ''
            fund_dict['fund_type'] = ''
            fund_dict['benchmark'] = ''
            fund_dict['issue_amount'] = ''
            fund_dict['m_fee'] = ''
            fund_dict['min_amount'] = ''
            # 基金经理
            manager_name = data_json['manager_name']
            manager_dict['name'] = manager_name
            managers.append(manager_name)
            manager_dict['edu'] = ''
            manager_dict['resume'] = ''
            manager_dict['gender'] = ''
            manager_dict['birth_year'] = ''
            # 关系 基金 基金经理
            rels_manage_by_who.append([fund_code, manager_name])
            # management
            if 'management' in data_json:
                managements.append(data_json['management'])
                # 关系 基金 管理人
                rels_belong_to.append([fund_code,data_json['management']])
                # 关系 基金经理 管理人
                rels_served_at.append([manager_name,data_json['management']])
            
            # 基金属性部分
            if 'name' in data_json:
                fund_dict['chinese_name'] = data_json['name']
            
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
                manager_dict['birth_year'] = data_json['birth_year']
            manager_infos.append(manager_dict)
        # print(rels_belong_to,rels_served_at)
        return set(funds),set(managers),set(managements),fund_infos,self.DictinList_duplicate(manager_infos),rels_belong_to,rels_manage_by_who,rels_served_at
    
            
    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱基金经理的节点'''
    def create_manager_nodes(self, manager_infos):
        count = 0
        for manager_dict in manager_infos:
            node = Node("Manager", name=manager_dict['name'], edu=manager_dict['edu'],
                        resume=manager_dict['resume'], gender=manager_dict['gender'],
                        birth_year=manager_dict['birth_year'])#各个疾病节点的属性
            self.g.create(node)
            count+=1
            print(count)
        return
    
    '''创建知识图谱基金的节点'''
    def create_fund_nodes(self, fund_infos):
        count = 0
        
        for fund_dict in fund_infos:
            node = Node("Fund", name=fund_dict['name'],chinese_name=fund_dict['chinese_name'], type_=fund_dict['type'],
                        fund_type=fund_dict['fund_type'], benchmark=fund_dict['benchmark'],
                        issue_amount=fund_dict['issue_amount'], m_fee=fund_dict['m_fee'],
                        min_amount=fund_dict['min_amount'])
            self.g.create(node)
            count += 1
            print(count)
        return
    
    '''创新图谱节点，基金类只有一个管理人非中心节点'''
    def create_graphnodes(self):
        # ts_codes,stk_codes,cb_infos,rels_match_to = self.read_nodes()
        # self.create_cbs_nodes(cb_infos)
        # self.create_node('Stk',stk_codes)  # 创建正股节点
        # print(len(stk_codes))
        funds,managers,managements,fund_infos,manager_infos,rels_belong_to,rels_manage_by_who,rels_served_at = self.read_nodes()
        self.create_fund_nodes(fund_infos)
        self.create_manager_nodes(manager_infos)
        self.create_node("Management",managements)
        print(len(managements))
        return 




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
            print(query)
            try:
                self.g.run(query)#执行语句
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return
    
    '''创建实体关系边'''
    def create_graphrels(self):
        funds,managers,managements,fund_infos,manager_infos,rels_belong_to,rels_manage_by_who,rels_served_at = self.read_nodes()
        self.create_relationship('Fund','Manager',rels_manage_by_who,"manage_by_who","对应基金经理为")
        self.create_relationship("Fund","Management",rels_belong_to,"belong_to","属于")
        self.create_relationship("Manager","Management",rels_served_at,"served_at","任职于")
        
        

    '''导出数据'''
    def export_data(self):
        funds,managers,managements,fund_infos,manager_infos,rels_belong_to,rels_manage_by_who,rels_served_at = self.read_nodes()
        f_fund = open('./dict/fund.txt', 'w+',encoding='utf-8')
        f_manager = open('./dict/manager.txt', 'w+',encoding='utf-8')
        f_management = open('./dict/management.txt', 'w+',encoding='utf-8')
        
        f_fund.write('\n'.join(list(funds)))
        f_manager.write('\n'.join(list(managers)))
        f_management.write('\n'.join(list(managements)))
        
        f_fund.close()
        f_management.close()
        f_manager.close()
        return

    "需要对基金经理info进行去重"
    def DictinList_duplicate(self,data_list):
        """
        列表套字典去重
        :return:
        """
        seen = set()
        new_l = []
        for d in data_list:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                new_l.append(d)
        print(new_l)
        return new_l



if __name__ == '__main__':
    handler = FundGraph()#创建图数据库
    # handler.read_nodes()
    #handler.export_data()#输出数据，可以选择不执行
    handler.create_graphnodes() #创建节点
    handler.create_graphrels() #创建关系
    # handler.export_data()er
