from collections import OrderedDict
from regionmatcher import RegionMatcher

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
        return self.__get_elected_region_map__(line, style_map)

    def __get_elected_region_map__(self, line, style_map):
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
                region_indexes = range(region[0], region[1]+1) # inclusive range
                overlaps = self.__region_overlaps__(region_indexes, index_occupied)
                
                if not overlaps:
                    self.__occupy_indexes__(region_indexes, index_occupied)
                    region_map[region] = style
        return region_map

    def __region_overlaps__(self, region_indexes, index_occupied):
        for i in region_indexes:
            if index_occupied[i]:
                return True
        return False

    def __occupy_indexes__(self, region_indexes, index_occupied):
        for i in region_indexes:
            index_occupied[i] = True

