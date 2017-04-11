# -*- coding: utf-8 -*-
import sys

if sys.version_info >= (3,3):
    dashes = ["–", "--+"]
    for i in range(8208, 8214):
        dashes.append(chr(i))
else:
    dashes = [u"–", u"--+"]
    for i in range(8208, 8214):
        dashes.append(unichr(i))


UNDECIDED = 0
SHOULD_SPLIT = 1
SHOULD_NOT_SPLIT = 2

people = [
    "jr", "mr", "ms", "mrs", "dr", "prof", "esq", "sr",
    "sen", "sens", "rep", "reps", "gov", "attys", "attys",
    "supt", "det", "mssrs", "rev", "fr", "ss", "msgr"
]
army   = ["col", "gen", "lt", "cmdr", "adm", "capt", "sgt", "cpl", "maj", "brig", "pt"]
inst   = ["dept","univ", "assn", "bros", "ph.d"]
place  = [
    "arc", "al", "ave", "blvd", "bld", "cl", "ct",
    "cres", "exp", "expy", "dist", "mt", "mtn", "ft",
    "fy", "fwy", "hwy", "hway", "la", "pde", "pd","plz", "pl", "rd", "st",
    "tce"
]
comp   = ["mfg", "inc", "ltd", "co", "corp"]
state  = [
    "ala","ariz","ark","cal","calif","colo","col","conn",
    "del","fed","fla","ga","ida","id","ill","ind","ia","kans",
    "kan","ken","ky","la","me","md","is","mass","mich","minn",
    "miss","mo","mont","neb","nebr","nev","mex","okla","ok",
    "ore","penna","penn","pa","dak","tenn","tex","ut","vt",
    "va","wash","wis","wisc","wy","wyo","usafa","alta",
    "man","ont","que","sask","yuk"
]
month  = [
    "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep",
    "sept", "oct", "nov", "dec"
]
misc = ["vs", "etc", "no","esp", "ed", "iv", "Oper", "op", "i.e", "e.g", "v"]
website = ["www"]
currency = ["rs"]
ABBR = {}
# create a hash of these abbreviations:
for abbreviation_type in [people, army, inst, place, comp, state, month, misc, website, currency]:
    for abbreviation in abbreviation_type:
        ABBR[abbreviation] = True

MONTHS = {
    "january", "february", "march", "april", "may",
    "june", "july", "august", "september", "october",
    "november", "december"
}
PUNCT_SYMBOLS = {'.', "...", "?", "!", "..", "!!", "??", "!?", "?!", u"…"}
CONTINUE_PUNCT_SYMBOLS = {';', ',', '-', ':'} | set(dashes)
OPENING_SYMBOLS = {'(', '[', '"', '{', '“'}
CLOSING_SYMBOLS = {')', ']', '"', '}', '”'}
CLOSE_2_OPEN = {')':'(', ']': '[', '"':'"', '}':'{', '”':'“'}
