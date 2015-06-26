"""
Module for XML cleaning and text tokenization.

Usage
-----

> [sentence for sentence in xml_cleaner.to_raw_text("Joey was a great sailor.")]
#=> [["Joey", "was", "a", "great", "sailor", "."]]

"""
import pyximport
pyximport.install()

from .wiki_markup_processing import to_raw_text, to_raw_text_markupless, remove_brackets, to_raw_text_pairings, tokenize
from .word_tokenizer import split_sentences, split_and_group_sentences, split_punct

__all__ = [
	"to_raw_text",
	"to_raw_text_markupless",
	"remove_brackets",
	"to_raw_text_pairings",
	"split_sentences",
	"split_and_group_sentences",
    "tokenize",
	"split_punct"]
