import jieba
from typing import List,Dict

def split_words(text:str) -> List[str]:
    gen = jieba.cut_for_search(text)
    return [word for word in gen if word != " "]

def keyword_scores_to_dict(keyword_scores_string:str) -> Dict[int,float]:
    begin:int = keyword_scores_string.index("{") + 1
    end:int = keyword_scores_string.index("}")
    pairs:List[str] = keyword_scores_string[begin:end].split(",")

    keyword_scores:Dict[int,float] = {}
    for pair in pairs:
        kv:List[str] = pair.split(":")
        keyword_scores[int(kv[0])] = float(kv[1])

    return keyword_scores

if __name__ == "__main__":
    print(split_words("原神 妮露圣遗物"))