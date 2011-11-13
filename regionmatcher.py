
import re

class RegionMatcher:

    def find_regions(self, line, regex_obj):
        """\
        Returns a list of regions represented as tuples (start, end)
        matching the regex.
        """
        search_tokens = self.__get_unique_search_tokens__(line, regex_obj)
        found_regions = []
        
        for searchstr in search_tokens:
            matching_regions = self.__find_regions__(line, searchstr)
            if matching_regions:
                found_regions += matching_regions

        return found_regions


    def __get_unique_search_tokens__(self, line, regex_obj):
        """\
        Returns a list of unique search tokens that match the regex eg.
        Given "foo 12 bar 34" and regex "\d\d" returns: ['12', '34']
        """
        search_tokens = []
        # TODO: use r for rawstring
        it = re.finditer(regex_obj, line)
        for match in it:
            token = match.group(0)
            if token not in search_tokens:
                search_tokens.append(token)

        if len(search_tokens) == 1 and search_tokens[0] == '':
            return []
        else:
            return search_tokens


    def __find_regions__(self, s, searchstr):
        return self.__recursive_find_regions_internal__(s, searchstr, 0, [])
    

    def __recursive_find_regions_internal__(self, s, searchstr,
                                            offset=0, results=[]):
        if not searchstr:
            return []
        # if whole string match (when offset > 0, we're processing remainder)
        if searchstr == s and offset == 0:
            return [(0, len(s)-1)]

        start = s.find(searchstr)
        if start != -1:
            # snip non-matching front
            # e.g. search 'cat' in 'black cat' -> '[black ]cat'
            remainder = s[start:]
            
            # remove first occurance of searchstr in s
            print "-----------------------------------"
            print "S: <<%s>>" % s
            print "SEARCHSTR: <<%s>>" % searchstr
            print "REMAINDER: <<%s>>" % remainder
            remainder = re.sub(searchstr, '', remainder, 1)

            if remainder == '':
                end = len(s)-1
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

            result = (start + offset, end + offset)
            results.append(result)
            offset = offset + end + 1
            self.__recursive_find_regions_internal__(
                remainder, searchstr, offset, results)

        return results
