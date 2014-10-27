import pyximport
pyximport.install()

from .wiki_markup_processing import to_raw_text, remove_brackets
from .word_tokenizer import split_sentences, split_and_group_sentences, split_punct