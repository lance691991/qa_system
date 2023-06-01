import jsonlines
from sklearn.metrics.pairwise import cosine_similarity
from text2vec import SentenceModel
from pyserini.search.lucene import LuceneSearcher
import json

sentences = ['责任者填写要求']
model = SentenceModel('./models/shibing')
embeddings = model.encode(sentences)
result = []

with jsonlines.open("./embeddings/shibing_embeddings/embeddings.jsonl") as rf:
    for d in rf:
        d_embedding = d.get("vector")
        cos_sim = cosine_similarity(embeddings, [d_embedding])[0][0]
        if not result:
            d["cos_sim"] = cos_sim
            result.append(d)
        else:
            for i in range(len(result)):
                if result[i].get("cos_sim") == cos_sim:
                    continue
                elif result[i].get("cos_sim") < cos_sim:
                    d["cos_sim"] = cos_sim
                    result.insert(i, d)
                    if len(result) > 3:
                        result.pop()
    rf.close()

doc_ids = []
for r in result:
    doc_ids.append(r.get("id"))
    print(r.get("cos_sim"))

s_searcher = LuceneSearcher('indexes/sparse_index')
for doc_id in doc_ids:
    print(doc_id)
    doc_id_num = int(doc_id[3:])
    print(json.loads(s_searcher.doc("doc" + str(doc_id_num - 3)).raw()).get("contents"))
    print(json.loads(s_searcher.doc("doc" + str(doc_id_num - 2)).raw()).get("contents"))
    print(json.loads(s_searcher.doc("doc" + str(doc_id_num - 1)).raw()).get("contents"))
    print(json.loads(s_searcher.doc("doc" + str(doc_id_num - 0)).raw()).get("contents"))
    print(json.loads(s_searcher.doc("doc" + str(doc_id_num + 1)).raw()).get("contents"))
    print(json.loads(s_searcher.doc("doc" + str(doc_id_num + 2)).raw()).get("contents"))
    print(json.loads(s_searcher.doc("doc" + str(doc_id_num + 3)).raw()).get("contents"))


