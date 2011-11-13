import re
import unittest
from collections import OrderedDict

from confparser import ConfParser, ConfParserException
from linestyleprocessor import LineStyleProcessor
from regionmatcher import RegionMatcher
from transformer import Style

def regex(pattern):
    return re.compile(pattern)

#
# TODO: enable __tests
#

class LineStyleProcessorTests(unittest.TestCase):
    def setUp(self):
        self.line = "This is a long string forty chars long.."
        
        assert len(self.line) == 40
        self.lineStyleProcessor = LineStyleProcessor()
        self.style_map = OrderedDict()

    def tearDown(self):
        self.lineStyleProcessor = None
        self.style_map = None

    def add_style(self, regions):
        empty_regex = regex("")
        style = Style(empty_regex, None)
        self.style_map[style] = regions
        return style

    def __test_get_region_map(self):
        s1 = self.add_style([(1,2),(7,12),(19,25)])
        s2 = self.add_style([(4,7)])    # overlaps
        s3 = self.add_style([(12,15)])  # overlaps
        s4 = self.add_style([(25,29)])  # overlaps
        s5 = self.add_style([(26,28)])
        s6 = self.add_style([(26,28)])  # overlaps
        s7 = self.add_style([(29,29)])
        s8 = self.add_style([(13,15)])

        region_map = self.lineStyleProcessor.__get_elected_region_map__(
            self.line, self.style_map)
        
        regions = region_map.keys()
        regions.sort()
        
        self.assert_results([(1,2), (7,12), (13,15),
                             (19,25), (26,28), (29,29)], regions)
        
        self.assertEqual(region_map[(1,2)], s1)
        self.assertEqual(region_map[(7,12)], s1)
        self.assertEqual(region_map[(19,25)], s1)
        self.assertEqual(region_map[(26,28)], s5)
        self.assertEqual(region_map[(29,29)], s7)
        self.assertEqual(region_map[(13,15)], s8)

    def __test_get_region_map_reverse_order(self):
        s1 = self.add_style([(13,15)])
        s2 = self.add_style([(29,29)])
        s3 = self.add_style([(26,28)])
        s4 = self.add_style([(26,28)]) # overlaps
        s5 = self.add_style([(25,29)]) # overlaps
        s6 = self.add_style([(12,15)]) # overlaps
        s7 = self.add_style([(4,7)])
        s8 = self.add_style([(1,2),(7,12),(19,25)]) # overlaps except: (1,2)

        region_map = self.lineStyleProcessor.__get_elected_region_map__(
            self.line, self.style_map)
        regions = region_map.keys()
        regions.sort()

        self.assert_results([(1,2), (4,7), (13,15),
                             (19,25), (26,28), (29,29)], regions)
        
        self.assertEqual(region_map[(1,2)], s8)
        self.assertEqual(region_map[(4,7)], s7)
        self.assertEqual(region_map[(13,15)], s1)
        self.assertEqual(region_map[(19,25)], s8)
        self.assertEqual(region_map[(26,28)], s3)
        self.assertEqual(region_map[(29,29)], s2)

    def assert_results(self, expected_results, results):
        self.assertEquals(len(expected_results), len(results))
        for i, result in enumerate(results):
            self.assertEqual(expected_results[i], result)


