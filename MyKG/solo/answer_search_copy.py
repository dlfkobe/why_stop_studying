from py2neo import Graph

class AnswerSearcher:
    def __init__(self): # 调用数据库进行查询
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123456"))
        self.num_limit = 20#最多显示字符数量
    
    '''执行cql查询，并返回查询结果'''
    def search_main(self,sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type'] # cql中的关键字
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress  # 这里为什么用+=
            final_answer = self.answer_prettify(question_type,answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers
    
    '''根据对应的question_type，调用响应的回复模板'''
    def answer_prettify(self,question_type, answers):
        final_answer = []
        if not answers:
            return ''
        elif question_type == 'fund_manager':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0} 目前的基金经理是：{1}'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))
            
        elif question_type == 'manager_fund':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0} 管理的基金（代码）为：{1}'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))
            
        elif question_type == 'fund_management':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0} 属于：{1}'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))
            
        elif question_type == 'management_fund':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0} 管理的产品有：{1}'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))
        
        elif question_type == 'manager_management':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0} 任职于：{1}'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))
            
        elif question_type == 'management_manager':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0} 聘用的经理是：{1}'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))
            
        elif question_type == 'fund_chinese_name':
            desc = [i['m.chinese_name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0} 中文名是：'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))
            
        elif question_type == 'fund_type':
            desc = [i['m.type_'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0} 的基金类型是：{1}'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))
            
        elif question_type == 'fund_fund_type':
            desc = [i['m.fund_type'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0} 的投资类型是：{1}'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'fund_min_amount':
            desc = [i['m.min_amount'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0} 的起点金额为：{1}'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))
            
        elif question_type == 'fund_issue_amount':
            desc = [i['m.issue_amount'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0} 的发行总额为：{1}'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))
            
        elif question_type == 'fund_m_fee':
            desc = [i['m.m_fee'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0} 的管理费为：{1}'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))
            
        elif question_type == 'fund_benchmark':
            desc = [i['m.benchmark'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0} 的业绩比较基准为：{1}'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))
            
        elif question_type == 'manager_edu':
            desc = [i['m.edu'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0} 的学历：{1}'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))
            
        elif question_type == 'manager_gender':
            desc = [i['m.gender'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0} 性别为：{1}'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))
            
        elif question_type == 'manager_resume':
            desc = [i['m.resume'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0} 的简历： {1} '.format(subject,'；'.join(list(set(desc))[:self.num_limit]))
        
        elif question_type == 'manager_birth_year':
            desc = [i['m.birth_year'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0} 的出生日期： {1}'.format(subject,'；'.join(list(set(desc))[:self.num_limit]))
        
        return final_answer
    
if __name__ == '__main__':
    searcher = AnswerSearcher()
