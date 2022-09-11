import gensim
from gensim.utils import simple_preprocess
from nltk.stem import LancasterStemmer
import re
import nltk
import jieba

def jieba_token(documents,n_gram=True,stop = '') :
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

    # 匯入辭典
    jieba.load_userdict("./自定義辭典(繁體).txt") #若有匯入自動取代
    
    # 網址刪除
    p = r'(https?://\S+[a-zA-Z0-9])'
    t = r'bit\S+[a-zA-Z0-9]'
    z = r'\u3000'
    m = [re.sub(p, '', str(i), count=0, flags=0) for i in documents]
    m = [re.sub(t, '', str(i), count=0, flags=0) for i in m]
    documents = [re.sub(z, '', str(i), count=0, flags=0) for i in m]

    # 斷詞
    content = []

    for sentence in documents:
        seg_list = jieba.cut(sentence)
        sentence = ' '.join(seg_list)
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

