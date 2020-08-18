import ee
def get_CO(coordenates):

    service_account = 'some_stuff@some_stuff.iam.gserviceaccount.com'
    credentials = ee.ServiceAccountCredentials(service_account, 'privatekey.json')
    ee.Initialize(credentials)

    roi = ee.Geometry.Polygon(coordenates)

    #Choosing the satelite and filtrate with GEE functions
    collection = ee.ImageCollection('COPERNICUS/S5P/NRTI/L3_CO')
    collection = collection.select('CO_column_number_density').filterDate('2020-01-01', '2020-01-31').filterBounds(roi)
    collection_mean = collection.mean()
    mean_cliped = collection_mean.clip(roi)

    #Obtaining min, mean, and max values as dictionaries.
    minMaxImage = mean_cliped.select("CO_column_number_density").reduceRegion(reducer=ee.Reducer.minMax(), geometry=roi, scale=10, maxPixels= 1e10)
    medImage = mean_cliped.select("CO_column_number_density").reduceRegion(reducer=ee.Reducer.mean(), geometry=roi, scale=10, maxPixels= 1e10)
    minMaxDic = ee.Dictionary(minMaxImage)

    #Retreaving one value out of the dictionary
    med = ee.Number(medImage.get("CO_column_number_density"))
    min = ee.Number(minMaxDic.get('CO_column_number_density_min'))
    max = ee.Number(minMaxDic.get('CO_column_number_density_max'))

    #This is the pallet we will be using
    band_viz = {
        'min': 0,
        'max': 0.05,
        'palette': ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']
    }

    #Data map by url.
    ee_image_object = mean_cliped.updateMask(mean_cliped.gt(0))
    map_id_dict = ee.Image(ee_image_object).getMapId(band_viz)
    tilesURL = map_id_dict['tile_fetcher'].url_format

    #All the information obtained in a dictionary
    CO_dictionary = {
        'id': "CO",
        'units': "mol/m^2",
        'tileURL': tilesURL,
        'min': min.getInfo(),
        'med': med.getInfo(),
        'max': max.getInfo()
    }

    return CO_dictionary
