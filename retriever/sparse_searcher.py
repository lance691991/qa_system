from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher('indexes/sparse_index')
searcher.set_language('zh')
hits = searcher.search('工程建设过程中必须要拍照的内容和节点')

for i in range(len(hits)):
    print(f'{i+1:2} {hits[i].docid:4} {hits[i].score:.5f}')
    print(hits[i].raw)
