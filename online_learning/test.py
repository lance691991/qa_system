from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

model = AutoModelForQuestionAnswering.from_pretrained('./models/reader/luhua_mrc')
tokenizer = AutoTokenizer.from_pretrained('./models/reader/luhua_mrc')
QA = pipeline('question-answering', model=model, tokenizer=tokenizer)
QA_input = {'question': "现任总统是谁",
            'context': "我们发现现任总统不是张三，但我们知道现任总统是李四"}
print(QA(QA_input))

QA_input = {'question': "《战国无双3》是由哪两个公司合作开发的？",
            'context': "\"《战国无双3》（）是由光荣和ω-force开发的战国无双系列的正统第三续作。本作以三大故事为主轴，分别是以武田信玄等人为主的《关东三国志》，织田信长等人为主的《战国三杰》，石田三成等人为主的《关原的年轻武者》，丰富游戏内的剧情。此部份专门介绍角色，欲知武..."}
print(QA(QA_input))

model_checkpoint2 = "./online_learning/checkpoint-30"
QA = pipeline("question-answering", model=model_checkpoint2)

QA_input = {'question': "现任总统是谁",
            'context': "我们发现现任总统不是张三，但我们知道现任总统是李四"}
print(QA(QA_input))

QA_input = {'question': "《战国无双3》是由哪个公司合作开发的？",
            'context': "\"《战国无双3》（）是由光荣和ω-force开发的战国无双系列的正统第三续作。本作以三大故事为主轴，分别是以武田信玄等人为主的《关东三国志》，织田信长等人为主的《战国三杰》，石田三成等人为主的《关原的年轻武者》，丰富游戏内的剧情。此部份专门介绍角色，欲知武..."}
print(QA(QA_input))