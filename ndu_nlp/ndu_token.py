import gensim
from gensim.utils import simple_preprocess
from nltk.stem import LancasterStemmer
import re
import nltk
import jieba

def english_token(documents,n_gram=True,stemming=True):
    """
    english token contain n_gram and stemming

    ...

    Attributes
    ----------
    documents : list
        target content.
    n_gram : bool
        if you want to ues n_grams
    stemming : bool
        if you want to ues stemming

    return
    -------
    process content
    """
    # stop word
    nltk.download('stopwords')
    stop_words = nltk.corpus.stopwords.words('english')

    # regular expression
    def remove_URL(text):
        url = re.compile(r'https?://\S+')
        return url.sub(r' ', text)
    def remove_html(text):
        html = re.compile(r'<.*?>')
        return html.sub(r'', text)
    def remove_atsymbol(text):
        name = re.compile(r'@\S+')
        return name.sub(r' ', text)
    def remove_hashtag(text):
        hashtag = re.compile(r'#')
        return hashtag.sub(r' ', text)
    def remove_emoji(string):
        emoji_pattern = re.compile("["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                u"\U00002500-\U00002BEF"  # chinese char
                                u"\U00002702-\U000027B0"
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                u"\U0001f926-\U0001f937"
                                u"\U00010000-\U0010ffff"
                                u"\u2640-\u2642"
                                u"\u2600-\u2B55"
                                u"\u200d"
                                u"\u23cf"
                                u"\u23e9"
                                u"\u231a"
                                u"\ufe0f"  # dingbats
                                u"\u3030"
                                "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r' emoji ', string)
    

    documents = [remove_emoji(remove_hashtag(remove_atsymbol(remove_html(remove_URL(i.lower()))))) for i in documents]
    content = [' '.join([word for word in simple_preprocess(str(sentence)) if word not in stop_words]) for sentence in documents]
    # 多詞判定
    if n_gram == True:
        x = [i.split(" ") for i in content]
        bigram = gensim.models.Phrases(x) 
        trigram = gensim.models.Phrases(bigram[x])  

        bigram_mod = gensim.models.phrases.Phraser(bigram)
        trigram_mod = gensim.models.phrases.Phraser(trigram)

        # See trigram example
        content = [' '.join(i) for i in trigram_mod[bigram_mod[x]]]

    if stemming == True:
        lancaster=LancasterStemmer()
        content = [' '.join([lancaster.stem(i) for i in str(content_raw).split(' ')]) for content_raw in content]
    return content



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

