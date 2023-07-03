from pyserini.index.lucene import LuceneIndexer, IndexReader


class IndexAdder:
    def __init__(self, index_dir=None, append=True, args=None):
        self.index_dir = index_dir
        self.indexer = LuceneIndexer(index_dir, append=append, args=args)

    def add_doc(self, doc_input: str):
        reader = IndexReader(self.index_dir)
        sentences = doc_input.split("。")
        print(sentences)
        new_index = reader.stats()["documents"] + 1
        for sentence in sentences:
            id = "doc" + str(new_index)
            new_index += 1
            self.indexer.add_doc_dict({
                "id": id,
                "contents": sentence
            })
        self.indexer.close()
        self.indexer = LuceneIndexer('../indexes/sparse_index', append=True,
                            args=["-language", "zh", "-index", "../indexes/sparse_index", "-storePositions",
                                  "-storeDocvectors", "-storeRaw"])


if __name__ == '__main__':
    # indexer = LuceneIndexer('./indexes/sparse_index', append=True,
    #                         args=["-language", "zh", "-index", "./indexes/sparse_index", "-storePositions",
    #                               "-storeDocvectors", "-storeRaw"])
    # indexer.add_doc_dict({'id': 'new0', 'contents': '这是测试2'})
    # indexer.close()
    reader = IndexReader("./indexes/sparse_index")
    print(reader.stats())
