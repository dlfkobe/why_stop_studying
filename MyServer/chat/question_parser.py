class QuestionParser:
    '''构建实体节点'''
    def build_entitydict(self,args):
        entity_dict = {}
        for arg,types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict
    
    '''解析主函数'''
    def parser_main(self,res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        
        for question_type in question_types:
            sql_ = {} # 注意与下面sql的语句
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'ts_stk':
                sql = self.sql_transfer(question_type,entity_dict.get('ts'))
            elif question_type == 'stk_ts':
                sql = self.sql_transfer(question_type,entity_dict.get('stk'))
            elif question_type == 'ts_list_date':
                sql = self.sql_transfer(question_type,entity_dict.get('ts'))
            elif question_type == 'ts_par':
                sql = self.sql_transfer(question_type,entity_dict.get('ts'))
            elif question_type == 'ts_issue_size':
                sql = self.sql_transfer(question_type,entity_dict.get('ts'))
            elif question_type == 'ts_bond_full_name':
                sql = self.sql_transfer(question_type,entity_dict.get('ts'))
            elif question_type == 'ts_bond_short_name':
                sql = self.sql_transfer(question_type,entity_dict.get('ts'))
            elif question_type == 'ts_pay_per_year':
                sql = self.sql_transfer(question_type,entity_dict.get('ts'))
            elif question_type == 'ts_value_date':
                sql = self.sql_transfer(question_type,entity_dict.get('ts'))
            elif question_type == 'ts_maturity_date':
                sql = self.sql_transfer(question_type,entity_dict.get('ts'))
            elif question_type == 'ts_exchange':
                sql = self.sql_transfer(question_type,entity_dict.get('ts'))
            elif question_type == 'fund_manager':
                # 基金部分
                sql = self.sql_transfer(question_type,entity_dict.get('fund'))
            elif question_type == 'manager_fund':
                sql = self.sql_transfer(question_type,entity_dict.get('manager'))
            elif question_type == 'fund_management':
                sql = self.sql_transfer(question_type,entity_dict.get('fund'))
            elif question_type == 'management_fund':
                sql = self.sql_transfer(question_type,entity_dict.get('management'))
            elif question_type == 'manager_management':
                sql = self.sql_transfer(question_type,entity_dict.get('manager'))
            elif question_type == 'management_manager':
                sql = self.sql_transfer(question_type,entity_dict.get('management'))
            elif question_type == 'fund_chinese_name':
                sql = self.sql_transfer(question_type,entity_dict.get('fund'))
            elif question_type == 'fund_type':
                sql = self.sql_transfer(question_type,entity_dict.get('fund'))
            elif question_type == 'fund_fund_type':
                sql = self.sql_transfer(question_type,entity_dict.get('fund'))
            elif question_type == 'fund_benchmark':
                sql = self.sql_transfer(question_type,entity_dict.get('fund'))
            elif question_type == 'fund_issue_amount':
                sql = self.sql_transfer(question_type,entity_dict.get('fund'))
            elif question_type == 'fund_m_fee':
                sql = self.sql_transfer(question_type,entity_dict.get('fund'))
            elif question_type == 'fund_min_amount':
                sql = self.sql_transfer(question_type,entity_dict.get('fund'))
            elif question_type == 'manager_edu':
                sql = self.sql_transfer(question_type,entity_dict.get('manager'))
            elif question_type == 'manager_gender':
                sql = self.sql_transfer(question_type,entity_dict.get('manager'))
            elif question_type == 'manager_resume':
                sql = self.sql_transfer(question_type,entity_dict.get('manager'))
            elif question_type == 'manager_birth_year':
                sql = self.sql_transfer(question_type,entity_dict.get('manager'))

            if sql:
                sql_['sql'] = sql 
                sqls.append(sql_)
        
        return sqls # 可以是多条
    
    '''针对不同问题，分类处理'''
    def sql_transfer(self,question_type,entities):
        if not entities:
            return []
        
        # 查询语句
        sql = []
        
        if question_type == 'ts_stk':
            # 结合自己业务编写cql
            sql = ["MATCH (m:Cb)-[r:match_to]->(n:Stk) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]  # 调用match语句
        elif question_type == 'stk_ts':
            sql = ["MATCH (m:Cb)-[r:match_to]->(n:Stk) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        elif question_type == 'ts_list_date':
            sql = ["MATCH (m:Cb) where m.name = '{0}' return m.name, m.list_date".format(i) for i in entities]
        elif question_type == 'ts_issue_size':
            sql = ["MATCH (m:Cb) where m.name = '{0}' return m.name, m.issue_size".format(i) for i in entities]
        elif question_type == 'ts_bond_full_name':
            sql = ["MATCH (m:Cb) where m.name = '{0}' return m.name, m.bond_full_name".format(i) for i in entities]
        elif question_type == 'ts_bond_short_name':
            sql = ["MATCH (m:Cb) where m.name = '{0}' return m.name, m.bond_short_name".format(i) for i in entities]
        elif question_type == 'ts_pay_per_year':
            sql = ["MATCH (m:Cb) where m.name = '{0}' return m.name, m.pay_per_year".format(i) for i in entities]
        elif question_type == 'ts_value_date':
            sql = ["MATCH (m:Cb) where m.name = '{0}' return m.name, m.value_date".format(i) for i in entities]
        elif question_type == 'ts_maturity_date':
            sql = ["MATCH (m:Cb) where m.name = '{0}' return m.name, m.maturity_date".format(i) for i in entities]
        elif question_type == 'ts_exchange':
            sql = ["MATCH (m:Cb) where m.name = '{0}' return m.name, m.exchange".format(i) for i in entities]
        elif question_type == 'fund_manager':
            # 基金部分
            sql = ["MATCH (m:Fund)-[r:manage_by_who]->(n:Manager) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]  # 调用match语句
        elif question_type == 'manager_fund':
            sql = ["MATCH (m:Fund)-[r:manage_by_who]->(n:Manager) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        elif question_type == 'fund_management':
            sql = ["MATCH (m:Fund)-[r:belong_to]->(n:Management) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]    
        elif question_type == 'management_fund':
            sql = ["MATCH (m:Fund)-[r:belong_to]->(n:Management) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        elif question_type == 'manager_management':
            sql = ["MATCH (m:Manager)-[r:served_at]->(n:Management) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        elif question_type == 'management_manager':
            sql = ["MATCH (m:Manager)-[r:served_at]->(n:Management) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
        elif question_type == 'fund_type':
            sql = ["MATCH (m:Fund) where m.name = '{0}' return m.name, m.type_".format(i) for i in entities]
        elif question_type == 'fund_fund_type':
            sql = ["MATCH (m:Fund) where m.name = '{0}' return m.name, m.fund_type".format(i) for i in entities]
        elif question_type == 'fund_chinese_name':
            sql = ["MATCH (m:Fund) where m.name = '{0}' return m.name, m.chinese_name".format(i) for i in entities]
        elif question_type == 'fund_benchmark':
            sql = ["MATCH (m:Fund) where m.name = '{0}' return m.name, m.benchmark".format(i) for i in entities]
        elif question_type == 'fund_issue_amount':
            sql = ["MATCH (m:Fund) where m.name = '{0}' return m.name, m.issue_amount".format(i) for i in entities]
        elif question_type == 'fund_m_fee':
            sql = ["MATCH (m:Fund) where m.name = '{0}' return m.name, m.m_fee".format(i) for i in entities]
        elif question_type == 'fund_min_amount':
            sql = ["MATCH (m:Fund) where m.name = '{0}' return m.name, m.min_amount".format(i) for i in entities]
        elif question_type == 'manager_edu':
            sql = ["MATCH (m:Manager) where m.name = '{0}' return m.name, m.edu".format(i) for i in entities]
        elif question_type == 'manager_edu':
            sql = ["MATCH (m:Manager) where m.name = '{0}' return m.name, m.edu".format(i) for i in entities]
        elif question_type == 'manager_gender':
            sql = ["MATCH (m:Manager) where m.name = '{0}' return m.name, m.gender".format(i) for i in entities]
        elif question_type == 'manager_resume':
            sql = ["MATCH (m:Manager) where m.name = '{0}' return m.name, m.resume".format(i) for i in entities]
        elif question_type == 'manager_birth_year':
            sql = ["MATCH (m:Manager) where m.name = '{0}' return m.name, m.birth_year".format(i) for i in entities]
            
        return  sql
    
if __name__ == '__main__':
    handler = QuestionParser()
        
        
        
   
                
            
        
                