
import re

class RegionMatcher:

    def find_regions(self, line, regex_obj):
        """\
        Returns a list of tuples (start, end) matching the regex.
        """
        if not regex_obj:
            return []
        
        if isinstance(regex_obj, re._pattern_type) and not regex_obj.pattern:
            return []

        return [(m.start(0), m.end(0) - 1) for m in re.finditer(regex_obj, line)]

