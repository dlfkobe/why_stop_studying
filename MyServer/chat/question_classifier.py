import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        # cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        # 特征词路径
        self.ts_path = os.path.join(cur_dir,'dict/ts.txt') # 转债代码
        self.stk_path = os.path.join(cur_dir,'dict/stk.txt') # 正股代码
        
        # 基金特征词路径
        self.fund_path = os.path.join(cur_dir,'dict/fund.txt') # 基金代码
        self.manager_path = os.path.join(cur_dir,'dict/manager.txt') # 基金经理名字
        self.management_path = os.path.join(cur_dir,'dict/management.txt') # 管理人
        
        # 加载特征词
        self.ts_wds = [i.strip() for i in open(self.ts_path,encoding="utf-8") if i.strip()]
        self.stk_wds = [i.strip() for i in open(self.stk_path,encoding="utf-8") if i.strip()]
        # i基金加载特征词
        self.fund_wds = [i.strip() for i in open(self.fund_path,encoding="utf-8") if i.strip()]
        self.manager_wds = [i.strip() for i in open(self.manager_path,encoding="utf-8") if i.strip()]
        self.management_wds = [i.strip() for i in open(self.management_path,encoding="utf-8") if i.strip()]
        
        self.region_words = set(self.ts_wds + self.stk_wds + self.fund_wds + self.manager_wds + self.management_wds)
        
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构造词典
        self.wdtype_dict = self.build_wdtype_dict() # 构造词类型
        
        # 问句疑问词
        self.list_date_qwds = ['多久上市','什么时候上市','上市时间是多久','上市时间']
        self.par_qwds = ['面值','单张价格是','一张值多少钱']
        self.issue_size_qwds = ['发行总额是','共发行了多少','总共发行了多少','合计发行价值']
        self.bond_full_name_qwds = ['完整名字','详细版','中文全称','全称']
        self.bond_short_name_qwds = ['简称','简略版','中文缩写','中文名','中文']
        self.pay_per_year_qwds = ['年付息次数','利息次数','交多少次利息','一年付息几次','付多少次利息','一年','每年']
        self.value_date_qwds = ['起息日期','多久开始计息','什么时候起息']
        self.maturity_date_qwds = ['到息日期','多久到息','什么时候到息']
        self.exchange_qwds = ['上市地点','在哪里上市','什么地方上市']
        self.match_to_qwds = ['对应正股','对应','属于哪个正股','正股','对应转债股','转债股']
        ## 基金部分
        self.chinese_name_qwds = ['中文名是什么','叫什么名字','全称','简称','名字是','中文名']
        self.type_qwds = ['基金类型','什么类型','属于什么类','类型']
        self.fund_type_qwds = ['投资类型']
        self.benchmark_qwds = ['业绩标准','参照标准是',]
        self.issue_amount_qwds = ['发行了什么','发行份额','总额','总共发行','发行价值']
        self.m_fee_qwds = ['管理费','缴纳多少','付多少费用']
        self.min_amount_qwds = ['最小金额','起点金额','最少投资','至少','最少','最小']
        ## 基金经理部分
        self.edu_qwds = ['学历','教育经历','学习','教育']
        self.gender_qwds = ['性别','是男','是女']
        self.resume_qwds = ['简历','管理成绩','行业经验','经验','是谁']
        self.birth_year_qwds = ['年龄','出生','生日']
        ## 三者关系部分
        self.manage_by_who_qwds = ['基金经理是谁','经理','被谁','由谁','哪个人管理','管理',]
        self.served_at_qwds = ['任职','受聘','聘用','雇佣','工作','上班']
        self.belong_to_qwds = ['属于哪个管理人','属于什么基金','有什么产品','产品','属于']
        
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
        question_type = 'others'  # 跟债券基金无关的问题类型
        
        question_types = []
        
        # 已知转债找对应正股，或者相反
        if self.check_words(self.match_to_qwds,question) and ('ts' in types):
            #self.match_to_qwds来自于init，查找self.match_to_qwds是否在question内
            question_type = 'ts_stk'
            question_types.append(question_type)
        
        if self.check_words(self.match_to_qwds,question) and ('stk' in types):
            question_type = 'stk_ts'
            question_types.append(question_type)
        
        # 上市日期、
        if self.check_words(self.list_date_qwds,question) and ('ts' in types):
            question_type = 'ts_list_date'
            question_types.append(question_type)
            
        # 面值
        if self.check_words(self.par_qwds,question) and ('ts' in types):
            question_type = 'ts_par'
            question_types.append(question_type)
        
        # 发行总额
        if self.check_words(self.issue_size_qwds,question) and ('ts' in types):
            question_type = 'ts_issue_size'
            question_types.append(question_type)
            
        # 全称
        if self.check_words(self.bond_full_name_qwds,question) and ('ts' in types):
            question_type = 'ts_bond_full_name'
            question_types.append(question_type)
            
        # 简称
        if self.check_words(self.bond_short_name_qwds,question) and ('ts' in types):
            question_type = 'ts_bond_short_name'
            question_types.append(question_type)
        
        # 年付息次数
        if self.check_words(self.pay_per_year_qwds,question) and ('ts' in types):
            question_type = 'ts_pay_per_year'
            question_types.append(question_type)
            
        # 起息日期
        if self.check_words(self.value_date_qwds,question) and ('ts' in types):
            question_type = 'ts_value_date'
            question_types.append(question_type)
        
        # 到期日期
        if self.check_words(self.maturity_date_qwds,question) and ('ts' in types):
            question_type = 'ts_maturity_date'
            question_types.append(question_type)
            
        # 上市地点
        if self.check_words(self.exchange_qwds,question) and ('ts' in types):
            question_type = 'ts_exchange'
            question_types.append(question_type)
            
        # 基金部分
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
            if wd in self.ts_wds:
                wd_dict[wd].append('ts')
            if wd in self.stk_wds:
                wd_dict[wd].append('stk')
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
                    stop_wds.append(wd1) # stop_wds取重复的短的词，如region_wds=['乙肝', '肝硬化', '硬化']，则stop_wds=['硬化']
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
        
        
        