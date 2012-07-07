
import re

class RegionMatcher:

    def find_regions(self, line, regex_obj):
        """\
        Returns a list of regions represented as tuples (start, end)
        matching the regex.
        """
        search_tokens = self._get_unique_search_tokens(line, regex_obj)
        found_regions = []
        for searchstr in search_tokens:
            matching_regions = self._find_regions(line, searchstr)

            if matching_regions:
                found_regions.extend(matching_regions)

        return found_regions


    def _get_unique_search_tokens(self, line, regex_obj):
        """\
        Returns a list of unique search tokens that match the regex eg.
        Given "foo 12 bar 34" and regex "\d\d" returns: ['12', '34']
        """
        search_tokens = []
        it = re.finditer(regex_obj, line)
        for match in it:
            token = match.group(0)
            if token not in search_tokens:
                search_tokens.append(token)

        if len(search_tokens) == 1 and search_tokens[0] == '':
            return []
        else:
            return search_tokens

    def _find_regions(self, s, searchstr):
        regions = []
        offset = 0
        remainder = s
        while True:
            remainder, offset = self._collect_regions(remainder, searchstr, regions, offset)
            if not remainder:
                break

        return regions

    def _collect_regions(self, s, searchstr, results=[], offset=0):
        if not searchstr:
            return '', 0
        
        if searchstr == s and offset == 0:
            # if whole string match (when offset > 0, we're processing remainder)
            results.append((0, len(s) - 1))
            return '', 0

        start = s.find(searchstr)
        if start == -1:
            return '', 0

        # snip non-matching front
        # e.g. search 'cat' in 'black cat' -> '[black ]cat'
        remainder = s[start:]

        # remove first occurance of searchstr in s
        if remainder == searchstr:
            remainder = ''
        else:
            # escape in case searchstr has regex characters in it
            remainder = re.sub(re.escape(searchstr), '', remainder, 1)

        # Calculate region (start, end)
        if remainder == '':
            end = len(s) - 1
        else:
            # e.g. search 'o' in 'clock' (2,2)
            if len(searchstr) == 1:
                end = start
            # e.g. search 'is' in 'isisis' (remainder = 'isis')
            elif s.startswith(remainder):
                end = len(searchstr) - 1
            # eg. search 'is' in 'isis'
            elif remainder == searchstr:
                end = len(searchstr) * 2 - 1
            else:
                end = s.find(remainder) - 1

                if (end < start):
                    end = start - 1
                    # when searching through multiple occurrences, e.g. '-11' in 'foo-11-11'
                    while (end < start and end >= 0):
                        end = s.find(remainder, end + len(remainder), len(s)) - 1

        result = (start + offset, end + offset)
        results.append(result)
        offset = offset + end + 1
        return remainder, offset

