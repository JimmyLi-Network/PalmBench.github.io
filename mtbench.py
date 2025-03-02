from openai import OpenAI
import re
import json

# Initialize the OpenAI client with the API key
client = OpenAI(
    api_key=,
)

def format_prompt(question, answer):
    """
    Generates a formatted prompt using the provided template.
    """
    template = ("[Instruction]\n"
                "Please act as an impartial judge and evaluate the quality of the response provided by an AI assistant to the user question displayed below. "
                "Your evaluation should consider factors such as the helpfulness, relevance, accuracy, depth, creativity, and level of detail of the response. "
                "Begin your evaluation by providing a short explanation. Be as objective as possible. After providing your explanation, you must rate the response on a scale of 1 to 10 by strictly following this format: \"[[rating]]\", for example: \"Rating: [[5]]\".\n\n"
                "[Question]\n{question}\n\n"
                "[The Start of Assistant's Answer]\n{answer}\n"
                "[The End of Assistant's Answer]")
    return template.format(question=question, answer=answer)

def get_response_from_gpt(question, answer):
    """
    Sends a formatted request to GPT-4 and extracts the score from the response.
    """
    formatted_prompt = format_prompt(question, answer)
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": formatted_prompt,
            }
        ],
    )

    # Correctly access the response content
    response_text = response.choices[0].message.content

    # Extract score using regular expression
    # score_match = re.search(r"\[\[(\d+(\.\d+)?)\]\]", response_text)
    score_match = re.search(r"\[\[(\d+(\.\d+)?)\]\]", response_text)
    if score_match:
        score = score_match.group(1)
        score = float(score)
        # print(f"Extracted score from response: {score}")
    else:
        # print("No score found in the response.")
        score = 0.3

    return score


def evaluate_questions(questions, context):
    total_score = 0
    scores = []
    
    for question in questions:
        answer = get_answer_on_device(question, context, model='llama2:7b-chat-q2_K')
        score = get_response_from_gpt(question, answer)
        if score is not None:
            scores.append(score)
            total_score += score
    
    if scores:
        average_score = total_score / len(scores)
    else:
        average_score = 0
    
    return average_score, total_score, scores

def clean_text(text):
    text = text.strip()  
    text = re.sub(r'\s+', ' ', text)  
    text = re.sub(r'[^\w\s]', '', text)  
    return text.lower()  

if __name__ == "__main__":
    # Example usage
    scores_writing = []
    scores_roleplay = []
    scores_reasoning = []
    scores_stem = []
    scores_humanities = []
    scores_extraction = []
    scores_math = []
    scores_coding = []
    scores = []

    with open("question.jsonl", 'r') as file:
        for line in file:
            data = json.loads(line)
            question = data.get("turns")[0]
            category_value = data.get("category")
            context = "Please act as an impartial judge and evaluate the quality of the response provided by an AI assistant to the user question displayed below. Your evaluation should consider factors such as the helpfulness, relevance, accuracy, depth, creativity, and level of detail of the response."  
            answer = get_answer_on_device(question, context,'llama3.2:3b-instruct-q4_K_M')
            score = get_response_from_gpt(question, answer)
            score = float(score)
            #if score and category_value == "writing":
            if score:
                scores.append(score)

                if category_value == "writing":
                    scores_writing.append(score)
                    print(f"Writing:{score}")
                elif category_value == "roleplay":
                    scores_roleplay.append(score)
                    print(f"Roleplay:{score}")
                elif category_value == "reasoning": 
                    scores_reasoning.append(score)
                    print(f"Reasoning:{score}")
                elif category_value == "stem": 
                    scores_stem.append(score)
                    print(f"STEM:{score}")
                elif category_value == "humanities": 
                    scores_humanities.append(score)
                    print(f"Humanities:{score}")
                elif category_value == "coding": 
                    scores_coding.append(score)
                    print(f"Coding:{score}")
                elif category_value == "extraction": 
                    scores_extraction.append(score)
                    print(f"Extraction:{score}")
                elif category_value == "math": 
                    scores_math.append(score)
                    print(f"Math:{score}")

    # Calculate and print statistics
    if scores_writing or scores_roleplay or scores_reasoning:
        average_score_writing = sum(scores_writing) / len(scores_writing)
        print(f"Average writing Score: {average_score_writing}")

        average_score_roleplay = sum(scores_roleplay) / len(scores_roleplay)
        print(f"Average roleplay Score: {average_score_roleplay}")

        average_score_reasoning = sum(scores_reasoning) / len(scores_reasoning)
        print(f"Average reasoning Score: {average_score_reasoning}")

        average_score_math = sum(scores_math) / len(scores_math)
        print(f"Average math Score: {average_score_math}")

        average_score_coding = sum(scores_coding) / len(scores_coding)
        print(f"Average coding Score: {average_score_coding}")

        average_score_extraction = sum(scores_extraction) / len(scores_extraction)
        print(f"Average extraction Score: {average_score_extraction}")

        average_score_stem = sum(scores_stem) / len(scores_stem)
        print(f"Average stem Score: {average_score_stem}")

        average_score_humanities = sum(scores_humanities) / len(scores_humanities)
        print(f"Average humanities Score: {average_score_humanities}")

        average_score = sum(scores)   / len(scores)
        print(f"Average Score: {average_score}")
    else:
        print("No scores were calculated.")









