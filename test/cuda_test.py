from pyserini.search.faiss import FaissSearcher, AutoQueryEncoder

encoder = AutoQueryEncoder('./models/roberta')
searcher = FaissSearcher(
    './indexes/dense_sample_index',
    './models/roberta'
)
hits = searcher.search('服务请求管理是什么')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')