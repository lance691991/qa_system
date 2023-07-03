from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher('indexes/sparse_index')
searcher.set_language('zh')
hits = searcher.search('看远方的')

for i in range(len(hits)):
    print(f'{i+1:2} {hits[i].docid:4} {hits[i].score:.5f}')
    print(hits[i].raw)
