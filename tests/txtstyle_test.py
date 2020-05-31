import re
import sys
import unittest

from txtstyle.confparser import ConfParser
from txtstyle.linestyleprocessor import LineStyleProcessor
from txtstyle.transformer import _STYLES
from txtstyle.transformer import IndexStyle
from txtstyle.transformer import RegexStyle
from txtstyle.transformer import Transformer

sys.path.append("..")

_TEST_DATA_DIR = 'tests/testdata'

def regex(pattern):
    return re.compile(pattern)

class LineStyleProcessorTests(unittest.TestCase):
    def setUp(self):
        self.lineStyleProcessor = LineStyleProcessor()
        self.find_regions = self.lineStyleProcessor.find_regions


    def test_get_style_map(self):
        #       0123456789012345678901234567890123456789
        line = "This is a long string forty chars long.."
        red = ['red']

        s1 = RegexStyle(regex("This"), red)
        s2 = RegexStyle(regex("is"), red)
        s3 = RegexStyle(regex("s"), red)

        styles = [s1, s2, s3]
        
        style_map = self.lineStyleProcessor.get_style_map(
            line, styles)
        
        regions = sorted(style_map.keys())
        
        self.assert_results([(0,4), (5,7), (15,16),
                             (32,33)], regions)
        
        self.assertEqual(style_map[(0,4)], s1)
        self.assertEqual(style_map[(5,7)], s2)
        self.assertEqual(style_map[(15,16)], s3)
        self.assertEqual(style_map[(32,33)], s3)


    def test_get_style_map_reverse_order(self):
        #       0123456789012345678901234567890123456789
        line = "This is a long string forty chars long.."
        red = ['red']

        s1 = RegexStyle(regex("s"), red)
        s2 = RegexStyle(regex("is"), red)
        s3 = RegexStyle(regex("This"), red)
        styles = [s1, s2, s3]
        
        style_map = self.lineStyleProcessor.get_style_map(line, styles)
        
        regions = sorted(style_map.keys())
        
        self.assert_results([(3,4), (6,7), (15,16),
                             (32,33)], regions)
        
        self.assertEqual(style_map[(3,4)], s1)
        self.assertEqual(style_map[(6,7)], s1)
        self.assertEqual(style_map[(15,16)], s1)
        self.assertEqual(style_map[(32,33)], s1)

    def test_get_style_map_index_style_when_start_is_equal_to_line_length(self):
        line = "blip"
        region = (len(line), len(line) + 1)
        s1 = IndexStyle([region], ['red'])
        style_map = self.lineStyleProcessor.get_style_map(line, [s1])
        regions = style_map.keys()
        self.assert_results([], regions)


    def test_get_style_map_index_style_when_end_is_greater_than_line_length(self):
        #       01234567890123456
        line = "a short string..."

        region = (7,20)
        self.assertTrue(region[1] > len(line))

        s1 = IndexStyle([region], ['red'])
        styles = [s1]
        style_map = self.lineStyleProcessor.get_style_map(line, styles)

        regions = style_map.keys()

        self.assert_results([(7,17)], regions)
        self.assertEqual(style_map[(7,17)], s1)

    def test_get_style_map_index_style_when_end_is_none(self):
        line = "end is None, and therefore defaults to line length"
        region = (0, None)

        s1 = IndexStyle([region], ['red'])
        styles = [s1]
        style_map = self.lineStyleProcessor.get_style_map(line, styles)

        regions = style_map.keys()
        expected_end = len(line)
        self.assert_results([(0, expected_end)], regions)
        self.assertEqual(style_map[(0, expected_end)], s1)


    def test_get_style_map_index_style(self):
        line = "a test string that needs to be longer than 65 characters.........."
        
        s1 = IndexStyle([
                (1,5), (4,10), (15,20), (35,40), (45,50)], ['red'])
        s2 = IndexStyle([
                (1,3), (4,6), (7,14), (41,44), (55,60)], ['red'])
        s3 = IndexStyle([
                (60,65)], ['red'])

        styles = [s1, s2, s3]
        style_map = self.lineStyleProcessor.get_style_map(line, styles)
        
        regions = sorted(style_map.keys())
        
        self.assert_results([(1,5), (7,14), (15,20),
                             (35,40), (41,44), (45,50),
                             (55,60), (60,65)], regions) # (60,65)?
        
        self.assertEqual(style_map[(1,5)], s1)
        self.assertEqual(style_map[(7,14)], s2)
        self.assertEqual(style_map[(15,20)], s1)
        self.assertEqual(style_map[(35,40)], s1)
        self.assertEqual(style_map[(41,44)], s2)
        self.assertEqual(style_map[(45,50)], s1)
        self.assertEqual(style_map[(55,60)], s2)
        self.assertEqual(style_map[(60,65)], s3)

    def assert_results(self, expected_results, results):
        self.assertEqual(len(expected_results), len(results))
        for i, result in enumerate(results):
            self.assertEqual(expected_results[i], result)

    def test_repeated_invocation_returns_new_list(self):
        results1 = self.find_regions('string', 'in')
        results2 = self.find_regions('string', 'in')
        self.assertIsNot(results1, results2)
        self.assert_results([(3,5)], results1)
        self.assert_results([(3,5)], results2)

    def test_missing_searchstr_return_empty_results(self):
        results = self.find_regions('some string', '')
        self.assert_results([], results)
        
        results = self.find_regions('some string', None)
        self.assert_results([], results)
        
        results = self.find_regions('', '')
        self.assert_results([], results)

    def test_no_match(self):
        results = self.find_regions('', 'a')
        self.assert_results([], results)
        
        results = self.find_regions('', 'foo')
        self.assert_results([], results)

        results = self.find_regions('some string', 'foo')
        self.assert_results([], results)

    def test_smart_simple_cases(self):
        results = self.find_regions('this is...', 'this')
        self.assert_results([(0,4)], results)

        results = self.find_regions('my string', 'string')
        self.assert_results([(3,9)], results)

    def test_single_char_match(self):
        results = self.find_regions('a', 'a')
        self.assert_results([(0,1)], results)

        results = self.find_regions('aaaaa', 'a')
        self.assert_results([(0,1), (1,2), (2,3), (3,4), (4,5)], results)

        results = self.find_regions('axaxa', 'a')
        self.assert_results([(0,1), (2,3), (4,5)], results)

        results = self.find_regions('foo', 'f')
        self.assert_results([(0,1)], results)

        results = self.find_regions('foo', 'o')
        self.assert_results([(1,2), (2,3)], results)
        
    def test_consecutive_matches(self):
        results = self.find_regions('isisis', 'is')
        self.assert_results([(0,2), (2,4), (4,6)], results)

        results = self.find_regions('isisisis', 'is')
        self.assert_results([(0,2), (2,4), (4,6), (6,8)], results)

        results = self.find_regions('x isis', 'is')
        self.assert_results([(2,4), (4,6)], results)
        #                              0         1         2
        #                              012345678901234567890
        results = self.find_regions('this is his list isis', 'is')
        self.assert_results([(2,4), (5,7), (9,11),
                             (13,15), (17,19), (19,21)], results)

    def test_find_regions_with_simple_regex(self):
        results = self.find_regions('x-11-11', regex('\d+'))
        self.assert_results([(2,4), (5,7)], results)

        results = self.find_regions('01-3456-11-11', regex('\d+'))
        self.assert_results([(0,2), (3,7), (8,10), (11,13)], results)

        results = self.find_regions('0123456789 nums', regex('\d+'))
        self.assert_results([(0,10)], results)

        results = self.find_regions('0123456789', regex('\d+'))
        self.assert_results([(0,10)], results)

        results = self.find_regions('some string', regex('\w+'))
        self.assert_results([(0,4), (5,11)], results)

        results = self.find_regions('some long string', regex('long'))
        self.assert_results([(5,9)], results)

        results = self.find_regions('foo boo', regex('o+'))
        self.assert_results([(1,3), (5,7)], results)

        results = self.find_regions('foo boo', regex('o'))
        self.assert_results([(1,2), (2,3), (5,6), (6,7)], results)
        
        results = self.find_regions(" '192.168.99.1'", regex('\d+\.\d+\.\d+\.\d+'))
        self.assert_results([(2,14)], results)

    def assert_results(self, expected_results, results):
        self.assertEqual(len(expected_results), len(results))
        for i, result in enumerate(results):
            self.assertEqual(expected_results[i], result)

