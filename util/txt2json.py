import json
import os

dir_path = "E:\\repository\\qa_system\\corpus\\txt_files"
list_dir = os.listdir(dir_path)
doc_index = 1
for file_name in list_dir:
    if file_name.endswith(".txt"):
        with open("corpus/txt_files/" + file_name, "r") as rf:
            lines = rf.readlines()
            with open("./corpus/json_files/" + file_name[0: -4] + ".jsonl", "a") as wf:
                for l in lines:
                    l = l.replace("\t", "").replace(" ", "").replace("\n", "")
                    if not l:
                        continue
                    l_json = {"id": f"doc{doc_index}",
                              "contents": l}
                    json.dump(l_json, wf)
                    wf.write('\n')
                    doc_index += 1
                wf.close()
            rf.close()