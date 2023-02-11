import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # 特征词路径
        self.ts_path = os.path.join(cur_dir,'dict/ts.txt') # 转债代码
        self.stk_path = os.path.join(cur_dir,'dict/stk.txt') # 正股代码
        
        # 加载特征词
        self.ts_wds = [i.strip() for i in open(self.ts_path,encoding="utf-8") if i.strip()]
        self.stk_wds = [i.strip() for i in open(self.stk_path,encoding="utf-8") if i.strip()]
        self.region_words = set(self.ts_wds + self.stk_wds)
        
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
        
        
        