class ConfParserTests(unittest.TestCase):
    def setUp(self):
        conf = open('%s/test.txts.conf' % _TEST_DATA_DIR)
        try:
            self.confparser = ConfParser(conf.readlines())
        finally:
            conf.close()
        
        self.expected_styles = []

    def tearDown(self):
        self.confparser = None
        self.expected_styles = None

    def expect_regex_style(self, pattern, transforms, apply_to_whole_line=False):
        self.expected_styles.append(RegexStyle(pattern, transforms, apply_to_whole_line))

    def expect_index_style(self, regions, transforms):
        self.expected_styles.append(IndexStyle(regions, transforms))

    def test_example_style(self):
        styles = self.confparser.get_styles('example')
        self.expect_regex_style(r'error', ['red'], True)
        self.expect_regex_style(r'evil\.org', ['red'])
        self.expect_regex_style(r'\d{4}-\d\d-\d\d', ['green'])
        self.expect_regex_style(r'\d\d:\d\d:\d\d', ['green', 'bold'])
        self.expect_regex_style(r'\d+\.\d+\.\d+\.\d+(:\d+)?', ['yellow', 'underline'])
        self.expect_regex_style(r'\[samplesession\]', ['magenta'])
        self.expect_regex_style(r'\[[^\]]+\]', ['blue'])
        self.expect_regex_style(r'\b\d+\b', ['cyan', 'bold'])
        self.assert_regex_styles(styles)

    def test_get_first(self):
        styles = self.confparser.get_styles('first')
        self.expect_regex_style(r'some error', ['red'])
        self.expect_regex_style(r'\d\d-\d\d-\d\d\d\d', ['blue'])
        self.expect_regex_style(r'some pattern', ['green'])
        self.expect_regex_style(r'\[(xyz.*x+y?z+)\]', ['underline'])
        self.assert_regex_styles(styles)
        
    def test_get_second(self):
        styles = self.confparser.get_styles('second')
        self.expect_regex_style('\w+', ['blue'])
        self.assert_regex_styles(styles)

    def test_get_third(self):
        styles = self.confparser.get_styles('third')
        self.expect_regex_style(r':on-red : \d+', ['on-red'])
        self.expect_regex_style(r'\\:\\[\s+]foo.*(foo).*bar\\\\', ['grey'])
        self.expect_regex_style(r': double: quotes', ['yellow'])
        self.assert_regex_styles(styles)

    def test_get_fourth(self):
        styles = self.confparser.get_styles('fourth')
        assert styles == []

    def test_get_fifth(self):
        self.assert_style_error(
            'fifth', 'Invalid style definition: green regex("some pattern")')
        
    def test_get_sixth(self):
        try:
            styles = self.confparser.get_styles('sixth')
            self.fail('should fail on invalid style key')
        except Exception as e:
            self.assertEqual(e.args[0], 'Invalid style key: "some-bad-key"')

    def test_get_seventh(self):
        styles = self.confparser.get_styles('seventh')
        self.expect_regex_style(r':.*\d\s\'\"', ['blue', 'on-white'])
        self.expect_regex_style(r'\"', ['125', 'on-245'])
        self.assert_regex_styles(styles)

    def test_get_eighth(self):
        styles = self.confparser.get_styles('eighth')
        self.expect_regex_style(r'org.[\w+|\.]+', ['red'])
        self.assert_regex_styles(styles)

    def test_get_ninth(self):
        styles = self.confparser.get_styles('ninth')
        self.expect_regex_style(r'error', ['red'], True)
        self.expect_regex_style(r'another error', ['red', 'bold'], True)
        self.assert_regex_styles(styles)

    def test_get_tenth(self):
        expected_error = 'Invalid style definition: red:' \
            + ' regex("bad") # can\'t comment here'
        self.assert_style_error('tenth', expected_error)

    def test_get_eleventh(self):
        styles = self.confparser.get_styles('eleventh')
        self.expect_index_style([(0,8)], ['green'])
        self.expect_index_style([(9,13)], ['160', 'bold'])
        self.expect_index_style([(15,18)], ['215'])
        self.expect_index_style([(20,24)], ['115'])
        self.expect_index_style([(26,31)], ['162'])
        self.expect_index_style([(65,200)], ['48'])
        self.assert_index_styles(styles)

    def test_get_twelfth(self):
        styles = self.confparser.get_styles('twelfth')
        self.expect_index_style([(0,8)], ['18', 'on-45'])
        self.expect_index_style([(13,18), (20,22)], ['yellow'])
        self.assert_index_styles(styles)

    def test_get_thirteenth(self):
        self.assert_style_error(
            'thirteenth', 'Invalid style definition: blue: index()')

    def test_get_undefined(self):
        self.assert_style_error('FOO', 'Style "FOO" is not defined')

    def assert_regex_styles(self, styles):
        self.assertEqual(len(self.expected_styles), len(styles))
        for i, style in enumerate(styles):
            expected = self.expected_styles[i]
            self.assertEqual(expected.regex_obj.pattern, style.regex_obj.pattern)
            self.assertEqual(expected.transforms, style.transforms)
            msg = "Expected apply_to_whole_line=%s for %r" % (expected.apply_to_whole_line, style)
            self.assertEqual(expected.apply_to_whole_line, style.apply_to_whole_line, msg)

    def assert_index_styles(self, styles):
        self.assertEqual(len(self.expected_styles), len(styles))
        for i, style in enumerate(styles):
            expected = self.expected_styles[i]
            self.assertEqual(expected.regions, style.regions)
            self.assertEqual(expected.transforms, style.transforms)

    def assert_style_error(self, style, expected_error_msg):
        try:
            styles = self.confparser.get_styles(style)
            self.fail('should fail on invalid style definition')
        except Exception as e:
            self.assertEqual(e.message, expected_error_msg)

