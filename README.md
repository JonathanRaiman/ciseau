XML cleaner
-----------

Utilities for tokenizing and cleaning up xml text.

Usage
-----

Parse and tokenize sentence and words in sentences:

	> [sentence for sentence in xml_cleaner.to_raw_text("Joey was a great sailor.")]
	#=> [["Joey", "was", "a", "great", "sailor", "."]]
