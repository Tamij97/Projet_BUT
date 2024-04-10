from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
from googletrans import Translator

class IA:
    def __init__(self, cache_dir="/code/.cache"):
        self.tokenizer_bert = AutoTokenizer.from_pretrained('DracolIA/BERT-Context-based-QA', cache_dir=cache_dir)
        self.model_bert = AutoModelForQuestionAnswering.from_pretrained('DracolIA/BERT-Context-based-QA', cache_dir=cache_dir)

        self.tokenizer_bigbird = AutoTokenizer.from_pretrained('DracolIA/BigBird-Roberta-Context-based-QA', cache_dir=cache_dir)
        self.model_bigbird = AutoModelForQuestionAnswering.from_pretrained('DracolIA/BigBird-Roberta-Context-based-QA', cache_dir=cache_dir)

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    def generate_responses(self, question, file_content, have_file, selected_model):
        translator = Translator()
        language = translator.detect(question).lang.upper() # Verify the language of the prompt

        if have_file:
            context = file_content
        else:   
            context = ""

        if selected_model.upper() == "BERT":
            tokenizer = self.tokenizer_bert
            model = self.model_bert
            see = "BERT"
        elif selected_model.upper() == "BIGBIRD":
            tokenizer = self.tokenizer_bigbird
            model = self.model_bigbird
            see = "BIGBIRD"

        if language != "EN":
                question = translator.translate(question, src=language, dest="en").text # Translation of user text to english for the model

        # Tokenize the input question and context
        inputs = tokenizer.encode_plus(
            question, context,
            add_special_tokens=True,
            return_tensors="pt",
            truncation="only_second",  # Only truncate the context, not the question
            max_length=512,
            stride=128,
            return_overflowing_tokens=True,
            return_offsets_mapping=True,
            padding="max_length"
        )

        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs["attention_mask"].to(self.device)

        # Model inference
        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_mask)

        # Get the most likely beginning and end of answer with the argmax of the score
        answer_start_scores = outputs.start_logits
        answer_end_scores = outputs.end_logits

        answer_start = torch.argmax(answer_start_scores, dim=-1)  # Get the index of the highest start score
        answer_end = torch.argmax(answer_end_scores, dim=-1) + 1  # Get the index of the highest end score

        # Convert the token indexes to actual text of the answer
        answer = tokenizer.decode(inputs['input_ids'][0][answer_start:answer_end], skip_special_tokens=True)
        if language != "EN":
            answer = Translator().translate(answer, src="en", dest=language).text # Translation of model's text to user's language

        return answer

