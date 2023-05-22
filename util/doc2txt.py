import docx2txt
import os

# dir_path = "E:\\repository\\qa_system\\corpus"
# list_dir = os.listdir(dir_path)
#
# for file_name in list_dir:
#     if file_name.endswith(".docx"):
#         corpus_path = "corpus/" + file_name
#         text = docx2txt.process(corpus_path)
#         text_lines = text.split("\n")
#
#         with open("corpus/txt_files/" + file_name[0: -5] + ".txt", "w") as f:
#             for l in text_lines:
#                 f.write(f"{l}\n")
#             f.close()

dir_path = "E:\\repository\\qa_system\\corpus\\YLJ-IM-26声像档案管理实施细则（完成）"
list_dir = os.listdir(dir_path)

for file_name in list_dir:
    if file_name.endswith(".docx"):
        corpus_path = "corpus/YLJ-IM-26声像档案管理实施细则（完成）/" + file_name
        text = docx2txt.process(corpus_path)
        text_lines = text.split("\n")

        with open("corpus/txt_files/" + file_name[0: -5] + ".txt", "w") as f:
            for l in text_lines:
                try:
                    f.write(f"{l}\n")
                except Exception as e:
                    print(e)
            f.close()