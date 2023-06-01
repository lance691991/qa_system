from pyserini.search.faiss import FaissSearcher, AutoQueryEncoder
from pyserini.search.lucene import LuceneSearcher
import json


s_searcher = LuceneSearcher('indexes/sparse_index')
encoder = AutoQueryEncoder('./models/shibing')
searcher = FaissSearcher(
    './indexes/shibing_index',
    encoder
)

hits = searcher.search("工程建设过程中必须要拍照的内容和节点", k=3)

for i in range(0, 3):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
    doc_id = hits[i].docid
    doc_id_num = int(doc_id[3:])
    print(json.loads(s_searcher.doc("doc" + str(doc_id_num - 3)).raw()).get("contents"))
    print(json.loads(s_searcher.doc("doc" + str(doc_id_num - 2)).raw()).get("contents"))
    print(json.loads(s_searcher.doc("doc" + str(doc_id_num - 1)).raw()).get("contents"))
    print(json.loads(s_searcher.doc("doc" + str(doc_id_num - 0)).raw()).get("contents"))
    print(json.loads(s_searcher.doc("doc" + str(doc_id_num + 1)).raw()).get("contents"))
    print(json.loads(s_searcher.doc("doc" + str(doc_id_num + 2)).raw()).get("contents"))
    print(json.loads(s_searcher.doc("doc" + str(doc_id_num + 3)).raw()).get("contents"))
