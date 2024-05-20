import pandas as pd
from jamo import *

CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28

class Node:
    def __init__(self, key, data=None):
        self.key = key
        self.data = []
        self.children = {}

class SubjectName:
    def __init__(self) -> None:
        self.trie = self.returnTrie_ver2()
        
    def return_jamo(self, text):
        return_value = ""
        for t in text:
            jamo_list = j2hcj(h2j(t))
            if len(jamo_list) == 2:
                return_value += jamo_list[0]
                return_value += j2h(*jamo_list)
            else:
                return_value += jamo_list[0]
                for i in range(2,len(jamo_list)+1):
                    han = j2h(*jamo_list[:i])
                    return_value += han
        return return_value
    
    def return_chosung(self, text):
        chosung = ""
        for t in text:
            if ord('가') <= ord(t) <= ord('힣'):
                chosung_index = (ord(t) - BASE_CODE) // CHOSUNG
                chosung += CHOSUNG_LIST[chosung_index]
            else:
                chosung += t
        return chosung

    def returnTrie_ver2(self):
        df = pd.read_csv(r"C:\Users\wldnj\OneDrive\바탕 화면\autocomplete\brands.csv")
        brand_list = df.iterrows()
        head = Node(None)
        for i, brand in brand_list:
            kor_name = brand['kor_name']
            current_node = head
            kor_name_jamo = self.return_jamo(kor_name)
            for kor in kor_name_jamo:
                if kor not in current_node.children:
                    current_node.children[kor] = Node(kor)
                current_node.children[kor].data.append(kor_name)
                current_node = current_node.children[kor]  
            
            kor_name = brand['kor_name']
            current_node = head
            kor_name_ja = self.return_chosung(kor_name)
            for kor in kor_name_ja:
                if kor not in current_node.children:
                    current_node.children[kor] = Node(kor)
                if kor_name not in current_node.children[kor].data:
                    current_node.children[kor].data.append(kor_name)
                current_node = current_node.children[kor]  
        self.trie = head
        return head

    
    def searchTrie(self, keyword):
        result = []
        current_node = self.trie
        for word in keyword:
            if not is_hangul_char(word):
                if word in current_node.children:
                    current_node = current_node.children[word]
                else:
                    result = current_node.data
                    break
            else:
                if is_jamo(word):
                    if word in current_node.children:
                        current_node = current_node.children[word]
                    else:
                        result = current_node.data
                        break
                else:
                    word_list = self.return_jamo(word)
                    for w in word_list:
                        if w in current_node.children:
                            current_node = current_node.children[w]
                        else:
                            result = current_node.data
                            break

        if len(result) == 0:
            result = current_node.data
        result = result[-10:][::-1]
        return result




                        




# def returnTrie():
#     df = pd.read_csv("./brands.csv")

#     brand_list = df.iterrows()
#     head = Node(None)
#     for i, brand in brand_list:
#         kor_name = brand["kor_name"]
#         current_node = head
#         for kor in kor_name:
#             if kor not in current_node.children:
#                 current_node.children[kor] = Node(kor)
#                 current_node.children[kor].data.append(kor_name)
#             else:
#                 current_node.children[kor].data.append(kor_name)
#             current_node = current_node.children[kor]
#     return head

