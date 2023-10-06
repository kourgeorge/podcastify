# Load model directly
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, T5ForConditionalGeneration

class AITextCleaner:
    _model = None
    _tokenizer = None
    _cleaning_model = 'prakharz/dial-flant5-xl'  # 'NousResearch/Nous-Hermes-13b'#

    @classmethod
    def initialize(cls):
        if cls._model is None:
            # Load the model only when it's first accessed
            cls._tokenizer = AutoTokenizer.from_pretrained(cls._cleaning_model)
            cls._model = AutoModelForSeq2SeqLM.from_pretrained(cls._cleaning_model)

    @classmethod
    def clean(cls, prompt):
        cls.initialize()
        inputs = AITextCleaner._tokenizer.encode(prompt, return_tensors="pt")
        outputs = AITextCleaner._model.generate(inputs, early_stopping=True, do_sample=False, max_new_tokens=2000)
        decoded_outputs = AITextCleaner._tokenizer.decode(outputs[0])
        return decoded_outputs