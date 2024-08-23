from transformers import BartTokenizer, BartForConditionalGeneration
import warnings

warnings.filterwarnings("ignore", category=FutureWarning, message="`clean_up_tokenization_spaces` was not set.")

# Initialize tokenizer and model
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')


def gen_sum(text: str, sum_len: str = 'medium') -> str:
    # Length settings
    length_settings = {
        'short' :   {'max_length': 100, 'min_length': 50, 'length_penalty': 1.0},
        'medium':   {'max_length': 200, 'min_length': 100, 'length_penalty': 1.0},
        'long'  :   {'max_length': 500, 'min_length': 200, 'length_penalty': 1.5}
    }
    settings = length_settings.get(sum_len)

    # Tokenize the input text
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    
    # Generate the summary
    sum_ids = model.generate(
        inputs, 
        max_length=settings['max_length'], 
        min_length=settings['min_length'], 
        length_penalty=settings['length_penalty'], 
        num_beams=4, 
        early_stopping=True
    )
    
    # Decode the generated summary
    summary = tokenizer.decode(sum_ids[0], skip_special_tokens=True)
    
    return summary

def read_text_from_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

if __name__ == '__main__':
    file_path = 'tests/text.txt'
    sum_len = 'short'
    
    try:
        text = read_text_from_file(file_path)

        result = gen_sum(text, sum_len)
        print(result)
    except Exception as e:
        print(f"An error occurred: {e}")
