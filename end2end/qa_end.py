from pyserini.search.lucene import LuceneSearcher
from pyserini.search.hybrid import HybridSearcher
from pyserini.search.faiss import FaissSearcher, AutoQueryEncoder
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline, PretrainedConfig
import json


class QAEnd2End:
    def __init__(self, dense_searcher, sparse_searcher, qa_pipeline):
        self.dense_searcher = dense_searcher
        self.sparse_searcher = sparse_searcher
        self.hybrid_searcher = self.assemble_hybrid_searcher(dense_searcher, sparse_searcher)
        self.qa_pipline = qa_pipeline
        self.mrc_dense_index_json = None
        self.trainer = None
        self.index_adder = None

    def set_trainer(self, trainer):
        self.trainer = trainer

    def train(self, training_data):
        self.trainer.train(training_data)
        model = self.trainer.training_args.output_dir + "/checkpoint-30"
        self.reassemble_pipline(model)

    def reassemble_pipline(self, model):
        self.qa_pipline = pipeline('question-answering', model=model)

    def set_index_adder(self, index_adder):
        self.index_adder = index_adder

    def add_index(self, doc_input):
        self.index_adder.add_doc(doc_input)
        self.set_sparse_searcher('../indexes/sparse_index')

    def set_sparse_searcher(self, path_dir):
        self.sparse_searcher = LuceneSearcher(path_dir)
        self.sparse_searcher.set_language("zh")
        self.hybrid_searcher = self.assemble_hybrid_searcher(self.dense_searcher, self.sparse_searcher)

    @staticmethod
    def assemble_hybrid_searcher(d_searcher, s_searcher):
        return HybridSearcher(d_searcher, s_searcher)

    def set_json_faiss_index(self, path):
        self.mrc_dense_index_json = json.load(open(path))

    def hybrid_search(self, query, k=3):
        # hits = self.hybrid_searcher.search(query, k=k)
        # result_list = []
        # for i in range(k):
        #     doc_id = hits[i].docid
        #     faiss_content = self.mrc_dense_index_json.get(doc_id)
        #     raw_doc = self.sparse_searcher.search(faiss_content, k=1)[0].raw
        #     content = json.loads(raw_doc).get("contents")
        #     result_list.append(content)
        result_list = []
        hits = self.sparse_searcher.search(query, k=k)
        for i in range(len(hits)):
            result = ""
            doc_id = hits[i].docid
            doc_id_num = int(doc_id[3:])
            for j in range(-3, 4):
                content = json.loads(self.sparse_searcher.doc("doc" + str(doc_id_num + j)).raw()).get("contents")
                if not content.endswith("。"):
                    content += "。"
                result += content
            result_list.append(result)
        return result_list
        # hits = self.hybrid_searcher.search(query, k=k)
        # for i in range(len(hits)):
        #     result = ""
        #     doc_id = hits[i].docid
        #     doc_id_num = int(doc_id[3:])
        #     for j in range(-3, 4):
        #         content = json.loads(self.sparse_searcher.doc("doc" + str(doc_id_num + j)).raw()).get("contents")
        #         if not content.endswith("。"):
        #             content += "。"
        #         result += content
        #     result_list.append(result)
        # return result_list

    def qa(self, query, k=3):
        hybrid_search_result = self.hybrid_search(query=query, k=k)
        qa_result = []
        for r in hybrid_search_result:
            qa_input = {
                "question": query,
                "context": r
            }
            qa_result.append(self.qa_pipline(qa_input))
        return hybrid_search_result, qa_result


if __name__ == '__main__':

    s_searcher = LuceneSearcher('./indexes/mrc_sparse_index')
    s_searcher.set_language('zh')
    encoder = AutoQueryEncoder('./models/shibing')
    d_searcher = FaissSearcher(
        './indexes/mrc_index',
        encoder
    )
    # config = PretrainedConfig.from_json_file("./models/reader/luhua_mrc/config.json")
    model = AutoModelForQuestionAnswering.from_pretrained('./models/roberta')
    tokenizer = AutoTokenizer.from_pretrained('./models/roberta')
    QA = pipeline('question-answering', model=model, tokenizer=tokenizer)
    qa_end2end = QAEnd2End(d_searcher, s_searcher, QA)
    qa_end2end.set_json_faiss_index("./corpus/mrc_index/mrc_index.json")

    model = AutoModelForQuestionAnswering.from_pretrained('./models/reader/luhua_mrc')
    tokenizer = AutoTokenizer.from_pretrained('./models/reader/luhua_mrc')
    QA = pipeline('question-answering', model=model, tokenizer=tokenizer)
    qa_end2end_luhua = QAEnd2End(d_searcher, s_searcher, QA)
    qa_end2end_luhua.set_json_faiss_index("./corpus/mrc_index/mrc_index.json")

    hybrid_search_result, qa_result = qa_end2end.qa(query="woshiren")
    print(hybrid_search_result)
    print(qa_result)

    hybrid_search_result, qa_result = qa_end2end_luhua.qa(query="woshiren")
    print(hybrid_search_result)
    print(qa_result)