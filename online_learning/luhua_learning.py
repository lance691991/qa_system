from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from transformers import TrainingArguments, Trainer
import datasets
import pandas as pd


model = AutoModelForQuestionAnswering.from_pretrained("./online_learning/checkpoint-30")
tokenizer = AutoTokenizer.from_pretrained('./online_learning/checkpoint-30')
QA = pipeline('question-answering', model=model, tokenizer=tokenizer)
QA_input = {'question': "现任总统是谁",
            'context': "我们发现现任总统不是张三，但我们知道现任总统是李四"}
print(QA(QA_input))

def tokenize_function(examples):
    inputs = tokenizer(examples["question"], examples["context"], return_overflowing_tokens=True, return_offsets_mapping=True)
    # inputs = tokenizer(examples["question"], examples["context"])
    offset_mapping = inputs.pop("offset_mapping")
    sample_map = inputs.pop("overflow_to_sample_mapping")
    answers = examples["answers"]
    if not isinstance(answers, list):
        answers = [answers]
    start_positions = []
    end_positions = []

    for i, offset in enumerate(offset_mapping):
        sample_idx = sample_map[i]
        answer = answers[sample_idx]
        start_char = answer["answer_start"][0]
        end_char = answer["answer_start"][0] + len(answer["text"][0])
        sequence_ids = inputs.sequence_ids(i)

        # Find the start and end of the context
        idx = 0
        while sequence_ids[idx] != 1:
            idx += 1
        context_start = idx
        while sequence_ids[idx] == 1:
            idx += 1
        context_end = idx - 1

        # If the answer is not fully inside the context, label is (0, 0)
        if offset[context_start][0] > start_char or offset[context_end][1] < end_char:
            start_positions.append(0)
            end_positions.append(0)
        else:
            # Otherwise it's the start and end token positions
            idx = context_start
            while idx <= context_end and offset[idx][0] <= start_char:
                idx += 1
            start_positions.append(idx - 1)

            idx = context_end
            while idx >= context_start and offset[idx][1] >= end_char:
                idx -= 1
            end_positions.append(idx + 1)
    inputs["start_positions"] = start_positions
    inputs["end_positions"] = end_positions
    inputs['input_ids'] = inputs["input_ids"][0]
    inputs['token_type_ids'] = inputs["token_type_ids"][0]
    inputs['attention_mask'] = inputs["attention_mask"][0]
    return inputs


training_data = {
    "context": ["我们发现现任总统不是张三，但我们知道现任总统是李四"],
    "id": ["TRAIN_ONLINE"],
    "question": ["现任总统是谁"],
    "answers": [{
        "answer_start": [23],
        "text": ["李四"]
    }]
}

training_data = datasets.Dataset.from_dict(training_data)
tokenized_data = training_data.map(tokenize_function, remove_columns=["context", "id", "question", "answers"])
training_args = TrainingArguments(output_dir="./online_learning",  num_train_epochs=30)
training_args = training_args.set_save(strategy="steps", steps=30)
print(training_args.output_dir)
# trainer = Trainer(model=model, args=training_args, train_dataset=tokenized_data, tokenizer=tokenizer)
# trainer.train()
