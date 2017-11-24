import logging
from gstools import restutils

# enable logging for requests
try:
    from http.client import HTTPConnection  # py3
except ImportError:
    from httplib import HTTPConnection  # py2

    HTTPConnection.debuglevel = 2
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

user = 'admin'
psw = 'geoserver'
auth = (user, psw)

base_url = "http://localhost:8080/geoserver"

shapefile_root_path = 'in/data/vector/waves-height-isolines'
shapefile_name = 'isolines'
netcdf_path = 'in/data/raster/tas.nc.zip'
sld_path = 'in/styles/redline.sld'
body_file_path = 'in/xml/layer_bopen-tas_mod.xml'


def test_create_feature_from_shapefile():
    restutils.create_feature_from_shapefile(auth,
                                            base_url,
                                            'bopen',
                                            'wave-height-isolines',
                                            shapefile_root_path,
                                            shapefile_name)


def test_create_coverage_from_zipped_netcdf():
    restutils.create_coverage_from_zipped_netcdf(auth,
                                                 base_url,
                                                 'bopen',
                                                 'tas',
                                                 netcdf_path)


def test_create_style_from_sld_file():
    restutils.create_style_from_sld_file(auth,
                                         base_url,
                                         sld_path,
                                         'bopen-stile')


def test_get_cached_layers():
    restutils.get_cached_layers(auth, base_url)


def test_get_cached_layer():
    restutils.get_cached_layer(auth, base_url, 'bopen:tas')


def test_update_cached_layer():
    restutils.update_cached_layer(auth, base_url, 'bopen:tas', body_file_path)
