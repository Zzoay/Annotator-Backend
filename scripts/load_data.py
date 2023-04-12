"""
数据读取脚本
"""
import random
import json
from collections import defaultdict
from urllib import request
import requests  # type: ignore


def preproc_vocab():
    path_list = [r"E:\CSDS\val.json", r"E:\CSDS\test.json", r"E:\CSDS\train.json"]
    word_dct = defaultdict(int)
    for path in path_list:
        with open(path, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
            for d in data:
                for dialog in d.get('Dialogue'):
                    for word in dialog.get('utterance').split(' '):
                        if word != '':
                            word_dct[word] += 1
    
    out_file = r'E:\django_project\annotator\data\conv_dep\vocab.txt'
    with open(out_file, 'w+', encoding='utf-8') as fp:
        for word, count in sorted(word_dct.items(), key=lambda x:x[1], reverse=True):
            fp.write(f"{word} {count}\n")


def push_vocab():
    file = r'E:\django_project\annotator\data\conv_dep\vocab.txt'
    url = 'http://localhost:8000/api/word/'
    data_lst = []
    with open(file, 'r', encoding='utf-8') as fp:
        for i, line in enumerate(fp.readlines()):
            word, count = line.split(' ')
            if word in ['\xa0', '\x0b', '\u2006']:
                continue
            data_lst.append({'word': word})
            if (i + 1) % 2000 == 0 or word == '顶上':
                res = requests.post(url, json=data_lst)
                if res.status_code == 400:
                    print(data_lst)
                    res = requests.post(url, json=data_lst)
                    print(i, res.status_code)
                data_lst = []


def select_data():
    '''
    数据的选择规则：
        1. 轮次 6 ~ 16
        2. 单句长度 <= 20
        # 3. 词频 >= 3
        # 4. 单词长度 <= 4
        # 5. 训练集、验证集和测试集等比例采样
    '''
    split_lst = ['test']
    path_list = [f"E:/CSDS/{x}.json" for x in split_lst]
    word_dct = dict()
    with open(r'E:\django_project\annotator\data\conv_dep\vocab.txt', encoding='utf-8') as fp:
        for line in fp.readlines():
            word, count = line.split(' ')
            count = int(count.strip())
            word_dct[word] = count

    data_dct = {
        "train": [],
        "val": [],
        "test": [],
    }
    rejected = False
    for i, path in enumerate(path_list):
        with open(path, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
            for d in data:
                # 一个对话
                for turn, dialog in enumerate(d.get('Dialogue')):
                    # 一轮     
                    speaker = dialog.get('speaker')
                    utterance = dialog.get('utterance')
                    word_lst = utterance.split(' ')
                    word_lst = [word for word in word_lst if word != '']
                    # if len(word_lst) > 20:
                    #     rejected = True
                    #     break

                    # for word in word_lst:
                    #     if word_dct.get(word, 0) < 3:
                    #         rejected = True
                    #         break
                    
                # if rejected or (turn + 1) < 6 or (turn + 1) > 16:
                #     rejected = False
                #     continue

                data_dct[split_lst[i]].append(d)
                rejected = False
    
    # print('train:', len(data_dct['train']))
    # print('val:', len(data_dct['val']))
    print('test:', len(data_dct['test']))

    '''
    输出文件格式：
        id:
        dialog:
            turn:
            speaker:
            utterance:
            words: {index: int, word: word}
        relationship: {head_id: 'turn-index', tail_id: 'turn-index', relation_id: '', relation_name: ''}
    '''
    
    for key in data_dct.keys():
        out_dir = f"data/diag_dep/{key}.json"
        save_lst = []

        fp =  open(out_dir, 'w+', encoding='utf-8')
        for d in data_dct[key]:
            dialog_id = d.get('DialogueID')
            save_dct = {}
            save_dct['id'] = dialog_id
            save_dct['dialog'] = []
            save_dct['relationship'] = []

            for turn, dialog in enumerate(d.get('Dialogue')):
                speaker = dialog.get('speaker')
                utterance = dialog.get('utterance')
                save_dct['dialog'].append({
                    'turn': turn,
                    'speaker': speaker,
                    'utterance': utterance,
                    'words': []
                })

                for word_idx, word in enumerate(utterance.split(' ')):
                    if word == '':
                        continue
                    save_dct['dialog'][turn]['words'].append({
                        'index': word_idx + 1,
                        'word': word
                    })
            save_lst.append(save_dct)
        save_str = json.dumps(save_lst, ensure_ascii=False, indent=4, separators=(',', ': '))
        fp.write(save_str)
        fp.close()

def preproc_data():
    replace_dct = {
        "点前": "点 前", "点后": "点 后", "取货": "取 货", "收货": "收 货", "送货": "送 货", "下单": "下 单", "取件": "取 件 ", "收件": "收 件 ", "送件": "送 件 ", "寄件": "寄 件", 
        "工作日内": "工作日 内", "急需": "急 需", "售后服务": "售后 服务", "拒收": "拒 收", "拒签": "拒 签", "退货": "退 货", "退款": "退 款", "退换货": "退换 货", "退换": "退 换",
        # "有没有": "有 没 有", "能不能": "能 不 能", "能否": "能 否", "可不可以": "可 不 可以", "可以 不 可以": "可以 不 可以", "是不是": "是 不 是", "用不用": "用 不 用",
        "了": " 了 ", "我": " 我 ", "你": " 你 ", "您": " 您 ", "他": " 他 ", "她": " 她 ", "它": " 它 ", "这": " 这 ", "这 样": " 这样 ", "这 么": "这么", 
        "不": " 不 ", "货": " 货 ", "退": " 退 ", "换": " 换 ", "没": " 没 ", "新": " 新 ", "旧": " 旧 ", "买": " 买 ", "卖": " 卖 ", "别": " 别 ", "有": " 有 ",
        "给": " 给 ", "开": " 开 ", "关": " 关 ", "上门": "上 门", "商品信息": "商品 信息", "还有": "还 有", "还能": "还 能", "还可": "还 可", 
        "[ 订单": "订单", "先为": "先 为", "原返": "原 返", "晒图": "晒 图", "返现": "返 现",  "接听电话": "接听 电话", "付款": "付 款", "购 买": " 购买", "延期": "延 期",
        "对妹 纸": "对 妹纸", "打电话": "打 电话", "送到": "送到", "到货": "到 货", "晚上": " 晚上 ", "中午": " 中午 ", "下午": " 下午 ","早上": " 早上 ", "会为": " 会 为",
        "早就": "早 就", "早些": "早 些", "早起": "早 起", "早晚": "早 晚", "稍等": "稍 等 ", "久等": "久 等", "是否": "是 否 ", "以旧": "以 旧", "寄出": "寄 出",
        "~ ~ ~ O ( ∩ _ ∩ ) O / ~": " ", "^ _ ^": " ", "[姓名] [姓名] 康康": "健健康康", "身体健康": "身体 健康", "阖家幸福": "阖家 幸福", "生意兴隆": "生意 兴隆",
        "多喝水": "多 喝 水", "添麻烦": "添 麻烦", "来电显示": "来电 显示", "张卡": "张 卡", "定位": "定 位", "啥意思": "啥 意思", "为准": "为 准", "才能": "才 能", "才可以": "才 可以",
        "开 始": "开始", "# E - s [电话] [数字]": "[数字]", "保价": "保 价", "升价": "升 价", "涨价": "涨 价", "降价": "降 价", "解决问题": "解决 问题", "送达": "送 达",
        "聊天 框中": "聊天框 中", "单点": "单 点", "开 具": "开具", "有点": "有 点", "# E - b ": "", "周 到": "周到", "亲是": "亲 是", "联系方式": "联系 方式", 
        "联系电话": "联系 电话", "算错": "算 错", "下线": "下 线", "有个": "有 个", "选错": "选 错", "点错": "点 错", "好意思": "好 意思",
        "收获": "收 货", "货 物": "货物", "怎么弄": "怎么 弄", "有些": "有 些", "保修": "保 修", "从 新": "重新", "留个": "留 个", "发邮件": "发 邮件", "[组织 机构]": "[组织机构]",
        "多长时间": "多长 时间", "比价": "比 价", "开 心": "开心", "分 开": "分开", "分内之事": "分内 之 事", "财务咨询": "财务 咨询", "这 么久": "这么 久", "这 边": "这边",
        "错": " 错 ", "错 误": "错误", "怎么回事": "怎么 回事", "相 关": "相关", "返修": "返 修", "一下": "一 下", "寄回": "寄 回", "只能": "只 能", " 们": "们", "第 ": "第",
        "打个": "打 个", "出库": "出 库", "之处": "之 处", "是从": "是 从", "能取消": "能 取消", "重 新": "重新", "[组织 机构 [ 组织 机构]": "组织 机构 [组织机构]", "更 换": "更换",
        "其 他": "其他", "进线": "进 线", "在 次": "再次", "收费": "收 费", "无理由": "无 理由", "还款": "还 款", "了 解": "了解", " 相 关": "相关", "明 细": "明细", "类 别": "类 别",
        "先发": "先 发", "打款": "打 款", "再次日": "在 次日", "前会": "前 会", "放在": "放 在", "关 注": "关注", "客户服务": "客户 服务", "到 底": "到底", "特 别": "特别", "不 过": "不过",
        "海 关": "海关", "开 始": "开始", "级 别": "级别", "还有": "还有", "收取 件 费": "收 取件 费"
    }
    # 手工部分： USER_ID  => 用户编号
    split_lst = ['train', 'test', 'val']
    for key in split_lst:
        file = f"data/raw/{key}.json"
        out_file = f"data/raw/{key}_proc.json"
        save_lst = []

        fp = open(file, 'r', encoding='utf-8')
        fw = open(out_file, 'w', encoding='utf-8')
        data = json.load(fp)

        for d in data:
            save_dct = {}
            save_dct['id'] = d.get('DialogueID')
            save_dct['dialog'] = []
            save_dct['relationship'] = []

            for turn, dialog in enumerate(d.get('Dialogue')):
                speaker = dialog.get('speaker')
                utterance = dialog.get('utterance')

                # process
                if 'http' in utterance:
                    utterance = '[链接]'

                for key, value in replace_dct.items():
                    utterance = utterance.replace(key, value)

                save_dct['dialog'].append({
                    'turn': turn,
                    'speaker': speaker,
                    'utterance': utterance,
                    # 'words': []
                })

                word_idx, word_lst = 0, [] 
                for word in utterance.split(' '):
                    if word in ['', ' ', '\t', '\xa0', '\x0b', '\u2006']:
                        continue
                    # save_dct['dialog'][turn]['words'].append({
                    #     'index': word_idx + 1,
                    #     'word': word
                    # })
                    word_lst.append(word)
                    word_idx += 1
                
                save_dct['dialog'][turn]['utterance'] = ' '.join(word_lst)
            
            save_lst.append(save_dct)
        
        save_str = json.dumps(save_lst, ensure_ascii=False, indent=4, separators=(',', ': '))
        fw.write(save_str)
        fp.close()
        fw.close()

def push_data():
    conv_lst, uttr_lst = [], []
    conv_cnt = 851
    file = f'data/diag_dep/pre_annot/annoted_train_50.json'
    fp = open(file, 'r', encoding='utf-8')
    data = json.load(fp)

    for i, d in enumerate(data):
        conv_lst.append({
            'conv_id': conv_cnt,
            'set': 'train',
        })

        for turn, dialog in enumerate(d.get('dialog')):
            speaker = dialog.get('speaker')
            # requests.post(uttr_url, data={
            #     'conv_id': i+1,
            #     'uttr_id': turn,
            #     'word_id': 0,
            #     'word': speaker,
            # })

            # 添加 root
            uttr_lst.append({
                'conv': conv_cnt,
                'utr_id': turn,
                'word_id': 0,
                'word': 'ROOT',
            })

            uttr_lst.append({
                'conv': conv_cnt,
                'utr_id': turn,
                'word_id': 1,
                'word': speaker,
            })

            utterance = dialog.get('utterance')
            word_idx = 2 
            for word in utterance.split(' '):
                if word in ['', '\xa0', '\x0b', '\u2006']:
                    continue
                # requests.post(uttr_url, data={
                #     'conv_id': i+1,
                #     'uttr_id': turn,
                #     'word_id': word_idx,
                #     'word': word,
                # })
                uttr_lst.append({
                    'conv': conv_cnt,
                    'utr_id': turn,
                    'word_id': word_idx,
                    'word': word,
                })
                word_idx += 1
        conv_cnt += 1

    # push到conv表
    conv_url = 'http://localhost:8000/api/conv/'
    res = requests.post(conv_url, json=conv_lst)

    # push到utterance表
    uttr_url = 'http://localhost:8000/api/conv_dep/'
    # res = requests.post(uttr_url, json=uttr_lst)
    start, end = 0, 4000
    while end < len(uttr_lst):
        res = requests.post(uttr_url, json=uttr_lst[start:end])

        start += 4000
        end += 4000
        if end > len(uttr_url):
            res = requests.post(uttr_url, json=uttr_lst[start:])
        
        if res.status_code == 400:
            print(uttr_lst[start:end])
            res = requests.post(uttr_url, json=uttr_lst[start:end])
            print(i, res.status_code)
    return


def push_rels():
    rel_dct = {
        'Root': '根节点',
        'AGT': '施事',
        'EXP': '当事',
        'PAT': '受事',
        'CONT': '客事',
        'DATV': '涉事',
        'LINK': '系事',
        'FEAT': '修饰',
        'LOC': '空间',
        'MANN': '方式',
        'MATL': '材料',
        'MEAS': '度量',
        'REAS': '缘由',
        'SCO': '范围',
        'STAT': '状态',
        'TIME': '时间',
        'TOOL': '工具',
        'dAGT': 'd-施事',
        'dEXP': 'd-当事',
        'dPAT': 'd-受事',
        'dCONT': 'd-客事',
        'dDATV': 'd-涉事',
        'dLINK': 'd-系事',
        'dFEAT': 'd-修饰',
        'dLOC': 'd-空间',
        'dMANN': 'd-方式',
        'dMATL': 'd-材料',
        'dMEAS': 'd-度量',
        'dREAS': 'd-缘由',
        'dSCO': 'd-范围',
        'dSTAT': 'd-状态',
        'dTIME': 'd-时间',
        'dTOOL': 'd-工具',
        'rAGT': 'r-施事',
        'rEXP': 'r-当事',
        'rPAT': 'r-受事',
        'rCONT': 'r-客事',
        'rDATV': 'r-涉事',
        'rLINK': 'r-系事',
        'rFEAT': 'r-修饰',
        'rLOC': 'r-空间',
        'rMANN': 'r-方式',
        'rMATL': 'r-材料',
        'rMEAS': 'r-度量',
        'rREAS': 'r-缘由',
        'rSCO': 'r-范围',
        'rSTAT': 'r-状态',
        'rTIME': 'r-时间',
        'rTOOL': 'r-工具',
        'mPUNC': '标点',
        'mNEG': '否定',
        'mRELA': '关系',
        'mDEPD': '依附',
        'eCOO': '并列',
        'ePREC': '先行',
        'eSUCC': '后继',
        'EXPL': '解说',
        'REF': '共指'
    }

    rel_dct = {
        'root': '根节点',
        'sasubj-obj': '同主同宾',
        'sasubj': '同主语',
        'dfsubj': '不同主语',
        'subj': '主语',
        'subj-in': '内部主语',
        'obj': '宾语',
        'pred': '谓语',
        'att': '定语',
        'adv': '状语',
        'cmp': '补语',
        'coo': '并列',
        'pobj': '介宾',
        'iobj': '间宾',
        'de': '的',
        'adjct': '附加',
        'app': '称呼',
        'exp': '解释',
        'punc': '标点',
        'frag': '片段',
        'repet': '重复',
    }

    rel_dct = {
        'attr': '归属',
        'bckg': '背景',
        'cause': '因果',
        'comp': '比较',
        'cond': '状况',
        'cont': '对比',
        'elbr': '阐述',
        'enbm': '目的',
        'eval': '评价',
        'expl': '解释-例证',
        'joint': '联合',
        'manner': '方式',
        'rstm': '重申',
        'temp': '时序',
        'tp-change': '主题变更',
        'prob-sol': '问题-解决',
        'qst-ans': '疑问-回答',
        'stm-rsp': '陈述-回应',
        'req-proc': '需求-处理',
    }

    for i, (key, value) in enumerate(rel_dct.items()):
        color = ''.join([random.choice('0123456789ABCDEF') for j in range(6)])

        form = {
            "tag": key,
            "name": value,
            "color": color
        }

        # push到relation表
        rel_url = 'http://localhost:8000/api/relation/'
        res = requests.post(rel_url, json=form)  


def push_relationship():
    # 获得relation表
    rel_url = 'http://localhost:8000/api/relation/'
    res = requests.get(rel_url)
    rel_lst = json.loads(res.text)["results"]

    tag2id = {}
    for item in rel_lst:
        rel_id, tag, name = item['id'], item['tag'], item['name']
        tag2id[tag] = rel_id

    relship_url = 'http://localhost:8000/api/relationship/'

    # 读取数据
    split_lst = ['test']
    conv_cnt = 851
    for key in split_lst:
        # file = f"data/diag_dep/pre_annot/annoted_by_1to500.json"
        file = f'data/diag_dep/pre_annot/annoted_train_50.json'
        fp = open(file, 'r', encoding='utf-8')
        data = json.load(fp)
        fp.close()

        for i, d in enumerate(data):

            push_lst = []
            for tri in d['relationship']:
                head_uttr_id, head_word_idx = tri[0].split('-')
                tail_uttr_id, tail_word_idx = tri[2].split('-')

                # 考虑话语者在1的位置，往右移动1
                if int(head_word_idx) > 0:
                    head_word_idx = str(int(head_word_idx) + 1)
                if int(tail_word_idx) > 0:
                    tail_word_idx = str(int(tail_word_idx) + 1)

                push_lst.append({
                    'conv': conv_cnt,
                    'head': f'{head_uttr_id}-{head_word_idx}',
                    'relation': tag2id[tri[1]],
                    'tail': f'{tail_uttr_id}-{tail_word_idx}'
                })
            
            res = requests.post(relship_url, json=push_lst)
            
            conv_cnt += 1


def fix_seg(false_seg):
    for convId in range(851, 901):
        # get words
        conv_url = 'http://localhost:8000/api/conv_dep/'
        res = requests.get(conv_url, {'convId': convId})
        uttrs = res.json()

        # get relships
        relship_url = 'http://localhost:8000/api/relationship/'
        res = requests.get(relship_url, {'convId': convId})
        rels = res.json()

        for uttr_id, uttr in enumerate(uttrs):
            word_lst = []
            word_segs = false_seg.split(' ')
            seg_len = len(word_segs)
            cnt = 0
            for item in uttr['items']:
                word_idx, word = item['id'], item['word']
                if word == word_segs[cnt]:
                    cnt += 1
                else:
                    cnt = 0
                # 匹配
                if cnt == seg_len:
                    cnt = 0
                    start = word_idx - seg_len
                    curr = f'{uttr_id}-{word_idx}'
                    for i, rel in enumerate(rels):
                        tmp = rel.copy()
                        head_uttr_idx, head_word_idx = [int(x) for x in rel['head'].split('-')]
                        tail_uttr_idx, tail_word_idx = [int(x) for x in rel['tail'].split('-')]
                        # 同一话语
                        if (head_uttr_idx == uttr_id or tail_uttr_idx == uttr_id):
                            if head_word_idx > start:
                                tmp['head'] = f'{head_uttr_idx}-{str(head_word_idx - seg_len + 1)}'  
                            if tail_word_idx > start:
                                tmp['tail'] = f'{tail_uttr_idx}-{str(tail_word_idx - seg_len + 1)}' 
                            print(rels[i]) 
                            print(tmp)
                            
                            # 更新关系
                            # if convId != 22:
                            res = requests.put(f"{relship_url}{tmp['id']}/", tmp)
                            print(res)
                        
                        rels[i] = tmp


def save2json():
    rel_dct = {
        'root': '根节点',
        'sasubj-obj': '同主同宾',
        'sasubj': '同主语',
        'dfsubj': '不同主语',
        'subj': '主语',
        'subj-in': '内部主语',
        'obj': '宾语',
        'pred': '谓语',
        'att': '定语',
        'adv': '状语',
        'cmp': '补语',
        'coo': '并列',
        'pobj': '介宾',
        'iobj': '间宾',
        'de': '的',
        'adjct': '附加',
        'app': '称呼',
        'exp': '解释',
        'punc': '标点',
        'frag': '片段',
        'repet': '重复',
        # rst
        'attr': '归属',
        'bckg': '背景',
        'cause': '因果',
        'comp': '比较',
        'cond': '状况',
        'cont': '对比',
        'elbr': '阐述',
        'enbm': '目的',
        'eval': '评价',
        'expl': '解释-例证',
        'joint': '联合',
        'manner': '方式',
        'rstm': '重申',
        'temp': '时序',
        'tp-chg': '主题变更',
        'prob-sol': '问题-解决',
        'qst-ans': '疑问-回答',
        'stm-rsp': '陈述-回应',
        'req-proc': '需求-处理',
    }
    rel_lst = [k for k in rel_dct.keys()]
    
    proc_file = f"data/diag_dep/pre_annot/annoted_by_1to500.json"
    fp = open(proc_file, 'r', encoding='utf-8')
    data = json.load(fp)
    fp.close()
    for convId in range(1, 801):
        # get words
        conv_url = 'http://localhost:8000/api/conv_dep/'
        res = requests.get(conv_url, {'convId': convId})
        uttrs = res.json()

        # get relships
        relship_url = 'http://localhost:8000/api/relationship/'
        res = requests.get(relship_url, {'convId': convId})

        tmp = []
        for r in res.json():
            tail = r['tail']
            if int(tail.split('-')[1]) > 0:
                tail = '-'.join([str(tail.split('-')[0]), str(int(tail.split('-')[1]) - 1)])
            head = r['head']
            if int(head.split('-')[1]) > 0:
                head = '-'.join([str(head.split('-')[0]), str(int(head.split('-')[1]) - 1)])
            trip = [head, rel_lst[r['relation']-1], tail]
            tmp.append(trip)

        data[convId - 1]['relationship'] = list(sorted(tmp))
    
    out_file = f"data/diag_dep/annoted/1to800_1126.json"
    fw = open(out_file, 'w', encoding='utf-8')
    save_str = json.dumps(data, ensure_ascii=False, indent=2, separators=(',', ': '))
    fw.write(save_str)
    fw.close()


def merge():
    first_file = 'data/diag_dep/annoted/1to101_0912.json'
    second_file = 'data/diag_dep/pre_annot/test.json'
    with open(first_file, 'r', encoding='utf-8') as f:
        first = json.load(f)
    with open(second_file, 'r', encoding='utf-8') as f:
        second = json.load(f)  
    
    merge = list()
    bound = 101
    for i in range(bound):
        merge.append(first[i])
    for i in range(bound, len(second)):
        uni_rel = set([str(x) for x in second[i]['relationship']])
        second[i]['relationship'] = list([eval(x) for x in uni_rel])
        merge.append(second[i])
    
    with open('data/diag_dep/annoted/merge.json', 'w', encoding='utf-8') as f:
        save_str = json.dumps(merge, ensure_ascii=False, indent=2, separators=(',', ': '))
        f.write(save_str)
    

def uni_same():
    in_file = 'data/diag_dep/annoted/merge.json'
    with open(in_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 例句, 所在话语
    same2data = {
        "请问 您 是 咨询 之前 的 问题 还是 有 其他 的 问题 需要 处理 呢 ?": data[81],
        "请问 还 有 其他 可以 帮 您 的 吗": data[81],
        "有 什么 问题 我 可以 帮 您 处理 或 解决 呢 ?": data[82],
        "请问 还 有 其他 还 可以 帮到 您 的 吗 ?": data[82],
        "感谢 您 对 京东 的 支持 ， 祝 您 生活 愉快 ， 再见": data[82],
        "感谢 您 对 京东 的 支持 ， 祝 您 购物 愉快 ， 再见": data[89],
        "感谢 您 对 京东 的 支持 ， 祝 您 生活 愉快 ， 再见 !": data[90],
        "请问 还 有 其他 我 可以 为 您 效劳 的 么 ?": data[93],
        "别 忘 了 对 妹纸 的 服务 做出 评价 哦 谢谢 您 啦 么么哒": data[93],
        "还 辛苦 您 给 小妹 的 服务 打 个 评价 呢 ~ 点击 表情 栏 旁边 的 “ + ” 哦 ， 谢谢 您 啦 ~ 么么哒": data[96],
        "您 好 ， 请问 有 什么 可以 帮 您 的 呢 ?": data[97],
        "请问 还 有 什么 可以 帮 您 的 吗 ?": data[98],
        "遇到 像 您 这样 善解人意 的 客户 ， 真是 我们 莫大 的 荣幸 呢 ~": data[99],
        "还 辛苦 您 给 小妹 打 个 评价 呢 ~ 点击 表情 栏 旁边 的 “ + ” 哦 。": data[99],
    }
    # 例句，对应关系
    same_dct = {}
    for s, d in same2data.items():
        rels = d['relationship']
        for item in d['dialog']:
            if item['utterance'] == s:
                turn = item['turn']
                same_dct[s] = [x for x in rels if x[0].split('-')[0] == str(turn)]

    s_lst = []
    for diag_idx, d in enumerate(data):
        dialog = d['dialog'].copy()
        rels = d['relationship'].copy()
        for uttr_idx, item in enumerate(dialog):
            if item['utterance'] in same_dct.keys():
                # delete original relationships
                for rel in rels:
                    if rel[0].split('-')[0] == str(uttr_idx) and rel[0].split('-')[0] == rel[2].split('-')[0]:
                        d['relationship'].remove(rel)
                for new_rel in same_dct[item['utterance']]:
                    # different utterance
                    if new_rel[0].split('-')[0] != new_rel[2].split('-')[0]:
                        continue
                    head = f"{uttr_idx}-{new_rel[0].split('-')[1]}"
                    tail = f"{uttr_idx}-{new_rel[2].split('-')[1]}"
                    d['relationship'].append([head, new_rel[1], tail])
        s_lst.append(json.dumps(d, ensure_ascii=False))
    
    new = []
    for s in s_lst:
        new.append(json.loads(s))

    out_file = 'data/diag_dep/annoted/test_new_0912.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        save_str = json.dumps(new, ensure_ascii=False, indent=2, separators=(',', ': '))
        f.write(save_str)


def del_relships(conv_id):
    data = requests.get(f"http://localhost:8000/api/relationship/?convId={conv_id}")
    for item in data.json():
        rel_id = item['id']
        res = requests.delete(f"http://localhost:8000/api/relationship/{rel_id}")


def shift_root():
    for conv_id in range(1, 84):
        data = requests.get(f"http://localhost:8000/api/relationship/?convId={conv_id}")
        root_item_dct = {}
        for item in data.json():
            head_uttr_idx, head_word_idx = [int(x) for x in item['head'].split('-')]
            tail_uttr_idx, tail_word_idx = [int(x) for x in item['tail'].split('-')]
            # root
            if head_word_idx == 0 and head_uttr_idx == tail_uttr_idx:
                root_item_dct[head_uttr_idx] = tail_word_idx
        for item in data.json():
            head_uttr_idx, head_word_idx = [int(x) for x in item['head'].split('-')]
            tail_uttr_idx, tail_word_idx = [int(x) for x in item['tail'].split('-')]
            if head_uttr_idx != tail_uttr_idx and head_word_idx + tail_word_idx == 0:
                new = item.copy()
                new['head'] = f'{head_uttr_idx}-{root_item_dct[head_uttr_idx]}'
                new['tail'] = f'{tail_uttr_idx}-{root_item_dct[tail_uttr_idx]}'
                res = requests.put(f"http://localhost:8000/api/relationship/{item['id']}/", new)


def fix_annot_bug():
    for conv_id in range(851, 901):
        relationship = requests.get(f"http://localhost:8000/api/relationship/?convId={conv_id}").json()
        dialog = requests.get(f"http://localhost:8000/api/conv_dep/?convId={conv_id}").json()
        max_len_dct = {}
        for i, uttr in enumerate(dialog):
            max_len = len(uttr['items'])
            max_len_dct[i] = max_len
        for item in relationship:
            head_uttr_idx, head_word_idx = [int(x) for x in item['head'].split('-')]
            tail_uttr_idx, tail_word_idx = [int(x) for x in item['tail'].split('-')]
            if head_uttr_idx != tail_uttr_idx:
                continue
            if head_word_idx >= max_len_dct[head_uttr_idx] or tail_word_idx >= max_len_dct[head_uttr_idx]:
                print(item)
                res = requests.delete(f"http://localhost:8000/api/relationship/{item['id']}")


def uni_same_one(conv_id):
    relationship = requests.get(f"http://localhost:8000/api/relationship/?convId={conv_id}").json()
    source_uttr_idx, target_uttr_idx = 1, 4
    for item in relationship:
        head_uttr_idx, head_word_idx = [int(x) for x in item['head'].split('-')]
        tail_uttr_idx, tail_word_idx = [int(x) for x in item['tail'].split('-')]
        if head_uttr_idx == source_uttr_idx:
            res = requests.post(f"http://localhost:8000/api/relationship/", {
                'head': f'{target_uttr_idx}-{head_word_idx}',
                'tail': f'{target_uttr_idx}-{tail_word_idx}',
                'conv': item['conv'],
                'relation': item['relation']
            })
            pass


def reverse_attribution():
    rst_dct = {
        'attr': '归属',
        'bckg': '背景',
        'cause': '因果',
        'comp': '比较',
        'cond': '状况',
        'cont': '对比',
        'elbr': '阐述',
        'enbm': '目的',
        'eval': '评价',
        'expl': '解释-例证',
        'joint': '联合',
        'manner': '方式',
        'rstm': '重申',
        'temp': '时序',
        'tp-chg': '主题变更',
        'prob-sol': '问题-解决',
        'qst-ans': '疑问-回答',
        'stm-rsp': '陈述-回应',
        'req-proc': '需求-处理',
    }
    data_file = 'data/diag_dep/annoted/1to800_1126.json'
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for i, d in enumerate(data):
        relships = []
        old2new = {}
        for tri in d['relationship']:
            rel = tri[1]
            head_uttr_id, head_word_idx = tri[0].split('-')
            tail_uttr_id, tail_word_idx = tri[2].split('-')
            new_head = tri[0]
            new_rel = tri

            if rel == 'attr':
                new_rel = [tri[2], tri[1], tri[0]]  # reverse
                # find head
                for ftri in d['relationship']:
                    frel = ftri[1]
                    fhead_uttr_id, fhead_word_idx = ftri[0].split('-')
                    ftail_uttr_id, ftail_word_idx = ftri[2].split('-')
                    if head_uttr_id == ftail_uttr_id and head_word_idx == ftail_word_idx:
                        fhead = f'{fhead_uttr_id}-{fhead_word_idx}'
                        ftail = f'{tail_uttr_id}-{tail_word_idx}'
                        old2new[' '.join(ftri)] = [fhead, frel, ftail]
                    elif head_uttr_id == fhead_uttr_id and head_word_idx == fhead_word_idx and frel in rst_dct.keys():
                        fhead = f'{tail_uttr_id}-{tail_word_idx}'  # tail becomes head
                        ftail = f'{ftail_uttr_id}-{ftail_word_idx}'
                        old2new[' '.join(ftri)] = [fhead, frel, ftail]
            # if new_rel[2] not in [x[2] for x in relships]:
            relships.append(new_rel)

        news = []
        for tri in relships:
            if ' '.join(tri) in old2new.keys():
                tri = old2new[' '.join(tri)]
            news.append(tri)

        d['relationship'] = news

    with open('output.json', 'w', encoding='utf-8') as f:
        save_str = json.dumps(data, ensure_ascii=False, indent=2, separators=(',', ': '))
        f.write(save_str)


if __name__ == '__main__':
    # fix_seg(false_seg='没 有')
    # save2json()
    # merge()
    # uni_same()

    # push_data()
    # push_rels()
    # push_relationship()

    # del_relships()
    # shift_root()
    # fix_annot_bug()

    # uni_same_one(102)

    # del_relships(376)

    # preproc_data()

    reverse_attribution()
    
    pass