from geoserver.catalog import Catalog
from geoserver import util
import requests
import os, errno


def create_feature_from_shapefile(auth,
                                  base_url,
                                  target_ws_name,
                                  target_ds_name,
                                  shapefile_root_path,
                                  shapefile_name):

    cat = Catalog(base_url + '/rest', username=auth[0], password=auth[1])

    if not cat.get_workspace(target_ws_name):
        cat.create_workspace(target_ws_name, base_url + '/rest/workspaces/' +
                             target_ws_name)

    ws = cat.get_workspace(target_ws_name)
    data = util.shapefile_and_friends(shapefile_root_path + '/' +
                                      shapefile_name)

    cat.create_featurestore(target_ds_name, data, ws, overwrite=True)

    # When a new data store is created a new GeoServer layers is automatically
    # added using the shapefile name as name for the layer.
    # When a new data store is created a new GeoWebCache layers is
    # automatically added using the shapefile name as name for the layer.
    # Changing the target data store will result in both a new store
    # and new layers.


def create_coverage_from_zipped_netcdf(auth,
                                       base_url,
                                       target_ws_name,
                                       target_cs_name,
                                       netcdf_path):
    put_url = base_url \
            + '/rest/workspaces/' \
            + target_ws_name \
            + '/coveragestores/' \
            + target_cs_name \
            + '/file.netcdf'

    headers = {'Content-Type': 'application/zip'}
    with open(netcdf_path) as data:
        requests.put(put_url, headers=headers, auth=auth, data=data)

    # When a new coverage store is created a new GeoServer layer is
    # automatically added using the internal netcdf variable name as name
    # for the layer.
    # When a new coverage store is created a new GeoWebCache layer is
    # automatically added using the internal netcdf variable name as name
    # for the layer.
    # Changing the target coverage store will not result in new layers
    # if both the target workspace and the internal netcdf variable
    # name are preserved.


def create_style_from_sld_file(auth, base_url, file_path, style_name):
    with open(file_path) as f:
        cat = Catalog(base_url + '/rest', username=auth[0], password=auth[1])
        cat.create_style(style_name, f.read(), overwrite=True)


def get_cached_layers(auth, base_url):
    try:
        os.makedirs('../out')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    url = base_url + '/gwc/rest/layers.xml'
    response = requests.get(url, auth=auth)
    # print response.content
    with open('../out/layers.xml', 'w') as f:
        f.write(response.content)


def get_cached_layer(auth, base_url, layer_name):
    try:
        os.makedirs('../out')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    url = base_url + '/gwc/rest/layers/' + layer_name + '.xml'
    response = requests.get(url, auth=auth)

    layer_name = '-'.join(layer_name.split(':'))

    filename = 'layer_{}.xml'.format(layer_name)
    with open('../out/' + filename, 'w') as f:
        f.write(response.content)


def update_cached_layer(auth, base_url, layer_name, body_file_path):
    url = base_url + '/gwc/rest/layers/' + layer_name + '.xml'
    headers = {'Content-Type': 'text/xml'}
    data = open(body_file_path)
    requests.put(url, auth=auth, headers=headers, data=data)
