import os
import json
from py2neo import Graph,Node

class FinanceGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])# 获取当前绝对路径的上层目录 linux中应用'/'split和join
        self.data_path = os.path.join(cur_dir, 'data/cb_data2.json')# 获取json文件路径
        # self.g = Graph("http://localhost:7474", username="neo4j", password="123456")#老版本neo4j
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123456"))
    '''读取文件'''
    def read_nodes(self):
        
        # 债券类，共两类节点
        ts_codes = [] #转债代码 列表
        stk_codes = [] #正股名称 列表
        
        # 转债信息表，并不是节点
        cb_infos = []
        
        # 债券类 构建实体关系 共一种
        rels_match_to = []  # 转债与正股的关系
        
        count = 0
        
        for data in open(self.data_path,encoding='utf-8'):
            print(data)
            cb_dict = {}
            count += 1
            print(count)
            data_json = json.loads(data)
            cb = data_json['ts_code']
            cb_dict['ts_code'] = cb
            ts_codes.append(cb)
            # 转债代码属性
            cb_dict['list_date'] = ''              # 上市日期
            cb_dict['par'] = ''                    # 面值
            cb_dict['issue_size'] = ''             # 发行总额
            cb_dict['bond_full_name'] = ''         # 转债名称
            cb_dict['bond_short_name'] = ''        # 转债简称
            cb_dict['pay_per_year'] = ''           # 年付息次数
            cb_dict['value_date'] = ''             # 起息日期
            cb_dict['maturity_date'] = ''          # 到期日期
            cb_dict['exchange'] = ''               # 上市地点
            
            # 字段是否在文档段中，前期已经将每段数据的字段处理到一致,为以防万一加了if判断
            if 'stk_code' in data_json:
                stk_codes.append(data_json['stk_code'])
                rels_match_to.append([cb,data_json['stk_code']])  # 对于每个转债代码与其正股代码建立联系
            
            # 属性部分
            if 'list_date' in data_json:               
                cb_dict['list_date'] = data_json['list_date']   # 上市日期
                
            if 'par' in data_json:
                cb_dict['par'] = data_json['par'] # 面值
                
            if 'issue_size' in data_json:
                cb_dict['issue_size'] = data_json['issue_size'] # 发行总额
                
            if 'bond_full_name' in data_json:
                cb_dict['bond_full_name'] = data_json['bond_full_name'] # 转债名称
            
            if 'bond_short_name' in data_json:
                cb_dict['bond_full_name'] = data_json['bond_short_name'] # 转债简称
                
            if 'pay_per_year' in data_json:
                cb_dict['pay_per_year'] = data_json['pay_per_year'] # 年付息次数
                
            if 'value_date' in data_json:
                cb_dict['value_date'] = data_json['value_date'] # 起息日期
                
            if 'maturity_date' in data_json:
                cb_dict['maturity_date'] = data_json['maturity_date'] # 到期日期
                
            if 'exchange' in data_json:     
                cb_dict['exchange'] = data_json['exchange'] # 上市地点  
            
            cb_infos.append(cb_dict) # 添加转债信息
            
        return set(ts_codes),set(stk_codes),cb_infos,rels_match_to
    
    '''建立节点'''
    def create_node(self,lable,nodes):
        count = 0
        for node_name in nodes:
            node = Node(lable,name = node_name)
            self.g.create(node)
            count += 1
            print(count,len(nodes))
        return
    
    '''创建知识图谱中心转债节点'''
    def create_cbs_nodes(self,cb_infos):
        count = 0
        for cb_dict in cb_infos:
            node = Node('Cb',name=cb_dict['ts_code'],
                        list_date=cb_dict['list_date'],
                        par=cb_dict['par'],
                        issue_size=cb_dict['issue_size'],
                        bond_full_name=cb_dict['bond_full_name'],
                        bond_short_name=cb_dict['bond_short_name'],
                        pay_per_year=cb_dict['pay_per_year'],
                        value_date=cb_dict['value_date'],
                        maturity_date=cb_dict['maturity_date'],
                        exchange=cb_dict['exchange']
                        )
            self.g.create(node)
            count += 1
            print(count)
        return
    
    '''创新非中心节点，债券类只有一个正股节点'''
    def create_graphnodes(self):
        ts_codes,stk_codes,cb_infos,rels_match_to = self.read_nodes()
        self.create_cbs_nodes(cb_infos)
        self.create_node('Stk',stk_codes)  # 创建正股节点
        print(len(stk_codes))
        return 
    
    '''创建实体关联边'''
    def create_relationship(self,start_node,end_node,edges,rel_type,rel_name):
        # 参数含义： 起点节点，终点节点，边，关系类型，关系名字
        count = 0
        # 去重，自己的知识图谱宅债券类数据缘故不涉及去重，为了以防万一写上
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)#match语法，p，q分别为标签，rel_type关系类别，rel_name 关系名字
            try:
                self.g.run(query)
                count += 1
                print(rel_type,count,all)
            except Exception as e:
                print(e)
        return 
        
       
    
    '''创建1种关系边，哈哈，债券类只设计了一种，重心都在基金'''
    def create_graphrels(self):
        ts_codes,stk_codes,cb_infos,rels_match_to = self.read_nodes()
        self.create_relationship('Cb','Stk',rels_match_to,'match_to','对应正股为')
    
        
        '''导出数据'''
    def export_data(self):
        ts_codes,stk_codes,cb_infos,rels_match_to = self.read_nodes()
        f_ts = open('./dict/ts.txt', 'w+')
        f_stk = open('./dict/stk.txt', 'w+')
        
        f_ts.write('\n'.join(list(ts_codes)))
        f_stk.write('\n'.join(list(stk_codes)))
        
        f_ts.close()
        f_stk.close()
        return
   
                
            

        

if __name__ == '__main__':
    handler = FinanceGraph()#创建图数据库
    #handler.export_data()#输出数据，可以选择不执行
    handler.create_graphnodes()#创建节点
    handler.create_graphrels()#创建关系
    handler.export_data() #导出数据