class RegionMatcherTests(unittest.TestCase):

    def setUp(self):
        regionmatcher = RegionMatcher()
        self.find_regions = regionmatcher.find_regions
        self.__find_regions__ = regionmatcher.__find_regions__
        self.__get_unique_search_tokens__ = regionmatcher.__get_unique_search_tokens__

    def tearDown(self):
        self.__find_regions__ = None
        self.__get_unique_search_tokens__ = None

    def __test_repeated_invocation_returns_new_list(self):
        results1 = self.__find_regions__('string', 'in')
        results2 = self.__find_regions__('string', 'in')
        self.assertIsNot(results1, results2)
        self.assert_results([(3,4)], results1)
        self.assert_results([(3,4)], results2)

    def __test_missing_searchstr_return_empty_results(self):
        results = self.__find_regions__('some string', '')
        self.assert_results([], results)
        
        results = self.__find_regions__('some string', None)
        self.assert_results([], results)
        
        results = self.__find_regions__('', '')
        self.assert_results([], results)

    def __test_no_match(self):
        results = self.__find_regions__('', 'a')
        self.assert_results([], results)
        
        results = self.__find_regions__('', 'foo')
        self.assert_results([], results)

        results = self.__find_regions__('some string', 'foo')
        self.assert_results([], results)

    def __test_smart_simple_cases(self):
        results = self.__find_regions__('this is...', 'this')
        self.assert_results([(0,3)], results)

        results = self.__find_regions__('my string', 'string')
        self.assert_results([(3,8)], results)

    def __test_single_char_match(self):
        results = self.__find_regions__('a', 'a')
        self.assert_results([(0,0)], results)

        results = self.__find_regions__('aaaaa', 'a')
        self.assert_results([(0,0), (1,1), (2,2), (3,3), (4,4)], results)

        results = self.__find_regions__('axaxa', 'a')
        self.assert_results([(0,0), (2,2), (4,4)], results)

        results = self.__find_regions__('foo', 'f')
        self.assert_results([(0,0)], results)

        results = self.__find_regions__('foo', 'o')
        self.assert_results([(1,1), (2,2)], results)
        
    def __test_consecutive_matches(self):
        results = self.__find_regions__('isisis', 'is')
        tokens = self.__get_unique_search_tokens__('isisis', regex('is'))
        self.assertEqual(['is'], tokens)
        self.assert_results([(0,1), (2,3), (4,5)], results)

        results = self.__find_regions__('isisisis', 'is')
        self.assert_results([(0,1), (2,3), (4,5), (6,7)], results)

        results = self.__find_regions__('x isis', 'is')
        self.assert_results([(2,3), (4,5)], results)
        #                              0         1         2
        #                              012345678901234567890
        results = self.__find_regions__('this is his list isis', 'is')
        self.assert_results([(2,3), (5,6), (9,10),
                             (13,14), (17,18), (19,20)], results)


    def __test_find_regions_with_simple_regex(self):
        results = self.find_regions('0123456789 nums', regex('\d+'))
        self.assert_results([(0,9)], results)

        results = self.find_regions('0123456789', regex('\d+'))
        self.assert_results([(0,9)], results)

        results = self.find_regions('some string', regex('\w+'))
        self.assert_results([(0,3), (5,10)], results)

        results = self.find_regions('some long string', regex('long'))
        self.assert_results([(5,8)], results)

        results = self.find_regions('foo boo', regex('o+'))
        self.assert_results([(1,2), (5,6)], results)

        results = self.find_regions('foo boo', regex('o'))
        self.assert_results([(1,1), (2,2), (5,5), (6,6)], results)

    # TODO: fix test and re-run all tests
    def test_FIX_BROKEN_1_match_digit_in_timestamp_string(self):
        #s = "2011-11-11 22:08:52.074932: Url: org.apache.tomcat.UrlResolver - doing something"
        #    0         1         2
        #    01234567890123456789012345
        s = "20-2011-11-11 22:08:52.074932"
        
        tokens = self.__get_unique_search_tokens__(s, regex("\d+"))
        results = self.find_regions(s, regex("\d+"))

        print "TOKENS", tokens    # ['2011', '11', '22', '08', '52', '074932']
        print "RESULTS", results  # (0,3), (2,3), (5,6)
        
        self.assert_results([(0,3), (4,5), (8,9),       # date
                             (11,12), (14,15), (17,18), # time
                             (20,25)], results)
        
    def __test_FIX_BROKEN_2(self):
        #    0         1
        #    012345678901234
        s = "(none) ((none))"
        regex_obj = regex(r".*\((.*)\).*")
        
        # token = ['none)']
        tokens = self.__get_unique_search_tokens__(s, regex_obj)
        # results = []
        results = self.find_regions(s, regex_obj)
        
        self.assert_results([(1,4), (9,12)], results)
        

    def __test_get_unique_search_tokens(self):
        results = self.__get_unique_search_tokens__(
            "111 some 111 string 111", regex("\d\d\d"))
        self.assertEqual(['111'], results)

        results = self.__get_unique_search_tokens__(
            "111 some 111 string 111", regex("some"))
        self.assertEqual(['some'], results)

        results = self.__get_unique_search_tokens__(
            "2011-11-11 22:08:52.074932:", regex("\d+"))
        self.assertEqual(sorted(['2011', '11', '074932', '22', '08', '52']),
                         sorted(results))

        results = self.__get_unique_search_tokens__("some string", regex("foo"))
        self.assertEqual([], results)

        results = self.__get_unique_search_tokens__("", regex(""))
        self.assertEqual([], results)

    def assert_results(self, expected_results, results):
        self.assertEquals(len(expected_results), len(results))
        for i, result in enumerate(results):
            self.assertEqual(expected_results[i], result)



class ConfParserTests(unittest.TestCase):
    def setUp(self):
        self.confparser = ConfParser('.test.txts.conf')
        self.expected_styles = []

    def tearDown(self):
        self.confparser = None
        self.expected_styles = None

    def add_style(self, pattern, transforms):
        self.expected_styles.append(Style(pattern, transforms))

    def __test_get_first(self):
        styles = self.confparser.get_styles('first')
        self.add_style('some error', 'red')
        self.add_style('\d\d-\d\d-\d\d\d\d', 'blue')
        self.add_style('some pattern', 'green')
        self.add_style('other pattern', 'underline')
        self.assert_styles(styles)
        
    def __test_get_second(self):
        styles = self.confparser.get_styles('second')
        self.add_style('\w+', 'blue')
        self.assert_styles(styles)

    def __test_get_third(self):
        styles = self.confparser.get_styles('third')
        self.add_style('\d+', 'on-red')
        self.add_style('.*(foo).*', 'black')
        self.add_style(': single: quotes', 'yellow')
        self.assert_styles(styles)

    def __test_get_fourth(self):
        styles = self.confparser.get_styles('fourth')
        assert styles == []

    def __test_get_fifth(self):
        try:
            styles = self.confparser.get_styles('fifth')
            self.fail('should fail on invalid definition')
        except ConfParserException, e:
            assert e.message == 'Invalid style definition: black "missing semi-colon"'
        
    def assert_styles(self, styles):
        self.assertEquals(len(self.expected_styles), len(styles))
        for i, style in enumerate(styles):
            expected = self.expected_styles[i]
            self.assertEqual(expected.regex_obj.pattern, style.regex_obj.pattern)
            self.assertEqual(expected.transforms, style.transforms)
        

if __name__ == "__main__":
    unittest.main()
