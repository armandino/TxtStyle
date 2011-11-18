import re
import unittest
from ordereddict import OrderedDict

from confparser import ConfParser, ConfParserException
from linestyleprocessor import LineStyleProcessor
from regionmatcher import RegionMatcher
import transformer

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
        style = transformer.Style(empty_regex, None)
        self.style_map[style] = regions
        return style

    def test_get_region_map(self):
        s1 = self.add_style([(1,2),(7,12),(19,25)])
        s2 = self.add_style([(4,7)])    # overlaps
        s3 = self.add_style([(12,15)])  # overlaps
        s4 = self.add_style([(25,29)])  # overlaps
        s5 = self.add_style([(26,28)])
        s6 = self.add_style([(26,28)])  # overlaps
        s7 = self.add_style([(29,29)])
        s8 = self.add_style([(13,15)])

        region_map = self.lineStyleProcessor._get_elected_region_map(
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

    def test_get_region_map_reverse_order(self):
        s1 = self.add_style([(13,15)])
        s2 = self.add_style([(29,29)])
        s3 = self.add_style([(26,28)])
        s4 = self.add_style([(26,28)]) # overlaps
        s5 = self.add_style([(25,29)]) # overlaps
        s6 = self.add_style([(12,15)]) # overlaps
        s7 = self.add_style([(4,7)])
        s8 = self.add_style([(1,2),(7,12),(19,25)]) # overlaps except: (1,2)

        region_map = self.lineStyleProcessor._get_elected_region_map(
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
        self._find_regions = regionmatcher._find_regions
        self._get_unique_search_tokens = regionmatcher._get_unique_search_tokens

    def tearDown(self):
        self._find_regions = None
        self._get_unique_search_tokens = None

    def test_repeated_invocation_returns_new_list(self):
        results1 = self._find_regions('string', 'in')
        results2 = self._find_regions('string', 'in')
        self.assertIsNot(results1, results2)
        self.assert_results([(3,4)], results1)
        self.assert_results([(3,4)], results2)

    def test_missing_searchstr_return_empty_results(self):
        results = self._find_regions('some string', '')
        self.assert_results([], results)
        
        results = self._find_regions('some string', None)
        self.assert_results([], results)
        
        results = self._find_regions('', '')
        self.assert_results([], results)

    def test_no_match(self):
        results = self._find_regions('', 'a')
        self.assert_results([], results)
        
        results = self._find_regions('', 'foo')
        self.assert_results([], results)

        results = self._find_regions('some string', 'foo')
        self.assert_results([], results)

    def test_smart_simple_cases(self):
        results = self._find_regions('this is...', 'this')
        self.assert_results([(0,3)], results)

        results = self._find_regions('my string', 'string')
        self.assert_results([(3,8)], results)

    def test_single_char_match(self):
        results = self._find_regions('a', 'a')
        self.assert_results([(0,0)], results)

        results = self._find_regions('aaaaa', 'a')
        self.assert_results([(0,0), (1,1), (2,2), (3,3), (4,4)], results)

        results = self._find_regions('axaxa', 'a')
        self.assert_results([(0,0), (2,2), (4,4)], results)

        results = self._find_regions('foo', 'f')
        self.assert_results([(0,0)], results)

        results = self._find_regions('foo', 'o')
        self.assert_results([(1,1), (2,2)], results)
        
    def test_consecutive_matches(self):
        results = self._find_regions('isisis', 'is')
        tokens = self._get_unique_search_tokens('isisis', regex('is'))
        self.assertEqual(['is'], tokens)
        self.assert_results([(0,1), (2,3), (4,5)], results)

        results = self._find_regions('isisisis', 'is')
        self.assert_results([(0,1), (2,3), (4,5), (6,7)], results)

        results = self._find_regions('x isis', 'is')
        self.assert_results([(2,3), (4,5)], results)
        #                              0         1         2
        #                              012345678901234567890
        results = self._find_regions('this is his list isis', 'is')
        self.assert_results([(2,3), (5,6), (9,10),
                             (13,14), (17,18), (19,20)], results)


    def test_find_regions_with_simple_regex(self):
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
    def __test_FIX_BROKEN_1_match_digit_in_timestamp_string(self):
        #    0         1         2
        #    01234567890123456789012345
        s = "20-2011-11-11 22:08:52.074932"
        
        tokens = self._get_unique_search_tokens(s, regex("\d+"))
        results = self.find_regions(s, regex("\d+"))

        print "TOKENS", tokens    # ['2011', '11', '22', '08', '52', '074932']
        print "RESULTS", results  # (0,3), (2,3), (5,6)
        
        self.assert_results([(0,3), (4,5), (8,9),       # date
                             (11,12), (14,15), (17,18), # time
                             (20,25)], results)
        
    def test_text_inside_brackets(self):
        s = "text (inside) brackets"
        r = regex("\((.*)\)")
        
        tokens = self._get_unique_search_tokens(s, r)
        results = self.find_regions(s, r)
        self.assertEqual(['(inside)'], tokens)
        self.assert_results([(5,12)], results)
       
    def test_get_unique_search_tokens(self):
        results = self._get_unique_search_tokens(
            "111 some 111 string 111", regex("\d\d\d"))
        self.assertEqual(['111'], results)

        results = self._get_unique_search_tokens(
            "111 some 111 string 111", regex("some"))
        self.assertEqual(['some'], results)

        results = self._get_unique_search_tokens(
            "2011-11-11 22:08:52.074932:", regex("\d+"))
        self.assertEqual(sorted(['2011', '11', '074932', '22', '08', '52']),
                         sorted(results))

        results = self._get_unique_search_tokens("some string", regex("foo"))
        self.assertEqual([], results)

        results = self._get_unique_search_tokens("", regex(""))
        self.assertEqual([], results)

    def assert_results(self, expected_results, results):
        self.assertEquals(len(expected_results), len(results))
        for i, result in enumerate(results):
            self.assertEqual(expected_results[i], result)

class ConfParserTests(unittest.TestCase):
    def setUp(self):
        conf = open('testdata/test.txts.conf')
        try:
            self.confparser = ConfParser(conf.readlines())
        finally:
            conf.close()
        
        self.expected_styles = []

    def tearDown(self):
        self.confparser = None
        self.expected_styles = None

    def expect_style(self, pattern, transforms):
        self.expected_styles.append(transformer.Style(pattern, transforms))

    def test_get_first(self):
        styles = self.confparser.get_styles('first')
        self.expect_style(r'some error', ['red'])
        self.expect_style(r'\d\d-\d\d-\d\d\d\d', ['blue'])
        self.expect_style(r'some pattern', ['green'])
        self.expect_style(r'\[(xyz.*x+y?z+)\]', ['underline'])
        self.assert_styles(styles)
        
    def test_get_second(self):
        styles = self.confparser.get_styles('second')
        self.expect_style('\w+', ['blue'])
        self.assert_styles(styles)

    def test_get_third(self):
        styles = self.confparser.get_styles('third')
        self.expect_style(r':on-red : \d+', ['on-red'])
        self.expect_style(r'\\:\\[\s+]foo.*(foo).*bar\\\\', ['grey'])
        self.expect_style(r': single: quotes', ['yellow'])
        self.assert_styles(styles)

    def test_get_fourth(self):
        styles = self.confparser.get_styles('fourth')
        assert styles == []

    def test_get_fifth(self):
        try:
            styles = self.confparser.get_styles('fifth')
            self.fail('should fail on invalid definition')
        except ConfParserException, e:
            self.assertEqual(e.message, 'Invalid style definition: green "some pattern"')
        
    def test_get_sixth(self):
        try:
            styles = self.confparser.get_styles('sixth')
            self.fail('should fail on invalid style attribute')
        except ConfParserException, e:
            self.assertEqual(e.message, 'Invalid style attribute: "some-bad-attribute"')

    def test_get_seventh(self):
        styles = self.confparser.get_styles('seventh')
        self.expect_style(r':.*\d\s\'\"', ['blue', 'on-white'])
        self.assert_styles(styles)

    def test_get_eighth(self):
        styles = self.confparser.get_styles('eighth')
        self.expect_style(r'org.[\w+|\.]+', ['red'])
        self.assert_styles(styles)

    def test_get_undefined(self):
        try:
            styles = self.confparser.get_styles('FOO')
            self.fail('should fail on undefined  style name')
        except ConfParserException, e:
            self.assertEqual(e.message, 'Style "FOO" is not defined')

    def assert_styles(self, styles):
        self.assertEquals(len(self.expected_styles), len(styles))
        for i, style in enumerate(styles):
            expected = self.expected_styles[i]
            self.assertEqual(expected.regex_obj.pattern, style.regex_obj.pattern)
            self.assertEqual(expected.transforms, style.transforms)


class TransformerTests(unittest.TestCase):
    def setUp(self):
        Style = transformer.Style
        styles = [
            Style("^\w\w\w \d\d\s?", ['white', 'on-magenta']),
            Style("\d\d:\d\d:\d\d", ['bold', 'on-blue']),
            Style(".*<warn>.*", ['yellow']),
            Style("\((.*)\)", ['red', 'on-white']),
            Style("\[(.*)\]", ['grey', 'bold']),
            ]
        self.transformer = transformer.Transformer(styles)
        self.lines = self.get_lines('testdata/test-syslog')
    
    def get_lines(self, fname):
        f = open(fname)
        lines = f.readlines()
        f.close()
        return lines

    def test_removing_styles_is_equal_to_original_line(self):
        """Style a line, remove escape sequences and compare to the original
        """
        for original_line in self.lines:
            original_line = original_line.strip('\n')
            styled_line = self.transformer.style(original_line)
            styled_line = styled_line.encode('string_escape')
            unstyled_line = self.remove_styles(styled_line)
            self.assertEqual(original_line, unstyled_line)

    def remove_styles(self, line):
        unstyled = line.replace(r'\x1b[m', '', 1000)
        unstyled = unstyled.replace("\\'", "'", 1000)
        for style_key in transformer.__STYLES__:
            transform = transformer.__STYLES__[style_key]
            escape_code = transform.encode('string_escape')
            unstyled = unstyled.replace(escape_code, '', 1000)
        return unstyled

if __name__ == "__main__":
    unittest.main()
