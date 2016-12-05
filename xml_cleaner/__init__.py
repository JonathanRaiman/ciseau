"""
Module for XML cleaning and text tokenization.

Usage
-----

> xml_cleaner.tokenize("Joey was a great sailor.")
#=> [["Joey", "was", "a", "great", "sailor", "."]]

"""

from .wiki_markup_processing import (
    to_raw_text,
    to_raw_text_markupless,
    to_raw_text_pairings
)
from .word_tokenizer import tokenize
from .sentence_tokenizer import sent_tokenize

__all__ = [
    "to_raw_text",
    "to_raw_text_markupless",
    "to_raw_text_pairings",
    "sent_tokenize",
    "tokenize"
]
