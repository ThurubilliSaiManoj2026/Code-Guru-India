# core/translator.py
from config.languages import LANGUAGE_CONFIG

class MultiLanguageTranslator:
    def __init__(self):
        print("Loading IndicTrans2 model... (first time takes 2-3 minutes)")
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        import torch

        # English → Indian languages
        en_indic = "ai4bharat/indictrans2-en-indic-dist-200M"
        self.en_indic_tokenizer = AutoTokenizer.from_pretrained(
            en_indic, trust_remote_code=True
        )
        self.en_indic_model = AutoModelForSeq2SeqLM.from_pretrained(
            en_indic, trust_remote_code=True
        )

        # Indian languages → English
        indic_en = "ai4bharat/indictrans2-indic-en-dist-200M"
        self.indic_en_tokenizer = AutoTokenizer.from_pretrained(
            indic_en, trust_remote_code=True
        )
        self.indic_en_model = AutoModelForSeq2SeqLM.from_pretrained(
            indic_en, trust_remote_code=True
        )
        print("✅ Translator loaded!")

    def to_english(self, text, source_language):
        """Telugu/Tamil/Hindi → English"""
        import torch
        lang_code = LANGUAGE_CONFIG[source_language]["code"]
        input_text = f"{lang_code} eng_Latn {text}"
        inputs = self.indic_en_tokenizer(
            input_text, return_tensors="pt", padding=True
        )
        with torch.no_grad():
            outputs = self.indic_en_model.generate(
                **inputs, max_length=512
            )
        return self.indic_en_tokenizer.decode(
            outputs[0], skip_special_tokens=True
        )

    def from_english(self, text, target_language):
        """English → Telugu/Tamil/Hindi"""
        import torch
        lang_code = LANGUAGE_CONFIG[target_language]["code"]
        input_text = f"eng_Latn {lang_code} {text}"
        inputs = self.en_indic_tokenizer(
            input_text, return_tensors="pt", padding=True
        )
        with torch.no_grad():
            outputs = self.en_indic_model.generate(
                **inputs, max_length=512
            )
        return self.en_indic_tokenizer.decode(
            outputs[0], skip_special_tokens=True
        )