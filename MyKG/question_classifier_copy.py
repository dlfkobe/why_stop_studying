import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # 特征词路径
        self.fund_path = os.path.join(cur_dir,'dict/fund.txt') # 基金代码
        self.manager_path = os.path.join(cur_dir,'dict/manager.txt') # 基金经理名字
        self.management_path = os.path.join(cur_dir,'dict/management.txt') # 管理人
        
        # 加载特征词
        self.fund_wds = [i.strip() for i in open(self.fund_path,encoding="utf-8") if i.strip()]
        self.manager_wds = [i.strip() for i in open(self.manager_path,encoding="utf-8") if i.strip()]
        self.management_wds = [i.strip() for i in open(self.management_path,encoding="utf-8") if i.strip()]
        
        self.region_words = set(self.fund_wds + self.manager_wds + self.management_wds)
        
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构造词典
        self.wdtype_dict = self.build_wdtype_dict() # 构造词类型
        
        # 问句疑问词
        ## 基金部分
        self.chinese_name_qwds = ['中文名是什么','叫什么名字','全称','简称','名字是','中文名']
        self.type_qwds = ['基金类型','什么类型','属于什么类','类型']
        self.fund_type_qwds = ['投资类型']
        self.benchmark_qwds = ['业绩标准','参照标准是',]
        self.issue_amount_qwds = ['发行了什么','发行份额','总额','总共发行','发行价值']
        self.m_fee_qwds = ['管理费','缴纳多少','付多少费用']
        self.min_amount_qwds = ['最小金额','起点金额','最少投资','至少','最少']
        ## 基金经理部分
        self.edu_qwds = ['学历','教育经历','学习',]
        self.gender_qwds = ['性别','是男','是女']
        self.resume_qwds = ['简历','管理成绩','行业经验','经验','是谁']
        self.birth_year_qwds = ['年龄','出生','生日']
        ## 三者关系部分
        self.manage_by_who_qwds = ['基金经理是谁','经理','被谁','由谁','哪个人管理','管理',]
        self.served_at_qwds = ['任职','受聘','聘用','雇佣','工作','上班']
        self.belong_to_qwds = ['属于哪个管理人','属于什么基金','有什么产品','产品']
        
        print("模型初始化完成！！！")
        return 
    
    def classify(self,question):
        data = {}
        cb_dict = self.check_cb(question)#调用下面定义的check_cb问句过滤函数
        if not cb_dict:
            return {}
        data['args'] = cb_dict
        # 获取问句中的实体类型
        types = []
        for type_ in cb_dict.values():
            types += type_
        question_type = 'others'  # 跟cb无关的问题类型
        
        question_types = []
        
        # 已知基金找基金经理，或者相反
        if self.check_words(self.manage_by_who_qwds,question) and ('fund' in types):
            #self.match_to_qwds来自于init，查找self.match_to_qwds是否在question内
            question_type = 'fund_manager'
            question_types.append(question_type)
        
        if self.check_words(self.manage_by_who_qwds,question) and ('manager' in types):
            question_type = 'manager_fund'
            question_types.append(question_type)
            
        # 已知基金找管理人，或者相反
        if self.check_words(self.belong_to_qwds,question) and ('fund' in types):
            #self.match_to_qwds来自于init，查找self.match_to_qwds是否在question内
            question_type = 'fund_management'
            question_types.append(question_type)
        
        if self.check_words(self.belong_to_qwds,question) and ('management' in types):
            question_type = 'management_fund'
            question_types.append(question_type)        
            
        # 已知基金经理找管理人，或者相反
        if self.check_words(self.served_at_qwds,question) and ('manager' in types):
            #self.match_to_qwds来自于init，查找self.match_to_qwds是否在question内
            question_type = 'manager_management'
            question_types.append(question_type)
        
        if self.check_words(self.served_at_qwds,question) and ('management' in types):
            question_type = 'management_manager'
            question_types.append(question_type)    
        
        # 基金中文名
        if self.check_words(self.chinese_name_qwds,question) and ('fund' in types):
            question_type = 'fund_chinese_name'
            question_types.append(question_type)
        # 基金类型
        if self.check_words(self.type_qwds,question) and ('fund' in types):
            question_type = 'fund_type'
            question_types.append(question_type)
        # 基金投资类型
        if self.check_words(self.fund_type_qwds,question) and ('fund' in types):
            question_type = 'fund_fund_type'
            question_types.append(question_type)    
        # 基金业绩标准
        if self.check_words(self.benchmark_qwds,question) and ('fund' in types):
            question_type = 'fund_benchmark'
            question_types.append(question_type)         
        # 基金发行总额
        if self.check_words(self.issue_amount_qwds,question) and ('fund' in types):
            question_type = 'fund_issue_amount'
            question_types.append(question_type)
        # 基金管理费
        if self.check_words(self.m_fee_qwds,question) and ('fund' in types):
            question_type = 'fund_m_fee'
            question_types.append(question_type)
        # 基金起点金额
        if self.check_words(self.min_amount_qwds,question) and ('fund' in types):
            question_type = 'fund_min_amount'
            question_types.append(question_type)
        
        # 基金经理学历
        if self.check_words(self.edu_qwds,question) and ('manager' in types):
            question_type = 'manager_edu'
            question_types.append(question_type)
        # 基金经理性别
        if self.check_words(self.gender_qwds,question) and ('manager' in types):
            question_type = 'manager_gender'
            question_types.append(question_type)
        # 基金经理简历
        if self.check_words(self.resume_qwds,question) and ('manager' in types):
            question_type = 'manager_resume'
            question_types.append(question_type)
        # 基金经理出生日期
        if self.check_words(self.birth_year_qwds,question) and ('manager' in types):
            question_type = 'manager_birth_year'
            question_types.append(question_type)
        
        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types
        return data
    
    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words: # 找到用户输入的词是什么范围的
            wd_dict[wd] = []
            if wd in self.fund_wds:
                wd_dict[wd].append('fund')
            if wd in self.manager_wds:
                wd_dict[wd].append('manager')
            if wd in self.management_wds:
                wd_dict[wd].append('management')
        return wd_dict
    
    '''构造actree，加速过滤'''
    def build_actree(self,wordlist):
        actree = ahocorasick.Automaton()  # 初始化
        for index,word in enumerate(wordlist):
            actree.add_word(word,(index,word))
        actree.make_automaton()
        return actree
    
    '''问句过滤'''
    def check_cb(self,question):
        region_wds = []
        for i in self.region_tree.iter(question): # ahocorasick库 匹配问题  iter返回一个元组
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1) 
        final_wds = [ i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}
        
        return final_dict
    
    
    '''基于特征词进行分类'''
    def check_words(self,wds,sent):
        for wd in wds:
            if wd in sent:
                return True
        return False
        

if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)
        
        
        