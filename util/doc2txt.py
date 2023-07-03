import docx2txt
import os

dir_path = "E:\\repository\\qa_system\\corpus\\电子文件通用元数据规范（完成）"
list_dir = os.listdir(dir_path)

for file_name in list_dir:
    if file_name.endswith(".docx"):
        corpus_path = "corpus/电子文件通用元数据规范（完成）/" + file_name
        text = docx2txt.process(corpus_path)
        text_lines = text.split("\n")

        with open("corpus/txt_files/" + file_name[0: -5] + ".txt", "w") as f:
            for l in text_lines:
                try:
                    f.write(f"{l}\n")
                except Exception as e:
                    print(e)
            f.close()

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
#                 try:
#                     f.write(f"{l}\n")
#                 except Exception as e:
#                     print(e)
#             f.close()