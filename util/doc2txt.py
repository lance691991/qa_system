
import docx2txt

corpus_path = "corpus/09数字档案馆系统运行维护管理制度（完成）.docx"
text = docx2txt.process(corpus_path)
text_lines = text.split()

with open("corpus/txt_files/09数字档案馆系统运行维护管理制度（完成）.txt", "w") as f:
    for l in text_lines:
        f.write(f"{l}\n")
    f.close()

