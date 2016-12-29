# -*- coding: utf-8 -*-
import re
from .constants import (
    PUNCT_SYMBOLS,
    ABBR,
    MONTHS,
    UNDECIDED,
    SHOULD_SPLIT,
    SHOULD_NOT_SPLIT
)
from .regular_expressions import (
    word_with_period,
    no_punctuation,
    numerical_expression,
    repeated_dash_converter,
    dash_converter,
    pure_whitespace,
    left_quote_shifter,
    left_quote_converter,
    one_letter_long_or_repeating,
    left_single_quote_converter,
    remaining_quote_converter,
    english_nots,
    english_contractions,
    english_specific_appendages,
    french_appendages,
    right_single_quote_converter,
    simple_dash_finder,
    advanced_dash_finder,
    url_file_finder,
    shifted_ellipses,
    shifted_standard_punctuation
)


def protect_shorthand(text, split_locations):
    """
    Annotate locations in a string that contain
    periods as being true periods or periods
    that are a part of shorthand (and thus should
    not be treated as punctuation marks).

    Arguments:
    ----------
        text : str
        split_locations : list<int>, same length as text.
    """
    word_matches = list(re.finditer(word_with_period, text))
    total_words = len(word_matches)

    for i, match in enumerate(word_matches):
        match_start = match.start()
        match_end = match.end()
        for char_pos in range(match_start, match_end):
            if split_locations[char_pos] == SHOULD_SPLIT and match_end - char_pos > 1:
                match_start = char_pos
        word = text[match_start:match_end]

        if not word.endswith('.'):
            # ensure that words contained within other words:
            # e.g. 'chocolate.Mountains of'  -> 'chocolate. Mountains of'
            if (not word[0].isdigit() and
                split_locations[match_start] == UNDECIDED):
                split_locations[match_start] = SHOULD_SPLIT
            continue
        period_pos = match_end - 1
        # this is not the last word, abbreviation
        # is not the final period of the sentence,
        # moreover:
        word_is_in_abbr = word[:-1].lower() in ABBR
        is_abbr_like = (
            word_is_in_abbr or
            one_letter_long_or_repeating.match(word[:-1]) is not None
        )
        is_digit = False if is_abbr_like else word[:-1].isdigit()

        is_last_word = i == (total_words - 1)
        is_ending = is_last_word and (match_end == len(text) or text[match_end:].isspace())
        is_not_ending = not is_ending
        abbreviation_and_not_end = (
            len(word) > 1 and
            is_abbr_like and
            is_not_ending
        )

        if abbreviation_and_not_end and (
                (not is_last_word and word_matches[i+1].group(0)[0].islower()) or
                (not is_last_word and word_matches[i+1].group(0) in PUNCT_SYMBOLS) or
                word[0].isupper() or
                word_is_in_abbr or
                len(word) == 2):
            # next word is lowercase (e.g. not a new sentence?), or next word
            # is punctuation or next word is totally uppercase (e.g. 'Mister.
            # ABAGNALE called to the stand')
            if split_locations[period_pos] == SHOULD_SPLIT and period_pos + 1 < len(split_locations):
                split_locations[period_pos + 1] = SHOULD_SPLIT
            split_locations[period_pos] = SHOULD_NOT_SPLIT
        elif (is_digit and
              len(word[:-1]) <= 2 and
              not is_last_word and
              word_matches[i+1].group(0).lower() in MONTHS):
            # a date or weird number with a period:
            if split_locations[period_pos] == SHOULD_SPLIT and period_pos + 1 < len(split_locations):
                split_locations[period_pos + 1] = SHOULD_SPLIT
            split_locations[period_pos] = SHOULD_NOT_SPLIT
        elif split_locations[period_pos] == UNDECIDED:
            # split this period into its own segment:
            split_locations[period_pos] = SHOULD_SPLIT


def split_with_locations(text, locations):
    """
    Use an integer list to split the string
    contained in `text`.

    Arguments:
    ----------
        text : str, same length as locations.
        locations : list<int>, contains values
            'SHOULD_SPLIT', 'UNDECIDED', and
            'SHOULD_NOT_SPLIT'. Will create
            strings between each 'SHOULD_SPLIT'
            locations.
    Returns:
    --------
        Generator<str> : the substrings of text
            corresponding to the slices given
            in locations.
    """
    start = 0
    for pos, decision in enumerate(locations):
        if decision == SHOULD_SPLIT:
            if start != pos:
                yield text[start:pos]
            start = pos
    if start != len(text):
        yield text[start:]


