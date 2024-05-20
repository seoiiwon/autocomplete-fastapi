import pandas as pd

class Node:
    def __init__(self, key, data=None):
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

