from regionmatcher import RegionMatcher

class LineStyleProcessor:

    def __init__(self):
        self.regionmatcher = RegionMatcher()

    def get_elected_regions(self, line, styles):
        region_map = {}
        occupied_indexes = [False for i in range(len(line))]

        for style in styles:
            candidate_regions = self.regionmatcher.find_regions(line, style.regex_obj)

            for region in candidate_regions:
                start, end = region[0], region[1] + 1
                overlaps = any(occupied_indexes[start : end])

                if not overlaps:
                    for i in range(start, end):
                        occupied_indexes[i] = True
                    region_map[region] = style

        # region map represents elected regions (i.e. no overlaps)
        return region_map
