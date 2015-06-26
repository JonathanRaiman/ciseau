import re
import pyximport
pyximport.install()
import word_tokenizer

bracket_parser           = re.compile("\[\[(?P<name>[^\]\|]+)(?:\|[\W]*(?P<trigger>[^\]\#\|]+)(?:\#[^\]\|]+)?)*\]\]")
squiggly_bracket_parser  = re.compile("{{([^}]+)}}")
table_parser             = re.compile("{\|[^}]+\|}")
mvar_parser              = re.compile("{{\d*mvar\d*\|([^}]+)}}")
remove_emphasis          = re.compile("'{2,5}([^']+)'{2,5}")

# handles links that don't have a pipe sign"
double_bracket_parser    = re.compile("\[\[|\]\]")
# normalizes: 01/02/2003, 2005-06-07, and 2001 type dates to 7777
date_remover              = re.compile("((\d{4}(?:[-/]\d{2}[-/]\d{2})?)|(\d{2}(?:[-/]\d{2}[-/]\d{4})))(?=[^\d]|$)")
remove_emphasis_asterix   = re.compile("\*{2,5}([^\*]+)\*{2,5}")
remove_emphasis_slash     = re.compile("/{2,5}([^/]+)/{2,5}")
remove_emphasis_low_ticks = re.compile(",{2,5}([^,]+),{2,5}")
remove_emphasis_heading   = re.compile("={2,5}([^=]+)={2,5}")
remove_emphasis_strikethrough = re.compile("~{2}([^~]+)~{2}")
remove_emphasis_underline = re.compile("_{2}([^_]+)_{2}")
remove_bullets_nbsps      = re.compile("(&amp;nbsp;|&nbsp;|[\^\n]\*{1,}|[\^\n]\#{1,}|[\^\n]:{1,})") # remove lists, bullet points, and html no breakspace
remove_wikipedia_link     = re.compile("\[\W*http[^\] ]+\b*(?P<anchor>[^\]]+)\]")
markup_normalizer         = re.compile("[',/\*_=-]{2,5}")
markup_removes            = [remove_emphasis, remove_emphasis_heading, remove_emphasis_asterix, remove_emphasis_slash, remove_emphasis_low_ticks, remove_emphasis_strikethrough, remove_emphasis_underline]
replacer                  = lambda matches: matches.group('trigger') if matches.group('trigger') != None else matches.group('name')
anchor_replacer           = lambda matches: matches.group('anchor') if matches.group('anchor') else ''
html_remover              = re.compile("<[^>]+>")
internal_html_remover     = re.compile("{{[^(}})]+}}")
math_source_sections      = re.compile("<(math|source|code|sub|sup)[^>]*>([^<]*)</(math|source|code|sub|sup)>")
greater_than              = re.compile("(\W)>(\W)")
less_than                 = re.compile("<([^\w/])")
single_internal_link      = re.compile("\[\[([^\]\|]+)\]\]")
category_internal_link    = re.compile("\[\[Category:([^\]\|]+)\]\]")

# handles links that always have a pipe sign e.g. "[[the girl|Angelina Jolie]]"
anchortag_internal_link   = re.compile("\[\[(?P<target>[^\]\|]+)\|[\W]*(?P<anchor>[^\]\#\|]+)(?:\#[^\]\|]+)?\]\]")
url_remover               = re.compile("http://[a-zA-Z\.&/]+")
cdef str empty_space = " "
cdef str empty_string = ""

cdef str remove_dates(str text):
    return date_remover.sub("7777", text)

cdef str remove_html(str text):
    return html_remover.sub(empty_space, text)

cdef str remove_markup(str text):
    return markup_normalizer.sub(empty_string, text)

cdef str reintroduce_less_than(str text):
    #return text
    return less_than.sub("&lt;\g<1>", text)
cdef str reintroduce_greater_than(text):
    #return text
    return greater_than.sub("\g<1>&gt;\g<2>", text)
