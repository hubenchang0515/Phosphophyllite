import jieba
from typing import List

def split_words(text:str) -> List[str]:
    gen = jieba.cut_for_search(text)
    return [word for word in gen if word != " "]

if __name__ == "__main__":
    print(split_words("原神 妮露圣遗物"))