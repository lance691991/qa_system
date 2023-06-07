import os
import json

dir_path = "E:\\repository\\qa_system\\corpus\\mrc"
list_dir = os.listdir(dir_path)

doc_id = 1
faiss_index = {}
for file_name in list_dir:
    if file_name.endswith(".json"):
        with open("corpus/mrc/" + file_name, "r") as rf:
            mrc_list = json.load(rf)
            with open("corpus/mrc_json_faiss_files/" + file_name[0: -5] + ".jsonl", "a") as wf:
                for d in mrc_list:
                    contents = d.get("context_text")
                    contents_list = contents.split("。")
                    for c in contents_list:
                        context_id = "doc" + str(doc_id)
                        doc_id += 1
                        context_text = c
                        faiss_index[context_id] = context_text
                        l_json = {"id": context_id,
                                  "contents": context_text}
                        json.dump(l_json, wf)
                        wf.write('\n')
                wf.close()
            rf.close()
with open("corpus/mrc_index/mrc_index.json", "w") as wf:
    json.dump(faiss_index, wf)
    wf.close()
