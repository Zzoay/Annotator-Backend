"""
数据读取脚本
"""
import os
import sys
import json
from collections import defaultdict
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
    split_lst = ['train', 'val', 'test']
    path_list = [r"E:\CSDS\train.json", r"E:\CSDS\val.json", r"E:\CSDS\test.json"]
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
                    if len(word_lst) > 20:
                        rejected = True
                        break

                    # for word in word_lst:
                    #     if word_dct.get(word, 0) < 3:
                    #         rejected = True
                    #         break
                    
                if rejected or (turn + 1) < 6 or (turn + 1) > 16:
                    rejected = False
                    continue

                data_dct[split_lst[i]].append(d)
                rejected = False
    
    print('train:', len(data_dct['train']))
    print('val:', len(data_dct['val']))
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
        out_dir = f"E:/django_project/annotator/data/conv_dep/pre_sample/{key}.json"
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
    split_lst = ['train', 'val', 'test']
    for key in split_lst:
        file = f"E:/django_project/annotator/data/conv_dep/pre_process/{key}.json"
        out_file = f"E:/django_project/annotator/data/conv_dep/pre_process1/{key}.json"
        save_lst = []

        fp = open(file, 'r', encoding='utf-8')
        fw = open(out_file, 'w', encoding='utf-8')
        data = json.load(fp)

        for d in data:
            save_dct = {}
            save_dct['id'] = d.get('id')
            save_dct['dialog'] = []
            save_dct['relationship'] = []

            for turn, dialog in enumerate(d.get('dialog')):
                speaker = dialog.get('speaker')
                utterance = dialog.get('utterance')

                # process
                if 'http' in utterance:
                    utterance = '[链接]'

                save_dct['dialog'].append({
                    'turn': turn,
                    'speaker': speaker,
                    'utterance': utterance,
                    'words': []
                })

                word_idx = 0 
                for word in utterance.split(' '):
                    if word == '':
                        continue
                    save_dct['dialog'][turn]['words'].append({
                        'index': word_idx + 1,
                        'word': word
                    })
                    word_idx += 1
            
            save_lst.append(save_dct)
        
        save_str = json.dumps(save_lst, ensure_ascii=False, indent=4, separators=(',', ': '))
        fw.write(save_str)
        fp.close()
        fw.close()

def push_data():
    split_lst = ['train', 'val', 'test']

    conv_lst, uttr_lst = [], []
    conv_cnt = 1
    for key in split_lst:
        file = f"E:/django_project/annotator/data/conv_dep/pre_process/{key}.json"
        fp = open(file, 'r', encoding='utf-8')
        data = json.load(fp)

        for i, d in enumerate(data):
            conv_lst.append({
                'conv_id': conv_cnt,
                'set': key,
            })

            for turn, dialog in enumerate(d.get('dialog')):
                speaker = dialog.get('speaker')
                # requests.post(uttr_url, data={
                #     'conv_id': i+1,
                #     'uttr_id': turn,
                #     'word_id': 0,
                #     'word': speaker,
                # })
                uttr_lst.append({
                    'conv': conv_cnt,
                    'utr_id': turn,
                    'word_id': 0,
                    'word': speaker,
                })

                utterance = dialog.get('utterance')
                word_idx = 1 
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
    # conv_url = 'http://localhost:8000/api/conv/'
    # res = requests.post(conv_url, json=conv_lst)

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
       

if __name__ == '__main__':

    push_data()