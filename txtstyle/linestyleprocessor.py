from regionmatcher import RegionMatcher
from ordereddict import OrderedDict

class LineStyleProcessor:

    def __init__(self):
        self.regionmatcher = RegionMatcher()

    def get_elected_regions(self, line, styles):
        # style -> candidate regions
        style_map = OrderedDict()        
        
        for style in styles:
            candidate_regions = self.regionmatcher.find_regions(line, style.regex_obj)
            style_map[style] = candidate_regions
        
        # region map represents elected regions (i.e. no overlaps)
        return self._get_elected_region_map(line, style_map)

    def _get_elected_region_map(self, line, style_map):
        """\
        Takes a style map (style -> candidate regions) and
        removes overlapping regions.
        
        Returns a flattened map of elected regions (region -> style)
        ordered by region in ascending order.
        """
        region_map = {}
        index_occupied = [False for i in range(len(line))]
        for style, regions in style_map.items():
            
            for region in regions:
                region_indexes = range(region[0], region[1] + 1) # inclusive range
                overlaps = self._region_overlaps(region_indexes, index_occupied)
                
                if not overlaps:
                    self._occupy_indexes(region_indexes, index_occupied)
                    region_map[region] = style
        return region_map

    def _region_overlaps(self, region_indexes, index_occupied):
        for i in region_indexes:
            if index_occupied[i]:
                return True
        return False

    def _occupy_indexes(self, region_indexes, index_occupied):
        for i in region_indexes:
            index_occupied[i] = True

