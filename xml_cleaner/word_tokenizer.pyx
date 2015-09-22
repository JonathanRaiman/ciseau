import re

uppercased                   = re.compile("[A-ZÀ-Þ\W]")
word_with_period             = re.compile("^([\w\.]+)\.$")
word_with_alpha_and_period   = re.compile("^([^\.]+)\.$")
one_letter_long_or_repeating = re.compile("^(?:(?:[a-z])|(?:[a-z](?:\.[a-z])+))$", re.IGNORECASE)

website_like = re.compile("^((?:www\.)?[^\. ]+\.[^\. ]+(?:\.[^\./ ]+))$")

no_punctuation               = re.compile("^\w+$")
left_quote_shifter           = re.compile("`(?!`)(?=.*\w)") # substitute only once.
left_quote_converter         = re.compile('[«"](?=.*\w)')
left_single_quote_converter  = re.compile("(?:(\W|^))'(?=.*\w)")
right_single_quote_converter = re.compile("(\w)'(?!')(?=\W|$)")

dashes = ["–", "--+", "â\x80\x93"]
for i in range(8208, 8214):
    dashes.append(chr(i))
dash_converter               = re.compile("|".join(dashes))

semicolon_shifter            = re.compile("(.):([^/])")
comma_shifter                = re.compile(",(?!\d)")
remaining_quote_converter    = re.compile('["“”»]')
shifted_ellipses             = re.compile("(\.\.\.+|…)")
shifted_brackets             = re.compile("([\(\[\{\}\]\)])")
shifted_parenthesis_squiggly_brackets = re.compile("([\(\{\}\)])")
shifted_standard_punctuation = re.compile("([\!\?#\$%;~|])")
period_mover                 = re.compile("([a-zA-ZÀ-Þ]{2})([\./])\s+([a-zA-ZÀ-Þ]{2})") # glued periods.

english_specific_appendages = re.compile("([A-Za-z])['’]([dms])\\b")
english_nots = re.compile("n['’]t\\b")
english_contractions = re.compile("['’](ve|ll|re)\\b")
french_appendages = re.compile("(\\b[tjnlsmdclTJNLSMLDC]|qu)['’](?=[^tdms])")

people = [
        "jr", "mr", "ms", "mrs", "dr", "prof", "esq", "sr",
        "sen", "sens", "rep", "reps", "gov", "attys", "attys",
        "supt", "det", "mssrs", "rev"]
army   = ["col", "gen", "lt", "cmdr", "adm", "capt", "sgt", "cpl", "maj", "brig"]
inst   = ["dept","univ", "assn", "bros", "ph.d"]
place  = [
    "arc", "al", "ave", "blvd", "bld", "cl", "ct",
    "cres", "exp", "expy", "dist", "mt", "mtn", "ft",
    "fy", "fwy", "hwy", "hway", "la", "pde", "pd","plz", "pl", "rd", "st", "tce"]
comp   = ["mfg", "inc", "ltd", "co", "corp"]
state  = [
    "ala","ariz","ark","cal","calif","colo","col","conn",
    "del","fed","fla","ga","ida","id","ill","ind","ia","kans",
    "kan","ken","ky","la","me","md","is","mass","mich","minn",
    "miss","mo","mont","neb","nebr","nev","mex","okla","ok",
    "ore","penna","penn","pa","dak","tenn","tex","ut","vt",
    "va","wash","wis","wisc","wy","wyo","usafa","alta",
    "man","ont","que","sask","yuk"]
month  =  ["jan","feb","mar","apr","may","jun","jul","aug","sep","sept","oct","nov","dec"]
misc   = ["vs","etc", "no","esp", "ed", "iv", "Oper", ""]
website = ["www"]
abbr   = {}

period           = '.'
ellipsis         = "..."
question_mark    = "?"
exclamation_mark = "!"

PUNCT_SYMBOLS = set([period, ellipsis, question_mark, exclamation_mark])

# create a hash of these abbreviations:
for abbreviation_type in [people, army, inst, place, comp, state, month, misc, website]:
    for abbreviation in abbreviation_type:
        abbr[abbreviation] = True

