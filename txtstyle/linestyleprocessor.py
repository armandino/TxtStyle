import re

class LineStyleProcessor:

    def get_region_map(self, line, styles):
        region_map = {}
        occupied = [False for i in range(len(line))]

        for style in styles:
            regions = self.find_regions(line, style.regex_obj)

            for region in regions:
                start, end = region[0], region[1] + 1
                overlaps = any(occupied[start : end])

                if not overlaps:
                    for i in range(start, end):
                        occupied[i] = True
                    region_map[region] = style

        return region_map

    def find_regions(self, line, regex_obj):
        """\
        Returns a list of tuples (start, end) matching the regex.
        """
        if not regex_obj:
            return []
        
        if isinstance(regex_obj, re._pattern_type) and not regex_obj.pattern:
            return []

        return [(m.start(0), m.end(0) - 1) for m in re.finditer(regex_obj, line)]

