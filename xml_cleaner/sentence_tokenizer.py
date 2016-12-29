# -*- coding: utf-8 -*-
from .regular_expressions import word_with_alpha_and_period
from .quoted_expressions import group_quoted_tokens
from .constants import (
    PUNCT_SYMBOLS,
    CONTINUE_PUNCT_SYMBOLS
)
from .word_tokenizer import tokenize

def is_end_symbol(symbol):
    return (
        symbol[:2] in PUNCT_SYMBOLS
    )

def detect_sentence_boundaries(tokens):
    """
    Subdivide an input list of strings (tokens)
    into multiple lists according to detected
    sentence boundaries.

    ```
    detect_sentence_boundaries(
        ["Cat ", "sat ", "mat", ". ", "Cat ", "'s ", "named ", "Cool", "."]
    )
    #=> [
        ["Cat ", "sat ", "mat", ". "],
        ["Cat ", "'s ", "named ", "Cool", "."]
    ]
    ```

    Arguments:
    ----------

        tokens : list<str>

    Returns:
    --------
        list<list<str>> : original list subdivided into multiple
            lists according to (detected) sentence boundaries.
    """
    tokenized = group_quoted_tokens(tokens)
    words = []
    sentences = []
    for i in range(len(tokenized)):
        # this is a parenthetical:
        end_sentence = False
        if isinstance(tokenized[i], list):
            if len(words) == 0:
                # end if a sentence finishes inside quoted section,
                # and no sentence was begun beforehand
                if is_end_symbol(tokenized[i][-2].rstrip()):
                    end_sentence = True
            else:
                # end if a sentence finishes inside quote marks
                if (tokenized[i][0][0] == '"' and
                    is_end_symbol(tokenized[i][-2].rstrip()) and
                    not tokenized[i][1][0].isupper()):
                    end_sentence = True
            words.extend(tokenized[i])
        else:
            stripped_tokenized = tokenized[i].rstrip()
            if is_end_symbol(stripped_tokenized):
                words.append(tokenized[i])
                not_last_word = i + 1 != len(tokenized)
                next_word_lowercase = (
                    not_last_word and
                    tokenized[i+1][0].islower()
                )
                next_word_continue_punct = (
                    not_last_word and
                    tokenized[i+1][0] in CONTINUE_PUNCT_SYMBOLS
                )
                end_sentence = not (
                    not_last_word and
                    (
                        next_word_lowercase or
                        next_word_continue_punct
                    )
                )
            else:
                words.append(tokenized[i])
        if end_sentence:
            sentences.append(words)
            words = []

    # add final sentence, if it wasn't added yet.
    if len(words) > 0:
        sentences.append(words)

    # If the final word ends in a period:
    if len(sentences) > 0 and sentences[-1][-1]:
        alpha_word_piece = word_with_alpha_and_period.match(sentences[-1][-1])
        if alpha_word_piece:
            sentences[-1][-1] = alpha_word_piece.group(1)
            sentences[-1].append(alpha_word_piece.group(2))
    return sentences


def remove_whitespace(sentences):
    """
    Clear out spaces and newlines
    from the list of list of strings.

    Arguments:
    ----------
        sentences : list<list<str>>

    Returns:
    --------
        list<list<str>> : same strings as input,
            without spaces or newlines.
    """
    return [[w.rstrip() for w in sent] for sent in sentences]


def sent_tokenize(text, keep_whitespace=False, normalize_ascii=True):
    """
    Perform sentence + word tokenization on the input text
    using regular expressions and english/french specific
    rules.

    Arguments:
    ----------
        text : str, input string to tokenize
        keep_whitespace : bool, whether to strip out spaces
            and newlines.
        normalize_ascii : bool, perform some replacements
            on rare characters so that they become
            easier to process in a ascii pipeline
            (canonicalize dashes, replace œ -> oe, etc..)
    Returns:
    --------
        list<list<str>> : sentences with their content held
            in a list of strings for each token.
    """
    sentences = detect_sentence_boundaries(
        tokenize(
            text,
            normalize_ascii
        )
    )
    if not keep_whitespace:
        sentences = remove_whitespace(sentences)
    return sentences