cdef list _split_and_group_sentences(list array):
    cdef list tokenized = array
    cdef list words = []
    cdef list sentences = []
    cdef int i = 0
    cdef int length = len(tokenized)
    for i in range(length):
        if tokenized[i] in PUNCT_SYMBOLS:
            words.append(tokenized[i])
            sentences.append(words)
            words = []
        else:
            potential_last_word = word_with_period.match(tokenized[i])
            if potential_last_word is not None:
                # Don't separate the period off words that
                # meet any of the following conditions:
                #
                # 1. It is defined in one of the lists above
                # 2. It is only one letter long: Alfred E. Sloan
                # 3. It has a repeating letter-dot: U.S.A. or J.C. Penney


                word_without_final_period = potential_last_word.group(1)

                likely_abbreviation = abbr.get(word_without_final_period.lower()) or \
                        one_letter_long_or_repeating.match(word_without_final_period)

                likely_last_word = len(tokenized) == i+1

                next_word_uppercase = len(tokenized) > i+1 and tokenized[i + 1] and uppercased.match(tokenized[i + 1])

                end_sentence = False

                if next_word_uppercase:
                    if likely_abbreviation:
                        words.append(tokenized[i])
                    else:
                        words.append(word_without_final_period)
                        end_sentence = True
                else:
                    if likely_last_word:
                        end_sentence = True
                    if likely_abbreviation:
                        words.append(tokenized[i])
                    else:
                        words.append(word_without_final_period)

                if end_sentence:
                    words.append(period)
                    sentences.append(words)
                    words = []
            else:
                words.append(tokenized[i])

    # add final sentence, if it wasn't added yet.
    if len(words) > 0:
        sentences.append(words)

    # If the final word ends in a period:
    if len(sentences) > 0 and sentences[-1][-1]:
        alpha_word_piece = word_with_alpha_and_period.match(sentences[-1][-1])
        if alpha_word_piece:
            sentences[-1][-1] = alpha_word_piece.group(1)
            sentences[-1].append(period)
    return sentences

def split_and_group_sentences(list array):
    return _split_and_group_sentences(array)

cdef list _split_sentences(list array):
    cdef list tokenized = array
    cdef list words = []
    cdef int i = 0
    cdef int length = len(tokenized)
    for i in range(length):
        abbreviation_match = word_with_period.match(tokenized[i])
        if tokenized[i + 1] and uppercased.match(tokenized[i + 1]) and abbreviation_match:
            word_without_final_period = abbreviation_match.group(1)
            # Don't separate the period off words that
            # meet any of the following conditions:
            #
            # 1. It is defined in one of the lists above
            # 2. It is only one letter long: Alfred E. Sloan
            # 3. It has a repeating letter-dot: U.S.A. or J.C. Penney
            if not abbr.get(word_without_final_period.downcase) \
            and not one_letter_long_or_repeating.match(word_without_final_period):
                words.append(word_without_final_period)
                words.append(period)
                continue
        words.append(tokenized[i])
    # If the final word ends in a period..

    if len(words) > 0 and words[-1]:
        alpha_word_piece = word_with_alpha_and_period.match(words[-1])
        if alpha_word_piece:
            words[-1] = alpha_word_piece.group(1)
            words.append(period)
    return words

def split_sentences(list array):
    return _split_sentences(array)

def split_punct(str text):
    return _split_punct(text)

