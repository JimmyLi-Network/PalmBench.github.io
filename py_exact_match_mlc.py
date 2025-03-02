from evaluate import load
from datasets import load_dataset, Features, Value, Sequence
import evaluate
import re
from transformers import pipeline
from datasets import Dataset
from palmbench import inferface

def get_answer_on_device(question, context, model='llama2:7b-chat-q4_0'):
    # 
    response = inferface.connect('Pixel5a')
    
    answer_text = response['message']['content']  
    return answer_text

def clean_text(text):
    text = text.strip()  
    text = re.sub(r'\s+', ' ', text)  
    text = re.sub(r'[^\w\s]', '', text)  
    return text.lower()  

def create_samples(prediction_text, reference_text, answer_start, question_id):
    predictions = {
        'prediction_text': prediction_text,
        'id': question_id
    }

    references = {
        'answers': {
            'answer_start': [answer_start],
            'text': [reference_text]
        },
        'id': question_id
    }
    
    return predictions, references

predictions = []
references = []

if __name__ == "__main__":

	dataset = load_dataset("squad")
	squad_metric = load("squad")


	for i in range(55):
		sample = dataset["validation"][i+1]
		question = sample["question"]
		context = sample["context"]
		#refs = sample["answers"]["text"]
		refs = get_answer_on_device(question, context,'llama2:7b-chat-fp16')

		print("Question:", question)
		print("Answer:", refs)

		answer = get_answer_on_device(question, context,'llama2:7b-chat-q5_K_M')
		print(answer)

		prediction_text = answer
		reference_text = refs

		answer_start = sample["answers"]["answer_start"][0]
		question_id = sample['id']

		predict_sample, refer_sample = create_samples(prediction_text, reference_text, answer_start, question_id)
		print(predict_sample)
		print(type(predict_sample))
		#exact_match = evaluate.load("exact_match")
		#results = exact_match.compute(references=references, predictions=predictions)

		#print(round(results["exact_match"], 2))   
		references.append(refer_sample)
		predictions.append(predict_sample)


	results = squad_metric.compute(predictions=predictions, references=references)
	print(results)



