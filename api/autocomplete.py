import pandas as pd
from jamo import *

CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28

# ========== part1 ==========
# TRIE로만 AUTOCOMPLETE
class Node:
    def __init__(self, key=None, data=None):
        self.key = key
        self.data = []
        self.children = {}

def returnTrie():
    df = pd.read_csv("./brands.csv")

    brand_list = df.iterrows()
    head = Node(None)
    for i, brand in brand_list:
        kor_name = brand["kor_name"]
        current_node = head
        for kor in kor_name:
            if kor not in current_node.children:
                current_node.children[kor] = Node(kor)
                current_node.children[kor].data.append(kor_name)
            else:
                current_node.children[kor].data.append(kor_name)
            current_node = current_node.children[kor]
    return head
# ===========================





# ========== part2 ==========
# jamo 포함 AUTOCOMPLETE
class SubjectName:
    def __init__(self) -> None:
        self.trie = self.returnTrie_ver2()
        
    def return_jamo(self, text):
        return_value = ""
        for t in text:
            jamo_list = j2hcj(h2j(t))
            if len(jamo_list) == 2: #종성이 없는 경우
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
        return result
# ===========================    




# ========== part3 ==========
def textTokenize(text):
    text_token_list = []
    for i in range(len(text)):
        if text[i] == " ":
            continue
        text_token_list.append(text[i:])
    return text_token_list

class Node:
    def __init__(self, key):
        self.key = key
        self.data = []
        self.children = {}
        self.prefix_data = []
        self.suffix_data = []
    
    def prefix_data_insert(self, text):
        self.prefix_data.append(text)

    def suffix_data_insert(self, text):
        self.suffix_data.append(text) 


# suffix trie 추가 AUTOCOMPLETE
class Trie:
    def __init__(self):
        self.head = Node(None)

    def prefix_eng_insert(self, eng_name):
        text = eng_name.lower()
        curr = self.head
        for t in text:
            if t not in curr.children:
                curr.children[t] = Node()
            curr = curr.children[t]
            curr.prefix_data_insert(eng_name)
    
    def prefix_kor_insert(self, kor_name):
        text = SubjectName().return_jamo(kor_name)
        curr = self.head
        for t in text:
            if t not in curr.children:
                curr.children[t] = Node(t)
            curr = curr.children[t]
            curr.prefix_data_insert(kor_name)
    
    def suffix_insert(self, text, name):
        text = text.lower()
        curr = self.head
        for t in text:
            if t not in curr.children:
                curr.children[t] = Node(t)
            curr = curr.children[t]
            curr.suffix_data_insert(name)

    def query(self, text):
        text = text.lower()
        curr = self.head
        for t in text:
            if t not in curr.children:
                break
            else:
                curr = curr.children[t]
        data = {}
        data["prefix_result"] = curr.prefix_data[::-1]
        data["suffix_result"] = curr.suffix_data[::-1]
        return data

    def query_kor(self, text):
        kor_text = SubjectName().return_jamo(text)
        return self.query(kor_text)


def returnTrie_ver3(text):
    df = pd.read_csv(r"C:\Users\wldnj\OneDrive\바탕 화면\autocomplete\brands.csv")
    trie = Trie()
    subjectname = SubjectName()
    for i, rows in df.iterrows():
        kor_name = rows["kor_name"]
        kor_name_token_list = []
        kor_suffix = textTokenize(kor_name)
        for suffix in kor_suffix:
            kor_name_token_list.append(subjectname.return_jamo(suffix))
        trie.prefix_kor_insert(kor_name)
        for kor_name_token in kor_name_token_list[1:]:
            trie.suffix_insert(kor_name_token, kor_name)
    
    searchResult_dict = trie.query_kor(text)
    searchResult_list = []
    for key, value in searchResult_dict.items():
        searchResult_list.extend(value)
    return searchResult_list
