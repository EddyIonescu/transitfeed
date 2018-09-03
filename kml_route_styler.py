"""
Helper for kmlwriter that takes in a CSV and outputs
which style (color and visibility) a route should have.
Matching is done based on route_short_name.

CSVs are made in Excel with the following format:
Agency_ID | Route_ID | Color | Hidden_Shapes

Usage:
route_styler = KMLRouteStyler()
route_styler.create_routes(csv_path='something.csv')
route_styler.validate_csv_input(agency_id, route_ids)

Hidden_Shapes is a comma-separated string containing the shape IDs
of shapes that should be removed.

Note that all columns are required, and that a color must always be defined
"""
import pandas as pd
import warnings

class KMLRouteStyler():

    def __init__(self, csv_path):
        """Load CSV given by kmlwriter and make it accessible in a dict
        
        :param csv_path: path to the CSV file
        :type csv_path: string
        """
        # (Agency_ID, Route_ID): Color
        # if key doesn't exist, then route shouldn't be visible
        self.routes = {}
        route_df = pd.read_csv(csv_path)
        print 'Loaded {csv_path}'.format(csv_path=csv_path)
        print route_df.head()       
        column_props = ['Color', 'Hidden_Shapes']
        routes = {}
        for index, route in route_df.iterrows():
            routes[(route['Agency_ID'], route['Route_ID'])] = {
                prop: route[prop] for prop in column_props
            }
        self.routes = routes
        print 'Loaded {num_routes} routes'.format(num_routes=len(routes))

    def route_is_visible(self, agency_id, route_id):
        """Determine whether we should draw the route
        
        :param agency_id: ID of transit agency (eg. Muni)
        :type agency_id: string
        
        :param route_id: ID of route (eg. 5)
        :type route_id: string

        :return: whether we draw the route
        :rtype: boolean
        """
        return self.routes.get((agency_id, route_id), False)

    def shape_is_visible(self, agency_id, route_id, shape_id):
        """Determine whether the shape is in Hidden_Shapes in the provided CSV
        Throws if agency/route pair not found, so route_is_visible should
        always be called first.
        
        :param agency_id: ID of transit agency (eg. Muni)
        :type agency_id: string
        
        :param route_id: ID of route (eg. 5)
        :type route_id: string

        :param shape_id: ID of shape (eg. 159174)
        :type shape_id: string

        :return: whether to show the shape or not 
        :rtype: boolean
        """
        hidden_shape_str = self.routes[(agency_id, route_id)]['Hidden_Shapes']
        # pandas default value for empty csv cell value is NaN (float)
        if not isinstance(hidden_shape_str, basestring):
            return True
        hidden_shapes = hidden_shape_str.split(',')
        return shape_id not in hidden_shapes

    def get_route_color(self, agency_id, route_id):
        """Get color to draw the route in from the provided CSV
        Throws if agency/route pair not found, so route_is_visible should
        always be called first.
        
        :param agency_id: ID of transit agency (eg. Muni)
        :type agency_id: string
        
        :param route_id: ID of route (eg. 5)
        :type route_id: string

        :return: color, in hex, to draw the route in (eg. FF0000)
                 no hashtag as GTFS format defines it as six characters long
        :rtype: string
        """
        color = self.routes[(agency_id, route_id)]['Color'].strip()
        if len(color) == 7:
            return color[1:] # remove the hashtag in the front
        elif len(color) == 6:
            return color
        raise ValueError('Expected hexadecimal string for color %s' % color)

    def validate_csv_input(self, agency_id, route_ids):
        """Validates CSV input by ensuring that all routes in CSV
        are in the GTFS for the same agency. Throws if a route
        in the CSV for that agency is not in route_ids

        :param agency_id: ID of transit agency (eg. Muni)
        :type agency_id: string

        :param route_ids: IDs of routes loaded in GTFS for that agency (eg. 5, 6, 7)
        :type route_ids: list of strings
        """
        routes = {(_agency_id, _route_id) for (_agency_id, _route_id) in self.routes if _agency_id == agency_id}
        if len(routes) == 0:
            warnings.warn('Provided CSV has zero routes for agency %s' % agency_id)
            # raise ValueError('Provided CSV has zero routes for agency %s' % agency_id)
        route_ids = {route_id for route_id in route_ids}
        for (_agency_id, _route_id) in routes:
            if _route_id not in route_ids:
                raise ValueError(
                    'Expected %s to be in %s but was not, check your route naming in the CSV provided' % (
                        _route_id,
                        route_ids,
                ))

