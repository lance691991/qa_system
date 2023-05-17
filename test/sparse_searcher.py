from pyserini.search.lucene import LuceneSearcher

searcher = LuceneSearcher('indexes/sample_index')
searcher.set_language('zh')
hits = searcher.search('问题')

for i in range(len(hits)):
    print(f'{i+1:2} {hits[i].docid:4} {hits[i].score:.5f}')
