# -*- coding: utf-8 -*-
import unittest
import sys
from xml_cleaner import tokenize, sent_tokenize

class TokenizationTests(unittest.TestCase):
    def test_quoted_expressions(self):
        expression = [
            "(", "in ", "2008", ") ", "the ", "Martians ",
            "arrived ", "and ", "you", "'ll ", "see ", "what ",
            "I ", "mean", "."
        ]
        self.assertEqual(
            tokenize(
                "".join(expression)
            ),
            expression
        )

    def test_weird_hybrid_expressions(self):
        expression = [
            u"Beyoncé", u"'s ", u"1840", u"'s ", u"song ", u"<", u"3lovely", u"."
        ]
        self.assertEqual(
            tokenize(
                "".join(expression)
            ),
            expression
        )

    def test_numerical_commas_periods_expressions(self):
        expression = [
            "In ", "the ", "year ", "2000", ", ",
            "there ", "was ", "evidence ", "that ", "100,000 ",
            "martians ", "came ", "to ", "see ", "us", ", ",
            "but ", "I ", "did", "n't ", "even ", "hear ",
            "98.2", ",", "98.3 ", "or ", "98.4 ", "speak ",
            "about ", "it", ","
        ]
        self.assertEqual(
            tokenize("".join(expression)),
            expression
        )

    def test_abbreviations(self):
        expression = [
            "Mr. ", "hooligan ", "and ", "his ", "brother ", "DR. ",
            "strange ", "know ", "each ", "other ", "well ", "said ",
            "d. ", "A. ", "Joe ", "the ", "sgt. ", "in ", "charge ",
            "of ", "all ", "this ", "bs", "."
        ]
        self.assertEqual(
            tokenize("".join(expression)),
            expression
        )

    def test_em_dash(self):
        expression = [
            "The ", "earthquake ", "was ",
            "also ", "felt ", "in ", "nearby ", "countries ",
            "and ", "as ", "far ", "away ", "as ", "both ",
            "Beijing ", "and ", "Shanghai ", "—", "1,500 ", "km ",
            "(", "930 ", "mi ", ") ", "and ", "1,700 ", "km ", "(",
            "1,060 ", "mi ", ") ", "away", "—", "where ", "office ",
            "buildings ", "swayed ", "with ", "the ", "tremor", "."
        ]
        self.assertEqual(
            tokenize("".join(expression), normalize_ascii=False),
            expression
        )

    def test_quoted_expressions_with_ascii(self):
        expression = [
            "Julius ", u"Cæsar ", "declared ", "-- ", "professed ", "- ",
            "his ", "passion ", "for ", "wine ", "A", "."
        ]
        self.assertEqual(
            tokenize(
                "".join(expression),
                normalize_ascii=False
            ),
            expression
        )
        self.assertEqual(
            tokenize(
                "".join(expression),
                normalize_ascii=True
            ),
            [w.replace(u"æ", "ae").replace("--", "-") for w in expression]
        )

    def test_sentence_detection(self):
        expression = [
            [u'Maslow', u'’s ', u'‘‘', u'Third ', u'Force ', u'Psychology ',
             u'Theory', u'’’ ', u'even ', u'allows ', u'literary ', u'analysts ',
             u'to ', u'critically ', u'understand ', u'how ', u'characters ',
             u'reflect ', u'the ', u'culture ', u'and ', u'the ', u'history ',
             u'in ', u'which ', u'they ', u'are ', u'contextualized', u'. '],
            [u'It ', u'also ', u'allows ', u'analysts ', u'to ', u'understand ',
             u'the ', u'author', u'’s ', u'intended ', u'message ', u'and ', u'to ',
             u'understand ', u'the ', u'author', u'’s ', u'psychology', u'. '],
            [u'The ', u'theory ', u'suggests ', u'that ', u'human ', u'beings ',
             u'possess ', u'a ', u'nature ', u'within ', u'them ', u'that ',
             u'demonstrates ', u'their ', u'true ', u'“', u'self', u'” ', u'and ',
             u'it ', u'suggests ', u'that ', u'the ', u'fulfillment ', u'of ',
             u'this ', u'nature ', u'is ', u'the ', u'reason ', u'for ', u'living',
             u'. '],
            [u'It ', u'also ', u'suggests ', u'that ', u'neurological ',
             u'development ', u'hinders ', u'actualizing ', u'the ', u'nature ',
             u'because ', u'a ', u'person ', u'becomes ', u'estranged ', u'from ',
             u'his ', u'or ', u'her ', u'true ', u'self', u'. '],
            [u'Therefore', u', ', u'literary ', u'devices ', u'reflect ', u'a ',
             u'characters', u'’s ', u'and ', u'an ', u'author', u'’s ', u'natural ',
             u'self', u'. '],
            [u'In ', u'his ', u'‘‘', u'Third ', u'Force ', u'Psychology ', u'and ',
             u'the ', u'Study ', u'of ', u'Literature', u'’’', u', ', u'Paris ',
             u'argues ', u'“', u'D.', u'H ', u'Lawrence', u'’s ', u'“', u'pristine ',
             u'unconscious', u'” ', u'is ', u'a ', u'metaphor ', u'for ', u'the ',
             u'real ', u'self', u'”', u'. '],
            [u'Thus ', u'Literature ', u'is ', u'a ', u'reputable ', u'tool ',
             u'that ', u'allows ', u'readers ', u'to ', u'develop ', u'and ',
             u'apply ', u'critical ', u'reasoning ', u'to ', u'the ', u'nature ',
             u'of ', u'emotions', u'.']
        ]
        self.assertEqual(
            sent_tokenize(
                u"".join(w for sent in expression for w in sent),
                keep_whitespace=True
            ),
            expression
        )

    def test_unequal_quote_detection(self):
        expression = [
            [u"Beyoncé", u"'s ", u'vocal ', u'range ', u'spans ', u'four ', u'octaves',
             u'. '],
            [u'Jody ', u'Rosen ', u'highlights ', u'her ', u'tone ', u'and ',
             u'timbre ', u'as ', u'particularly ', u'distinctive', u', ',
             u'describing ', u'her ', u'voice ', u'as ', u'"', u'one ', u'of ',
             u'the ', u'most ', u'compelling ', u'instruments ', u'in ',
             u'popular ', u'music', u'"', u'. '
            ],
            [u'While ', u'another ', u'critic ', u'says ', u'she ', u'is ',
             u'a ', u'"', u'Vocal ', u'acrobat', u', ', u'being ', u'able ',
             u'to ', u'sing ', u'long ', u'and ', u'complex ', u'melismas ',
             u'and ', u'vocal ', u'runs ', u'effortlessly', u', ', u'and ',
             u'in ', u'key', u'. '],
            [u'Her ', u'vocal ', u'abilities ', u'mean ', u'she ', u'is ',
             u'identified ', u'as ', u'the ', u'centerpiece ', u'of ', u'Destiny',
             u"'s ", u'Child', u'. '],
            [u'The ', u'Daily ', u'Mail ', u'calls ', u"Beyoncé", u"'s ", u'voice ',
             u'"', u'versatile', u'"', u', ', u'capable ', u'of ', u'exploring ',
             u'power ', u'ballads', u', ', u'soul', u', ', u'rock ', u'belting',
             u', ', u'operatic ', u'flourishes', u', ', u'and ', u'hip ', u'hop',
             u'. '],
            [u'Jon ', u'Pareles ', u'of ', u'The ', u'New ', u'York ', u'Times ',
             u'commented ', u'that ', u'her ', u'voice ', u'is ', u'"', u'velvety ',
             u'yet ', u'tart', u', ', u'with ', u'an ', u'insistent ', u'flutter ',
             u'and ', u'reserves ', u'of ', u'soul ', u'belting', u'"', u'. '],
            [u'Rosen ', u'notes ', u'that ', u'the ', u'hip ', u'hop ', u'era ',
             u'highly ', u'influenced ', u"Beyoncé", u"'s ", u'strange ', u'rhythmic ',
             u'vocal ', u'style', u', ', u'but ', u'also ', u'finds ', u'her ',
             u'quite ', u'traditionalist ', u'in ', u'her ', u'use ', u'of ',
             u'balladry', u', ', u'gospel ', u'and ', u'falsetto', u'. '],
            [u'Other ', u'critics ', u'praise ', u'her ', u'range ', u'and ',
             u'power', u', ', u'with ', u'Chris ', u'Richards ', u'of ', u'The ',
             u'Washington ', u'Post ', u'saying ', u'she ', u'was ', u'"',
             u'capable ', u'of ', u'punctuating ', u'any ', u'beat ', u'with ',
             u'goose', u'-', u'bump', u'-', u'inducing ', u'whispers ', u'or ',
             u'full', u'-', u'bore ', u'diva', u'-', u'roars', u'.', u'"']
        ]
        self.assertEqual(
            sent_tokenize(
                u"".join(w for sent in expression for w in sent),
                keep_whitespace=True
            ),
            expression
        )

    def test_contained_period_in_quotes(self):
        expression = [[
            "the ", "gray ", "bird ", "(", "which ", "was ",
            "famous ", "for ", "its ", "colors", ".", ") ",
            "was ", "ressurected ", "\" ", "she ", "said", ".", "\""
        ]]
        self.assertEqual(
            sent_tokenize(
                "".join(w for sent in expression for w in sent),
                keep_whitespace=True
            ),
            expression
        )