class TransformerTests(unittest.TestCase):
    
    def test_substring_style(self):
        input_line = "some text..."
        # <red>some<default> text...<default>
        expected_output_line = "\033[31msome\033[m text...\033[m"

        self.assert_styled_line([IndexStyle([(0,4)], ["red"])],
                                input_line, expected_output_line)

        self.assert_styled_line([RegexStyle("some", ["red"])],
                                input_line, expected_output_line)
        

    def test_whole_line_style(self):
        input_line = "some text..."
        # <red>some text...<default>
        expected_output_line = "\033[31msome text...\033[m"

        self.assert_styled_line([RegexStyle("some", ["red"], apply_to_whole_line=True)],
                                input_line, expected_output_line)

        self.assert_styled_line([RegexStyle("some text...", ["red"], apply_to_whole_line=False)],
                                input_line, expected_output_line)

        self.assert_styled_line([IndexStyle([(0, len(input_line))], ["red"])],
                                input_line, expected_output_line)

        # if end > line length, default to line length 
        self.assert_styled_line([IndexStyle([(0, 99999)], ["red"])],
                                input_line, expected_output_line)

    def assert_styled_line(self, styles, input_line, expected_output_line):
        transformer = Transformer(styles)
        actual_output_line = transformer.style(input_line)
        self.assertEqual(expected_output_line, actual_output_line)

    def test_removing_styles_is_equal_to_original_line(self):
        """Style a line, remove escape sequences and compare to the original
        """
        styles = [
            RegexStyle("http:[\w+|/+|:]+", ["red"]),
            RegexStyle("^\w\w\w \d\d\s?", ['white', 'on-magenta']),
            RegexStyle("\d\d:\d\d:\d\d", ['bold', 'on-blue']),
            RegexStyle(".*<warn>.*", ['yellow']),
            RegexStyle("\((.*)\)", ['red', 'on-white']),
            RegexStyle("\[(.*)\]", ['grey', 'bold']),
            ]
        transformer = Transformer(styles)
        lines = self.get_lines('%s/test-log' % _TEST_DATA_DIR)

        for original_line in lines:
            original_line = original_line.strip('\n')
            styled_line = transformer.style(original_line)
            styled_line = styled_line.encode('unicode_escape').decode('utf-8')
            unstyled_line = self.remove_styles(styled_line)
            self.assertEqual(original_line, unstyled_line)

    def remove_styles(self, line):
        unstyled = line.replace(r'\x1b[m', '', 1000)
        unstyled = unstyled.replace("\\'", "'", 1000)
        for style_key in _STYLES:
            transform = _STYLES[style_key]
            escape_code = transform.encode('unicode_escape').decode('utf-8')
            unstyled = unstyled.replace(escape_code, '', 1000)
        return unstyled

    def get_lines(self, fname):
        with open(fname, 'r') as f:
            return f.readlines()


if __name__ == "__main__":
    unittest.main()
