
import re

class RegionMatcher:

    def find_regions(self, line, regex_obj):
        """\
        Returns a list of regions represented as tuples (start, end)
        matching the regex.
        """
        search_tokens = self._get_unique_search_tokens(line, regex_obj)
        found_regions = []
        for token in search_tokens:
            matching_regions = self._find_regions(line, token)

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

    def _find_regions(self, string, token):
        """\
        Returns a list of regions (start, end) matching the token.
        """
        if not token:
            return []
        
        results = []
        offset = 0
        string_len = len(string)
        
        while True:
            idxs = string.find(token, offset, string_len)
            if idxs == -1:
                break
            
            token_len = len(token)
            if token_len == 1:
                idxe = idxs
                offset = idxe + 1
            else:
                idxe = idxs + token_len - 1
                offset = idxe
            
            result = (idxs, idxe)
            results.append(result)

        return results