def mark_regex(regex, text, split_locations):
    """
    Regex that adds a 'SHOULD_SPLIT' marker at the end
    location of each matching group of the given regex.

    Arguments
    ---------
        regex : re.Expression
        text : str, same length as split_locations
        split_locations : list<int>, split decisions.
    """
    for match in regex.finditer(text):
        end_match = match.end()
        if end_match < len(split_locations):
            split_locations[end_match] = SHOULD_SPLIT


def mark_begin_end_regex(regex, text, split_locations):
    """
    Regex that adds a 'SHOULD_SPLIT' marker at the end
    location of each matching group of the given regex,
    and adds a 'SHOULD_SPLIT' at the beginning of the
    matching group. Each character within the matching
    group will be marked as 'SHOULD_NOT_SPLIT'.

    Arguments
    ---------
        regex : re.Expression
        text : str, same length as split_locations
        split_locations : list<int>, split decisions.
    """
    for match in regex.finditer(text):
        end_match = match.end()
        begin_match = match.start()

        for i in range(begin_match+1, end_match):
            split_locations[i] = SHOULD_NOT_SPLIT
        if end_match < len(split_locations):
            if split_locations[end_match] == UNDECIDED:
                split_locations[end_match] = SHOULD_SPLIT
        if split_locations[begin_match] == UNDECIDED:
            split_locations[begin_match] = SHOULD_SPLIT


def tokenize(text, normalize_ascii=True):
    """
    Convert a single string into a list of substrings
    split along punctuation and word boundaries. Keep
    whitespace intact by always attaching it to the
    previous token.

    Arguments:
    ----------
        text : str
        normalize_ascii : bool, perform some replacements
            on non-ascii characters to canonicalize the
            string (defaults to True).

    Returns:
    --------
        list<str>, list of substring tokens.
    """
    # 1. If there's no punctuation, return immediately
    if no_punctuation.match(text):
        return [text]
    # 2. let's standardize the input text to ascii (if desired)
    # Note: this will no longer respect input-to-output character positions
    if normalize_ascii:
        # normalize these greco-roman characters to ascii:
        text = text.replace(u"œ", "oe").replace(u"æ", "ae")
        # normalize dashes:
        text = repeated_dash_converter.sub("-", text)
    # 3. let's construct an integer array of the possible split locations:
    split_locations = [UNDECIDED] * len(text)
    regexes = (
        pure_whitespace,
        left_quote_shifter,
        left_quote_converter,
        left_single_quote_converter,
        remaining_quote_converter,
        # regex can't fix this -> regex ca n't fix this
        english_nots,
        # you'll dig this -> you 'll dig this
        english_contractions,
        # the rhino's horns -> the rhino 's horns
        english_specific_appendages,
        # qu'a tu fais au rhino -> qu ' a tu fais au rhino,
        french_appendages
    )
    # 4. Mark end locations for specific regular expressions:
    for regex in regexes:
        mark_regex(regex, text, split_locations)

    begin_end_regexes = (
        right_single_quote_converter,
        # use dashes as the breakpoint:
        # the rhino--truck -> the rhino -- truck
        simple_dash_finder if normalize_ascii else advanced_dash_finder,
        numerical_expression,
        url_file_finder,
        shifted_ellipses,
        # the #rhino! -> the # rhino ! ;
        # the rino[sic] -> the rino [ sic ]
        shifted_standard_punctuation
    )

    # 5. Mark begin and end locations for other regular expressions:
    for regex in begin_end_regexes:
        mark_begin_end_regex(regex, text, split_locations)

    # 6. Remove splitting on exceptional uses of periods:
    # I'm with Mr. -> I 'm with Mr. , I'm with Mister. -> I 'm with Mister .
    protect_shorthand(text, split_locations)

    if normalize_ascii:
        text = dash_converter.sub("-", text)
    # 7. Return the split string using the integer list:
    return list(split_with_locations(text, split_locations))
