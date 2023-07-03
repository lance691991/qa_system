from pyserini.search.faiss import FaissSearcher, AutoQueryEncoder
from pyserini.search.lucene import LuceneSearcher
import json

mrc_dense_index_json = json.load(open("corpus/mrc_index/mrc_index.json"))
s_searcher = LuceneSearcher('indexes/sparse_index')
s_searcher.set_language('zh')
encoder = AutoQueryEncoder('./models/shibing')
searcher = FaissSearcher(
    './indexes/shibing_index',
    encoder
)

hits = searcher.search("这是一首简单", k=3)

# for i in range(0, 3):
#     print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
#     doc_id = hits[i].docid
#     doc_id_num = int(doc_id[3:])
#     print(json.loads(s_searcher.doc("doc" + str(doc_id_num - 3)).raw()).get("contents"))
#     print(json.loads(s_searcher.doc("doc" + str(doc_id_num - 2)).raw()).get("contents"))
#     print(json.loads(s_searcher.doc("doc" + str(doc_id_num - 1)).raw()).get("contents"))
#     print(json.loads(s_searcher.doc("doc" + str(doc_id_num - 0)).raw()).get("contents"))
#     print(json.loads(s_searcher.doc("doc" + str(doc_id_num + 1)).raw()).get("contents"))
#     print(json.loads(s_searcher.doc("doc" + str(doc_id_num + 2)).raw()).get("contents"))
#     print(json.loads(s_searcher.doc("doc" + str(doc_id_num + 3)).raw()).get("contents"))
for i in range(3):
    doc_id = hits[i].docid
    faiss_content = mrc_dense_index_json.get(doc_id)
    raw_doc = s_searcher.search(faiss_content, k=1)[0].raw
    content = json.loads(raw_doc).get("contents")
    print(content)
