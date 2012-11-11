import re
import transformer

class LineStyleProcessor(object):

    def get_region_map(self, line, styles):
        region_map = {}
        line_is_clean = True
        line_length = len(line)
        occupied = [False for i in range(line_length)]

        for style in styles:
            regions = []
            apply_to_whole_line = False

            if isinstance(style, transformer.IndexStyle):
                regions = style.regions
            else:
                regions = self.find_regions(line, style.regex_obj)
                apply_to_whole_line = style.apply_to_whole_line

            if apply_to_whole_line and regions:
                if line_is_clean:
                    region = (0, line_length - 1)
                    region_map[region] = style
                    break # can't apply any more styles
                else:
                    # skip since other styles
                    # have already been applied
                    continue

            for region in regions:
                start = region[0]
                end = min(region[1] + 1, line_length)
                overlaps = any(occupied[start : end])

                if not overlaps:
                    for i in range(start, end):
                        occupied[i] = True
                    region_map[region] = style
                    line_is_clean = False

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

