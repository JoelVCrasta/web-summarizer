from transformers import BartTokenizer, BartForConditionalGeneration
from utils.scraper import get_scraped_data
import torch
import warnings
import logging

warnings.filterwarnings("ignore", category=FutureWarning, message="`clean_up_tokenization_spaces` was not set.")
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MAX_TEXT_INPUT_LEN = 2000

# Initialize tokenizer and model
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn').to(device)

# -----------------------------------------------------------

def gen_sum(text: str, sumlen: int) -> str:
    try:
        # Get the length settings
        settings = length_settings(sumlen)

        # Tokenize the input text
        inputs = tokenizer.encode(
            text, 
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

def length_settings(sum_len: str) -> dict:
    length_settings = {
        0 :   {'max_length': 250, 'min_length': 100, 'length_penalty': 1.0},
        1 :   {'max_length': 500, 'min_length': 250, 'length_penalty': 1.0},
        2 :   {'max_length': 1000, 'min_length': 500, 'length_penalty': 1.5}
    }

    return length_settings.get(sum_len, length_settings[1])
    
def summary(mode: int, text: str = '', sumlen: int = 1) -> str:
    if mode in [0, 2]:
        return gen_sum(text, sumlen)
        
    elif mode == 1:
        tags = ['p', 'ul', 'ol', 'li']  
        text = get_scraped_data(text, tags)
        text = text[:MAX_TEXT_INPUT_LEN]
        return gen_sum(text, sumlen)