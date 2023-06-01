from pyserini.search.lucene import LuceneSearcher
from pyserini.search.hybrid import HybridSearcher
from pyserini.search.faiss import FaissSearcher, AutoQueryEncoder
from transformers import AutoModelForQuestionAnswering,AutoTokenizer,pipeline
import json


class QAEnd2End:
    def __init__(self, dense_searcher, sparse_searcher, qa_pipeline):
        self.dense_searcher = dense_searcher
        self.sparse_searcher = sparse_searcher
        self.assemble_hybrid_searcher(dense_searcher, sparse_searcher)
        self.qa_pipline = qa_pipeline

    def assemble_hybrid_searcher(self, d_searcher, s_searcher):
        self.hybrid_searcher = HybridSearcher(d_searcher, s_searcher)

    def hybrid_search(self, query, k=3, num_sentence=5):
        hits = self.hybrid_searcher.search(query, k=k)
        result_list = []
        for i in range(k):
            result = ""
            doc_id = hits[i].docid
            doc_id_num = int(doc_id[3:])
            for j in range(-num_sentence, num_sentence + 1):
                content = json.loads(self.sparse_searcher.doc("doc" + str(doc_id_num + j)).raw()).get("contents")
                print(content)
                if not content:
                    continue
                else:
                    if not content.endswith("。"):
                        content += "。"
                    result += content
            result_list.append(result)
            print("\n")
        return result_list

    def qa(self, query):
        hybrid_search_result = self.hybrid_search(query=query)
        qa_result = []
        for r in hybrid_search_result:
            qa_input = {
                "question": query,
                "context": r
            }
            qa_result.append(self.qa_pipline(qa_input))
        return qa_result


if __name__ == '__main__':
    s_searcher = LuceneSearcher('indexes/sparse_index')
    s_searcher.set_language('zh')
    encoder = AutoQueryEncoder('./models/shibing')
    d_searcher = FaissSearcher(
        './indexes/shibing_index',
        encoder
    )
    model = AutoModelForQuestionAnswering.from_pretrained('./models/reader/luhua_mrc')
    tokenizer = AutoTokenizer.from_pretrained('./models/reader/luhua_mrc')
    QA = pipeline('question-answering', model=model, tokenizer=tokenizer)
    qa_end2end = QAEnd2End(d_searcher, s_searcher, QA)
    print(qa_end2end.qa(query="网页归档需收集的内容"))