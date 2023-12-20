import re
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class Chatbot:
    def __init__(self, brain_path):
        self.model = AutoModelForCausalLM.from_pretrained(brain_path)
        self.tokenizer = AutoTokenizer.from_pretrained(brain_path)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.context  = ''
    def extract_bot_response(self, input_str):
        """Extracts the first bot response from a given input string.

        Args:
            input_str: A string containing the user's message and the bot's previous response.

        Returns:
            A string containing the bot's response, or None if no match is found.
        """

        pattern = r'bot\s*:\s*([^\n]+?)(?=\s*user\s*|$)'
        match = re.search(pattern, input_str, re.IGNORECASE)

        if match:
            bot_response = match.group(1).strip()
            return bot_response
        else:
            return None

    def reply(self, user_message):
        """Generates a bot response to a given user message.

        Args:
            user_message: A string containing the user's message.

        Returns:
            A string containing the bot's response.
        """
        
        input_str = f'user : ' + user_message + ' '
        inputs = self.tokenizer(input_str, return_tensors="pt")

        with torch.no_grad():
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            outputs = self.model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_new_tokens=64,
                eos_token_id=3
            )
            bot_response = self.tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)[0]
            bot_response = self.extract_bot_response(bot_response)
            self.context += bot_response + '\n'
            return bot_response

