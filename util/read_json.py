import json
import os

dir_path = "E:\\repository\\qa_system\\corpus\\mrc"
list_dir = os.listdir(dir_path)

# for file_name in list_dir:
#     if file_name.endswith(".json"):
#         with open("corpus/mrc/" + file_name, "r") as rf:
#             mrc_list = json.load(rf)
#             with open("corpus/mrc_json_files/" + file_name[0: -5] + ".jsonl", "a") as wf:
#                 for d in mrc_list:
#                     context_id = d.get("context_id")
#                     context_text = d.get("context_text")
#                     l_json = {"id": context_id,
#                               "contents": context_text}
#                     json.dump(l_json, wf)
#                     wf.write('\n')
#             rf.close()

for file_name in list_dir:
    if file_name.endswith(".json"):
        with open("corpus/mrc/" + file_name, "r") as rf:
            mrc_list = json.load(rf)
            # print(mrc_list[0].keys())
            with open("corpus/mrc_qas/" + file_name[0: -5] + ".jsonl", "a") as wf:
                for d in mrc_list:
                    qas_list = d.get("qas")
                    for qa in qas_list:
                        try:
                            json.dump(qa, wf, ensure_ascii=False)
                            wf.write("\n")
                        except Exception as e:
                            print(e)
                wf.close()
            rf.close()
