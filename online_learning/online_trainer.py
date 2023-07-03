from transformers import TrainingArguments, Trainer
import datasets
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

class OnlineLearner:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.training_args = None
        self.trainer = None

    def tokenize_function(self, examples):
        inputs = self.tokenizer(examples["question"], examples["context"], return_overflowing_tokens=True,
                                return_offsets_mapping=True)
        offset_mapping = inputs.pop("offset_mapping")
        sample_map = inputs.pop("overflow_to_sample_mapping")
        answers = [examples["answers"]]
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

    def set_training_args(self, output_dir, num_train_epochs):
        training_args = TrainingArguments(output_dir=output_dir, num_train_epochs=num_train_epochs)
        training_args = training_args.set_save(strategy="steps", steps=num_train_epochs)
        self.training_args = training_args

    def train(self, training_data):
        training_data = datasets.Dataset.from_dict(training_data)
        tokenized_data = training_data.map(self.tokenize_function, remove_columns=list(training_data.features.keys()))
        self.trainer = Trainer(model=self.model, args=self.training_args, train_dataset=tokenized_data, tokenizer=self.tokenizer)
        self.trainer.train()
        self.model = self.training_args.output_dir + "/checkpoint-30"
        self.tokenizer = self.training_args.output_dir + "/checkpoint-30"


if __name__ == '__main__':
    model = AutoModelForQuestionAnswering.from_pretrained('./models/reader/luhua_mrc')
    tokenizer = AutoTokenizer.from_pretrained('./models/reader/luhua_mrc')
    trainer = OnlineLearner(model, tokenizer)
    trainer.set_training_args("./online_learning", 30)
    training_data = {
        "context": ["我们发现现任总统不是张三，但我们知道现任总统是李四"],
        "id": ["TRAIN_ONLINE"],
        "question": ["现任总统是谁"],
        "answers": [{
            "answer_start": [10],
            "text": ["张三"]
        }]
    }
    trainer.train(training_data)