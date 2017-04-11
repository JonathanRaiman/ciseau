from .constants import (
    OPENING_SYMBOLS,
    CLOSING_SYMBOLS,
    CLOSE_2_OPEN,
    PUNCT_SYMBOLS,
    CONTINUE_PUNCT_SYMBOLS
)

def group_quoted_tokens(tokens):
    sentences = []
    opening_symbols = OPENING_SYMBOLS.copy()
    closing_symbols = CLOSING_SYMBOLS.copy()

    inside = []
    observed_opens = 0
    open_closed_sections = []

    for idx, word in enumerate(tokens):
        token_stripped = word[0]
        if token_stripped in opening_symbols and token_stripped == '"':
            # probably a closing quote since there are spaces
            # after it. Let's confirm by checking if there were
            # any spaces on the previous word:
            quote_has_spaces = len(word) > len(token_stripped)
            previous_word_has_spaces = idx > 0 and tokens[idx-1].endswith(' ')
            is_last_word = idx + 1 == len(tokens)
            if idx == 0:
                is_open_symbol = True
                is_close_symbol = False
            elif quote_has_spaces and previous_word_has_spaces:
                # 1. previous word has spaces before this symbol
                # so spaces are not meaningful.

                # 2. We find that we are already within a quoted section:
                if len(inside) > 0 and inside[-1][0] == '"':
                    is_open_symbol = False
                    is_close_symbol = True
                else:
                    # we are not within a quoted section, we resort to counting
                    # to see what is the best opening-closing strategy
                    num_expected_future_quotes = sum(symbol == '"' for symbol, _ in inside) + 1
                    num_future_quotes = sum(token[0] == '"' for token in tokens[idx+1:])
                    # find the right amount of quotes:
                    if num_expected_future_quotes == num_future_quotes:
                        is_open_symbol = True
                        is_close_symbol = False
                    else:
                        is_open_symbol = False
                        is_close_symbol = True
            elif quote_has_spaces and not previous_word_has_spaces:
                # 'joe" ' -> closing some quotes
                is_close_symbol = True
                is_open_symbol = False
            elif is_last_word:
                # last word may not have spaces
                is_open_symbol = False
                is_close_symbol = True
            else:
                if (not tokens[idx-1].endswith(' ') or
                    tokens[idx+1][0] in PUNCT_SYMBOLS or
                    tokens[idx+1][0] in CONTINUE_PUNCT_SYMBOLS):
                    if len(inside) > 0 and inside[-1][0] == '"':
                        # quote is followed by semicolon, comma, etc...
                        # or preceded by a word without a space 'joe"something"'
                        is_open_symbol = False
                        is_close_symbol = True
                    else:
                        is_open_symbol = True
                        is_close_symbol = False
                else:
                    # no spaces after this quote, can thus assume that it is opening
                    is_open_symbol = True
                    is_close_symbol = False
        else:
            is_open_symbol = token_stripped in opening_symbols
            is_close_symbol = token_stripped in closing_symbols

        if is_open_symbol:
            inside.append((token_stripped, idx))
            observed_opens += 1
        elif is_close_symbol:
            if len(inside) > 0:
                if inside[-1][0] == CLOSE_2_OPEN[token_stripped]:
                    open_closed_sections.append((inside[-1][1], idx + 1))
                    inside.pop()
                else:
                    if token_stripped in closing_symbols:
                        # this closing symbol seems to be ignored
                        closing_symbols.remove(token_stripped)
                        opening_symbols.remove(CLOSE_2_OPEN[token_stripped])
                    # from now on ignore this symbol as start or end:
                    inside = [(symbol, start)
                              for symbol, start in inside
                              if symbol != CLOSE_2_OPEN[token_stripped]]
            else:
                if observed_opens > 0:
                    if token_stripped in closing_symbols:
                        # this closing symbol seems to be ignored
                        closing_symbols.remove(token_stripped)
                        opening_symbols.remove(CLOSE_2_OPEN[token_stripped])

    earliest_start = len(tokens)
    out_tokens = []
    for start, end in open_closed_sections[::-1]:
        if start > earliest_start:
            continue
        else:
            if end != earliest_start:
                out_tokens = tokens[end:earliest_start] + out_tokens
            out_tokens = [tokens[start:end]] + out_tokens
            earliest_start = start
    if earliest_start > 0:
        out_tokens = tokens[0:earliest_start] + out_tokens
    return out_tokens

