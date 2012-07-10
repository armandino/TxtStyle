from regionmatcher import RegionMatcher

class StyleRegions:
    def __init__(self, style, regions):
        self.style = style
        self.regions = regions

class LineStyleProcessor:

    def __init__(self):
        self.regionmatcher = RegionMatcher()

    def get_elected_regions(self, line, styles):
        style_regions = []
        
        for style in styles:
            candidate_regions = self.regionmatcher.find_regions(line, style.regex_obj)
            style_region = StyleRegions(style, candidate_regions)
            style_regions.append(style_region)
        
        # region map represents elected regions (i.e. no overlaps)
        return self._get_elected_region_map(line, style_regions)

    def _get_elected_region_map(self, line, style_regions):
        """\
        Takes a style map (style -> candidate regions) and
        removes overlapping regions.
        
        Returns a flattened map of elected regions (region -> style).
        """
        region_map = {}
        occupied_indexes = [False for i in range(len(line))]
        
        for style_region in style_regions:
            for region in style_region.regions:
                start, end = region[0], region[1] + 1
                overlaps = any(occupied_indexes[start : end])
                
                if not overlaps:
                    for i in range(start, end):
                        occupied_indexes[i] = True
                    region_map[region] = style_region.style
                    
        return region_map
