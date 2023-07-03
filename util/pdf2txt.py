import PyPDF2
import os

# dir_path = "E:\\repository\\qa_system\\corpus\\电子文件通用元数据规范（完成）"
# list_dir = os.listdir(dir_path)
#
# for file_name in list_dir:
#     if file_name.endswith(".docx"):
#         corpus_path = "corpus/电子文件通用元数据规范（完成）/" + file_name
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

dir_path = "E:\\repository\\qa_system\\corpus"
list_dir = os.listdir(dir_path)

for file_name in list_dir:
    if file_name.endswith(".pdf"):
        corpus_path = "corpus/" + file_name
        with open(corpus_path, "rb") as rf:
            pdf_obj = PyPDF2.PdfReader(rf)
            num_pages = len(pdf_obj.pages)
            for i in range(num_pages):
                page_obj = pdf_obj.pages[i]
                text = page_obj.extract_text()

                with open("corpus/txt_files/" + file_name[0: -4] + ".txt", "a") as f:
                    try:
                        f.write(text)
                    except Exception as e:
                        print(e)
                    f.close()
            rf.close()