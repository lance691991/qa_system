from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher('indexes/mrc_sparse_index')
searcher.set_language('zh')
hits = searcher.search('武藏浦和站位于哪里')

for i in range(len(hits)):
    print(f'{i+1:2} {hits[i].docid:4} {hits[i].score:.5f}')
    print(hits[i].raw)
