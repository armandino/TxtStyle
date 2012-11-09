import re
import unittest

from confparser import ConfParser
from linestyleprocessor import LineStyleProcessor
import transformer

def regex(pattern):
    return re.compile(pattern)

class LineStyleProcessorTests(unittest.TestCase):
    def setUp(self):
        self.lineStyleProcessor = LineStyleProcessor()
        self.find_regions = self.lineStyleProcessor.find_regions


    def test_get_region_map(self):
        #       0123456789012345678901234567890123456789
        line = "This is a long string forty chars long.."
        
        s1 = transformer.Style(regex("This"), None)
        s2 = transformer.Style(regex("is"), None)
        s3 = transformer.Style(regex("s"), None)

        styles = [s1, s2, s3]
        
        region_map = self.lineStyleProcessor.get_region_map(
            line, styles)
        
        regions = region_map.keys()
        regions.sort()
        
        self.assert_results([(0,3), (5,6), (15,15),
                             (32,32)], regions)
        
        self.assertEqual(region_map[(0,3)], s1)
        self.assertEqual(region_map[(5,6)], s2)
        self.assertEqual(region_map[(15,15)], s3)
        self.assertEqual(region_map[(32,32)], s3)


    def test_get_region_map_reverse_order(self):
        #       0123456789012345678901234567890123456789
        line = "This is a long string forty chars long.."
        
        s1 = transformer.Style(regex("s"), None)
        s2 = transformer.Style(regex("is"), None)
        s3 = transformer.Style(regex("This"), None)

        styles = [s1, s2, s3]
        
        region_map = self.lineStyleProcessor.get_region_map(
            line, styles)
        
        regions = region_map.keys()
        regions.sort()
        
        self.assert_results([(3,3), (6,6), (15,15),
                             (32,32)], regions)
        
        self.assertEqual(region_map[(3,3)], s1)
        self.assertEqual(region_map[(6,6)], s1)
        self.assertEqual(region_map[(15,15)], s1)
        self.assertEqual(region_map[(32,32)], s1)

    def assert_results(self, expected_results, results):
        self.assertEquals(len(expected_results), len(results))
        for i, result in enumerate(results):
            self.assertEqual(expected_results[i], result)

    def test_repeated_invocation_returns_new_list(self):
        results1 = self.find_regions('string', 'in')
        results2 = self.find_regions('string', 'in')
        self.assertIsNot(results1, results2)
        self.assert_results([(3,4)], results1)
        self.assert_results([(3,4)], results2)

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
        self.assert_results([(0,3)], results)

        results = self.find_regions('my string', 'string')
        self.assert_results([(3,8)], results)

    def test_single_char_match(self):
        results = self.find_regions('a', 'a')
        self.assert_results([(0,0)], results)

        results = self.find_regions('aaaaa', 'a')
        self.assert_results([(0,0), (1,1), (2,2), (3,3), (4,4)], results)

        results = self.find_regions('axaxa', 'a')
        self.assert_results([(0,0), (2,2), (4,4)], results)

        results = self.find_regions('foo', 'f')
        self.assert_results([(0,0)], results)

        results = self.find_regions('foo', 'o')
        self.assert_results([(1,1), (2,2)], results)
        
    def test_consecutive_matches(self):
        results = self.find_regions('isisis', 'is')
        self.assert_results([(0,1), (2,3), (4,5)], results)

        results = self.find_regions('isisisis', 'is')
        self.assert_results([(0,1), (2,3), (4,5), (6,7)], results)

        results = self.find_regions('x isis', 'is')
        self.assert_results([(2,3), (4,5)], results)
        #                              0         1         2
        #                              012345678901234567890
        results = self.find_regions('this is his list isis', 'is')
        self.assert_results([(2,3), (5,6), (9,10),
                             (13,14), (17,18), (19,20)], results)

    def test_find_regions_with_simple_regex(self):
        results = self.find_regions('x-11-11', regex('\d+'))
        self.assert_results([(2,3), (5,6)], results)

        results = self.find_regions('01-3456-11-11', regex('\d+'))
        self.assert_results([(0,1), (3,6), (8,9), (11,12)], results)

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
        
        results = self.find_regions(" '192.168.99.1'", regex('\d+\.\d+\.\d+\.\d+'))
        self.assert_results([(2,13)], results)

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
        except Exception, e:
            self.assertEqual(e.message, 'Invalid style definition: green "some pattern"')
        
    def test_get_sixth(self):
        try:
            styles = self.confparser.get_styles('sixth')
            self.fail('should fail on invalid style key')
        except Exception, e:
            self.assertEqual(e.message, 'Invalid style key: "some-bad-key"')

    def test_get_seventh(self):
        styles = self.confparser.get_styles('seventh')
        self.expect_style(r':.*\d\s\'\"', ['blue', 'on-white'])
        self.assert_styles(styles)

    def test_get_eighth(self):
        styles = self.confparser.get_styles('eighth')
        self.expect_style(r'org.[\w+|\.]+', ['red'])
        self.assert_styles(styles)

    def test_get_ninth(self):
        styles = self.confparser.get_styles('ninth')
        self.expect_style(r'Exception', ['red', 'bold'])
        self.assert_styles(styles, True)

    def test_get_undefined(self):
        try:
            styles = self.confparser.get_styles('FOO')
            self.fail('should fail on undefined  style name')
        except Exception, e:
            self.assertEqual(e.message, 'Style "FOO" is not defined')

    def assert_styles(self, styles, apply_to_whole_line=False):
        self.assertEquals(len(self.expected_styles), len(styles))
        for i, style in enumerate(styles):
            expected = self.expected_styles[i]
            self.assertEqual(expected.regex_obj.pattern, style.regex_obj.pattern)
            self.assertEqual(expected.transforms, style.transforms)
            self.assertEquals(apply_to_whole_line, style.apply_to_whole_line)


class TransformerTests(unittest.TestCase):
    def setUp(self):
        Style = transformer.Style
        styles = [
            Style("http:[\w+|/+|:]+", ["red"]),
            Style("^\w\w\w \d\d\s?", ['white', 'on-magenta']),
            Style("\d\d:\d\d:\d\d", ['bold', 'on-blue']),
            Style(".*<warn>.*", ['yellow']),
            Style("\((.*)\)", ['red', 'on-white']),
            Style("\[(.*)\]", ['grey', 'bold']),
            ]
        self.transformer = transformer.Transformer(styles)
        self.lines = self.get_lines('testdata/test-log')
    
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
        for style_key in transformer._STYLES:
            transform = transformer._STYLES[style_key]
            escape_code = transform.encode('string_escape')
            unstyled = unstyled.replace(escape_code, '', 1000)
        return unstyled

if __name__ == "__main__":
    unittest.main()
