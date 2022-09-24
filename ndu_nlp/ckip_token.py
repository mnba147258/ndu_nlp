from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
from collections import defaultdict
import gensim
import re
from gensim.utils import simple_preprocess

def ckip_token(documents,n_gram=True,stop = '',path = r'D:\data') :
    """
    jieba token contain n_gram and html process

    ...

    Attributes
    ----------
    documents : list
        target content.
    n_gram : bool
        if you want to ues n_grams
    single_word : bool
        if you want to ues single_word
    stop : list
        str you want put in your stopword

    return
    -------
    process content
    """
    # 匯入停用詞
    def stopwordslist(filepath):  
        stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]  
        return stopwords 
    stopwords = stopwordslist('./中文停用詞.txt')  # 若有新匯入檔案自動取代
    for i in stop:
        stopwords.append(i) 

    # 匯入預訓練檔案
    ws = WS(path)
    pos = POS(path)
    ner = NER(path)    

    # 匯入辭典
    with open('./自定義辭典(繁體).txt', 'r',encoding='utf-8') as file:
        user_dict = file.read().split("\n")
    x = [i.split('\t') for i in user_dict]
    word_to_weight = defaultdict()
    for z in x :
        word_to_weight[z[0]] = z[1]
    dictionary = construct_dictionary(word_to_weight)
    
    # 網址刪除
    p = r'(https?://\S+[a-zA-Z0-9])'
    t = r'bit\S+[a-zA-Z0-9]'
    z = r'\u3000'
    m = [re.sub(p, '', str(i), count=0, flags=0) for i in documents]
    m = [re.sub(t, '', str(i), count=0, flags=0) for i in m]
    documents = [re.sub(z, '', str(i), count=0, flags=0) for i in m]

    # 斷詞
    word_sentence_list = ws( documents, recommend_dictionary = dictionary )
    content = []
    for sentence in word_sentence_list:
        sentence = ' '.join(sentence)
        words = sentence.split(' ')
        content.append(words)
    # 停用詞排除
    content = [[word for word in simple_preprocess(str(doc)) if word not in stopwords] for doc in content]
    

    # 多詞判定
    if n_gram == True:
        bigram = gensim.models.Phrases(content) 
        trigram = gensim.models.Phrases(bigram[content])  

        bigram_mod = gensim.models.phrases.Phraser(bigram)
        trigram_mod = gensim.models.phrases.Phraser(trigram)

        # See trigram example
        content = [' '.join(i) for i in trigram_mod[bigram_mod[content]]]
    
    return content