cdef str reintroduce_less_than_greater_than(text):
    return reintroduce_less_than(reintroduce_greater_than(text))

cdef str remove_math_sections(str text):
    return math_source_sections.sub(empty_space, reintroduce_less_than_greater_than(text))

cdef str _remove_brackets(str text):
    return anchortag_internal_link.sub("\g<anchor>", (single_internal_link.sub("\g<1>", category_internal_link.sub("\n\g<1> .\n", text))))

cdef str _remove_table(str text):
    return table_parser.sub(empty_space, text)

cdef str _remove_squiggly_bracket(str text):
    return squiggly_bracket_parser.sub(empty_space, text)

cdef str _remove_mvar(str text):
    return mvar_parser.sub("\g<1>", text)

cdef str _remove_remaining_double_brackets(str text):
    return double_bracket_parser.sub(empty_space, text)

cdef str _remove_urls(str text):
    return url_remover.sub("url", text)

def remove_brackets(str text):
    return _remove_remaining_double_brackets(_remove_brackets(text))

cdef list process_text(str text):
    # tokens = word_tokenizer.split_punct(text)
    # word_tokenizer.split_and_group_sentences(tokens)
    return word_tokenizer.split_and_group_sentences_using_text(text)

cdef list preprocess_text(str text):
    return process_text(                                                     \
        remove_html(                                                         \
            remove_math_sections(                                            \
                remove_dates(                                                \
                    remove_bullets_nbsps.sub(empty_space,                    \
                        remove_wikipedia_link.sub(anchor_replacer,           \
                            remove_markup(                                   \
                                _remove_remaining_double_brackets(           \
                                    _remove_brackets(                        \
                                        _remove_table(                       \
                                            _remove_squiggly_bracket(        \
                                                 _remove_mvar(
                                                    _remove_urls(text)))))))))))))

cdef list preprocess_text_markupless(str text):
    return process_text(remove_dates(_remove_urls(text)))

def tokenize(str text):
    for sentence in process_text(text):
        yield sentence

def to_raw_text_markupless(str text):
    """
    A generator to convert raw text segments, without xml to a
    list of words without any markup.
    Additionally dates are replaced by `7777` for normalization.

    Inputs
    ------
     str text: a piece of text

    Outputs
    -------
     generator<list<list<str>>>, a generator for sentences, with
     within each sentence a list of the words separated.
    """
    for sentence in preprocess_text_markupless(text):
        yield sentence

def to_raw_text(str text):
    """
    A generator to convert raw text segments, with xml, and other
    non-textual content to a list of words without any markup.
    Additionally dates are replaced by `7777` for normalization.

    Inputs
    ------
     str text: a piece of text

    Outputs
    -------
     generator<list<list<str>>>, a generator for sentences, with
     within each sentence a list of the words separated.
    """
    for sentence in preprocess_text(text):
        yield sentence

cdef list process_text_keeping_brackets(str text):
    return word_tokenizer.split_and_group_sentences_using_text_keep_brackets(text)

cdef list preprocess_text_keeping_brackets(str text):
    return process_text_keeping_brackets(                                    \
        remove_html(                                                         \
            remove_math_sections(                                            \
                    remove_bullets_nbsps.sub(empty_space,                    \
                        remove_wikipedia_link.sub(anchor_replacer,           \
                            remove_markup(                                   \
                                _remove_table(                               \
                                    _remove_squiggly_bracket(                \
                                        _remove_mvar(                        \
                                            text)))))))))                     

def to_raw_text_pairings(str text):
    """
    A generator to convert raw text segments, with xml, and other
    non-textual content to a list of words without any markup.
    Additionally dates are replaced by `7777` for normalization,
    along with wikipedia anchors kept.

    Inputs
    ------
     str text: a piece of text

    Outputs
    -------
     generator<list<list<str>>>, a generator for sentence with brackets kept, with
     within each sentence a list of the words separated.
    """
    for sentence in preprocess_text_keeping_brackets(text):
        yield sentence