cdef list _split_punct_keep_brackets(str text):
    # If there's no punctuation, return immediately
    if no_punctuation.match(text):
        return [text]

        # Shift off other ``standard'' punctuation
        # Shift off brackets

        # Shift semicolons off
        # Shift ellipses off
        # Shift commas off everything but numbers
        # Convert and separate dashes
        # Separate right single quotes
        # Convert (remaining) quotes to ''
        # Convert left quotes to `
        # Convert left quotes to ``
        # shift quotes left.
        # Put quotes into a standard format
    return french_appendages.sub("\g<1>' ",                                                     \
            shifted_standard_punctuation.sub(" \g<1> ",                                         \
                shifted_parenthesis_squiggly_brackets.sub(" \g<1> ",                            \
                    shifted_ellipses.sub(" ...",                                                \
                        semicolon_shifter.sub("\g<1> : \g<2>",                                  \
                            comma_shifter.sub(" , ",                                            \
                                dash_converter.sub(" - ",                                       \
                                    right_single_quote_converter.sub("\g<1> ' ",                \
                                        english_specific_appendages.sub("\g<1> '\g<2>",         \
                                            english_contractions.sub(" '\g<1>",                 \
                                                english_nots.sub(" n't",                        \
                                                    remaining_quote_converter.sub(" '' ",           \
                                                        left_single_quote_converter.sub("\g<1> ` ", \
                                                            left_quote_converter.sub(" `` ",        \
                                                                left_quote_shifter.sub("` ",        \
                                                                    period_mover.sub("\g<1> \g<2> \g<3>",
                                                                        period_mover.sub("\g<1> \g<2> \g<3>",
                                                                            text))))))))))))))))).replace("œ", "oe").replace("æ", "ae").split()

shorthand_symbol = "**§**"

cdef str protect_shorthand(str text):
    words = text.split()
    out_words = []
    total_words = len(words)
    for i, word in enumerate(words):
        if word.endswith("."):
            if word[:-1].lower() in abbr:
                if i == total_words - 1:
                    continue
                else:
                    if words[i+1][0].isupper() or words[i+1] in PUNCT_SYMBOLS:
                        out_words.append(word[:-1] + shorthand_symbol)
                        continue
        out_words.append(word)
    return " ".join(out_words)

cdef str undo_shorthand(str text):
    return text.replace(shorthand_symbol, ".")

cdef list _split_punct(str text):
    # If there's no punctuation, return immediately
    if no_punctuation.match(text):
        return [text]

        # Shift off other ``standard'' punctuation
        # Shift off brackets

        # Shift semicolons off
        # Shift ellipses off
        # Shift commas off everything but numbers
        # Convert and separate dashes
        # Separate right single quotes
        # Convert (remaining) quotes to ''
        # Convert left quotes to `
        # Convert left quotes to ``
        # shift quotes left.
        # Put quotes into a standard format
    return undo_shorthand(
        french_appendages.sub("\g<1>' ",                                                        \
            shifted_standard_punctuation.sub(" \g<1> ",                                         \
                shifted_brackets.sub(" \g<1> ",                                                 \
                    shifted_ellipses.sub(" ...",                                                \
                        semicolon_shifter.sub("\g<1> : \g<2>",                                  \
                            comma_shifter.sub(" , ",                                            \
                                dash_converter.sub(" - ",                                       \
                                    right_single_quote_converter.sub("\g<1> ' ",                \
                                        english_specific_appendages.sub("\g<1> '\g<2>",         \
                                            english_contractions.sub(" '\g<1>",                 \
                                                english_nots.sub(" n't",                        \
                                                    remaining_quote_converter.sub(" '' ",           \
                                                        left_single_quote_converter.sub("\g<1> ` ", \
                                                            left_quote_converter.sub(" `` ",        \
                                                                left_quote_shifter.sub("` ",        \
                                                                    period_mover.sub("\g<1> \g<2> \g<3>",
                                                                        protect_shorthand(text)))))))))))))))))).replace("œ", "oe").replace("æ", "ae").split()

cdef list _split_and_group_sentences_using_text(str text):
    return split_and_group_sentences(_split_punct(text))

def split_and_group_sentences_using_text_keep_brackets(str text):
    return _split_and_group_sentences(_split_punct_keep_brackets(text))

def split_and_group_sentences_using_text(str text):
    return _split_and_group_sentences(_split_punct(text))

    # English-specific contractions (let's not be that specific)
    # text = text.gsub(/([A-Za-z])'([dms])\b/o){$1 + " '" + $2}  # Separate off 'd 'm 's
    # text = text.gsub(/n't\b/o, " n't")                     # Separate off n't
    # text = text.gsub(/'(ve|ll|re)\b/o){" '" + $1}         # Separate off 've, 'll, 're
