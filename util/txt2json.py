import json
with open("corpus/txt_files/09数字档案馆系统运行维护管理制度（完成）.txt", "r") as rf:
    lines = rf.readlines()
    with open("./corpus/json_format_files/09.jsonl", "a") as wf:
        doc_index = 1
        for l in lines:
            l = l.replace("\n", "")
            l_json = {"id": f"doc{doc_index}",
                      "contents": l}
            json.dump(l_json, wf)
            wf.write('\n')
            doc_index += 1
        wf.close()
    rf.close()