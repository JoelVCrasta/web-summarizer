from transformers import BartTokenizer, BartForConditionalGeneration
from utils.file_open import open_file, read_text_from_file
from utils.scraper import get_scraped_data
import torch
import warnings
import logging

warnings.filterwarnings("ignore", category=FutureWarning, message="`clean_up_tokenization_spaces` was not set.")
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Initialize tokenizer and model
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn').to(device)

# -----------------------------------------------------------

def gen_sum(text: str, sum_len: str = 'medium') -> str:
    try:
        # Get the length settings
        settings = length_settings(sum_len)

        # Tokenize the input text
        inputs = tokenizer.encode(
            "summarize: " + text, 
            return_tensors="pt", 
            max_length=1024, 
            truncation=True
        ).to(device)
        
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
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise RuntimeError("An error occurred while generating the summary")
    
# -----------------------------------------------------------

def length_settings(sum_len):
    length_settings = {
        'short' :   {'max_length': 250, 'min_length': 100, 'length_penalty': 1.0},
        'medium':   {'max_length': 500, 'min_length': 250, 'length_penalty': 1.0},
        'long'  :   {'max_length': 1000, 'min_length': 500, 'length_penalty': 1.5}
    }
    settings = length_settings.get(sum_len)

    return settings
    
def summary(mode: int, text: str = '', url: str = '', sum_len: str = 'medium') -> str:
    if mode == 0:
        summary = gen_sum(text, sum_len)
        return summary
        
    elif mode == 1: 
        try:
            file_path = open_file()
            text = read_text_from_file(file_path)
            summary = gen_sum(text, sum_len)

            return summary
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise RuntimeError("An error occurred while generating the summary")
    
    elif mode == 2:
        tags = ['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'li']
        text = get_scraped_data(url, tags)
        summary = gen_sum(text, sum_len)

        return summary