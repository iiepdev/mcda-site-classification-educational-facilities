"""
Model exported as python.
Name : Natural Hazard Risk for Schools
Group : 
With QGIS : 31802
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterBoolean
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterVectorDestination
import processing


class NaturalHazardRiskForSchools(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterBoolean('Performlayerreprojections', 'Perform layer reprojections', defaultValue=False))
        self.addParameter(QgsProcessingParameterBoolean('Reclassifyrasterlayers', 'Reclassify raster layers', defaultValue=False))
        self.addParameter(QgsProcessingParameterVectorLayer('Sitearea', 'Site area (polygon)', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('schoollocations', 'Exposure Sites (point)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('hazardlayers', 'Hazard layer 1', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('hazardlayer2', 'Hazard layer 2', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('hazardlayer3', 'Hazard layer 3', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('hazardlayer4optional', 'Hazard layer 4 (optional)', optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('hazardlayer5optional', 'Hazard layer 5 (optional)', optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('Hazardlayer6optional', 'Hazard layer 6 (optional)', optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('HazardIndexPerformingReclassificationsWithNoReprojections', 'Hazard Index - Performing reclassifications with no reprojections', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('HazardIndexPerformingLayerReprojectionsAndPerformingReclassifications', 'Hazard Index - Performing layer reprojections and performing reclassifications', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('HazardIndexWithoutPerformingLayerReprojectionsNorReclassifications', 'Hazard Index - Without performing layer reprojections nor reclassifications', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('HazardIndexPerformingLayerReprojectionsWithNoReclassifications', 'Hazard Index - Performing layer reprojections with no reclassifications', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('SchoolHazardIndex', 'School Hazard Index', type=QgsProcessing.TypeVectorPoint, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('SchoolHazardIndexPerformingLayerReprojectionsWithNoReclassifications', 'School Hazard Index - Performing layer reprojections with no reclassifications', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('SchoolHazardIndexPerformingLayerReprojectionsAndPerformingReclassifications', 'School Hazard Index - Performing layer reprojections and performing reclassifications', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('SchoolHazardIndexPerformingReclassificationsWithNoReprojections', 'School Hazard Index Performing reclassifications with no reprojections', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterBoolean('VERBOSE_LOG', 'Verbose logging', optional=True, defaultValue=False))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(38, model_feedback)
        results = {}
        outputs = {}

        # Perform layer reprojections
        alg_params = {
        }
        outputs['PerformLayerReprojections'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Reproject Hazard layer 2
        alg_params = {
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': parameters['hazardlayer2'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,
            'SOURCE_CRS': None,
            'TARGET_CRS': 'ProjectCrs',
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectHazardLayer2'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Raster reclassification
        alg_params = {
        }
        outputs['RasterReclassification'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Reproject Hazard layer 1
        alg_params = {
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': parameters['hazardlayers'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,
            'SOURCE_CRS': None,
            'TARGET_CRS': 'ProjectCrs',
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectHazardLayer1'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Raster reclassification 4
        alg_params = {
            'BAND_A': 1,
            'BAND_B': None,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '--NoDataValue=0',
            'FORMULA': '(A-amin(A))/(amax(A)-amin(A))',
            'INPUT_A': parameters['hazardlayer4optional'],
            'INPUT_B': None,
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterReclassification4'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Reproject Hazard layer 5
        alg_params = {
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': parameters['hazardlayer5optional'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,
            'SOURCE_CRS': None,
            'TARGET_CRS': 'ProjectCrs',
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectHazardLayer5'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Raster reclassification 6
        alg_params = {
            'BAND_A': 1,
            'BAND_B': None,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '--NoDataValue=0',
            'FORMULA': '(A-amin(A))/(amax(A)-amin(A))',
            'INPUT_A': parameters['Hazardlayer6optional'],
            'INPUT_B': None,
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterReclassification6'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Raster reclassification 1
        alg_params = {
            'BAND_A': 1,
            'BAND_B': None,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '--NoDataValue=0',
            'FORMULA': '(A-amin(A))/(amax(A)-amin(A))',
            'INPUT_A': parameters['hazardlayers'],
            'INPUT_B': None,
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterReclassification1'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Reproject Exposure Sites layer
        alg_params = {
            'INPUT': parameters['schoollocations'],
            'OPERATION': '',
            'TARGET_CRS': 'ProjectCrs',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectExposureSitesLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Raster reclassification 5
        alg_params = {
            'BAND_A': 1,
            'BAND_B': None,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '--NoDataValue=0',
            'FORMULA': '(A-amin(A))/(amax(A)-amin(A))',
            'INPUT_A': outputs['ReprojectHazardLayer5']['OUTPUT'],
            'INPUT_B': None,
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterReclassification5'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Raster reclassification 1
        alg_params = {
            'BAND_A': 1,
            'BAND_B': None,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '--NoDataValue=0',
            'FORMULA': '(A-amin(A))/(amax(A)-amin(A))',
            'INPUT_A': outputs['ReprojectHazardLayer1']['OUTPUT'],
            'INPUT_B': None,
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterReclassification1'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Raster reclassification 2
        alg_params = {
            'BAND_A': 1,
            'BAND_B': None,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '--NoDataValue=0',
            'FORMULA': '(A-amin(A))/(amax(A)-amin(A))',
            'INPUT_A': parameters['hazardlayer2'],
            'INPUT_B': None,
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterReclassification2'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Raster reclassification
        alg_params = {
        }
        outputs['RasterReclassification'] = processing.run('native:condition', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Fix geometries
        alg_params = {
            'INPUT': parameters['Sitearea'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FixGeometries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Raster reclassification 3
        alg_params = {
            'BAND_A': 1,
            'BAND_B': None,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '--NoDataValue=0',
            'FORMULA': '(A-amin(A))/(amax(A)-amin(A))',
            'INPUT_A': parameters['hazardlayer3'],
            'INPUT_B': None,
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterReclassification3'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Raster reclassification 5
        alg_params = {
            'BAND_A': 1,
            'BAND_B': None,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '--NoDataValue=0',
            'FORMULA': '(A-amin(A))/(amax(A)-amin(A))',
            'INPUT_A': parameters['hazardlayer5optional'],
            'INPUT_B': None,
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterReclassification5'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Combining hazard to calculate average risk
        alg_params = {
            '-n': False,
            'GRASS_RASTER_FORMAT_META': '',
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_REGION_CELLSIZE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'input': [parameters['hazardlayer2'],parameters['hazardlayer3'],parameters['hazardlayer4optional'],parameters['hazardlayer5optional'],parameters['hazardlayers'],parameters['Hazardlayer6optional']],
            'method': [0],
            'quantile': '',
            'range': [nan,nan],
            'weights': '',
            'output': parameters['HazardIndexWithoutPerformingLayerReprojectionsNorReclassifications']
        }
        outputs['CombiningHazardToCalculateAverageRisk'] = processing.run('grass7:r.series', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['HazardIndexWithoutPerformingLayerReprojectionsNorReclassifications'] = outputs['CombiningHazardToCalculateAverageRisk']['output']

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Reproject Hazard layer 3
        alg_params = {
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': parameters['hazardlayer3'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,
            'SOURCE_CRS': None,
            'TARGET_CRS': 'ProjectCrs',
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectHazardLayer3'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Reproject Hazard layer 4
        alg_params = {
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': parameters['hazardlayer4optional'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,
            'SOURCE_CRS': None,
            'TARGET_CRS': 'ProjectCrs',
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectHazardLayer4'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Reproject Hazard layer 6
        alg_params = {
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': parameters['Hazardlayer6optional'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,
            'SOURCE_CRS': None,
            'TARGET_CRS': 'ProjectCrs',
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectHazardLayer6'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Raster reclassification 2
        alg_params = {
            'BAND_A': 1,
            'BAND_B': None,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '--NoDataValue=0',
            'FORMULA': '(A-amin(A))/(amax(A)-amin(A))',
            'INPUT_A': outputs['ReprojectHazardLayer2']['OUTPUT'],
            'INPUT_B': None,
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterReclassification2'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Clip
        alg_params = {
            'INPUT': parameters['schoollocations'],
            'OVERLAY': outputs['FixGeometries']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Clip points with polygons
        alg_params = {
            'FIELD': '0',
            'METHOD': 0,
            'POINTS': parameters['schoollocations'],
            'POLYGONS': outputs['FixGeometries']['OUTPUT'],
            'CLIPS': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ClipPointsWithPolygons'] = processing.run('saga:clippointswithpolygons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Combining hazard to calculate average risk
        alg_params = {
            '-n': False,
            'GRASS_RASTER_FORMAT_META': '',
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_REGION_CELLSIZE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'input': [outputs['ReprojectHazardLayer1']['OUTPUT'],outputs['ReprojectHazardLayer2']['OUTPUT'],outputs['ReprojectHazardLayer3']['OUTPUT'],outputs['ReprojectHazardLayer4']['OUTPUT'],outputs['ReprojectHazardLayer5']['OUTPUT'],outputs['ReprojectHazardLayer6']['OUTPUT']],
            'method': [0],
            'quantile': '',
            'range': [nan,nan],
            'weights': '',
            'output': parameters['HazardIndexPerformingLayerReprojectionsWithNoReclassifications']
        }
        outputs['CombiningHazardToCalculateAverageRisk'] = processing.run('grass7:r.series', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['HazardIndexPerformingLayerReprojectionsWithNoReclassifications'] = outputs['CombiningHazardToCalculateAverageRisk']['output']

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Raster reclassification 6
        alg_params = {
            'BAND_A': 1,
            'BAND_B': None,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '--NoDataValue=0',
            'FORMULA': '(A-amin(A))/(amax(A)-amin(A))',
            'INPUT_A': outputs['ReprojectHazardLayer6']['OUTPUT'],
            'INPUT_B': None,
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterReclassification6'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Raster reclassification 3
        alg_params = {
            'BAND_A': 1,
            'BAND_B': None,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '--NoDataValue=0',
            'FORMULA': '(A-amin(A))/(amax(A)-amin(A))',
            'INPUT_A': outputs['ReprojectHazardLayer3']['OUTPUT'],
            'INPUT_B': None,
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterReclassification3'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Reproject Site area layer
        alg_params = {
            'INPUT': outputs['FixGeometries']['OUTPUT'],
            'OPERATION': '',
            'TARGET_CRS': 'ProjectCrs',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ReprojectSiteAreaLayer'] = processing.run('native:reprojectlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Clip points with polygons
        alg_params = {
            'FIELD': '0',
            'METHOD': 0,
            'POINTS': outputs['ReprojectExposureSitesLayer']['OUTPUT'],
            'POLYGONS': outputs['ReprojectSiteAreaLayer']['OUTPUT'],
            'CLIPS': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ClipPointsWithPolygons'] = processing.run('saga:clippointswithpolygons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # Combining hazard to calculate average risk1
        alg_params = {
            '-n': False,
            'GRASS_RASTER_FORMAT_META': '',
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_REGION_CELLSIZE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'input': [outputs['RasterReclassification1']['OUTPUT'],outputs['RasterReclassification2']['OUTPUT'],outputs['RasterReclassification3']['OUTPUT'],outputs['RasterReclassification5']['OUTPUT'],outputs['RasterReclassification4']['OUTPUT'],outputs['RasterReclassification6']['OUTPUT']],
            'method': [0],
            'quantile': '',
            'range': [nan,nan],
            'weights': '',
            'output': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CombiningHazardToCalculateAverageRisk1'] = processing.run('grass7:r.series', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # Clip points with polygons
        alg_params = {
            'FIELD': '0',
            'METHOD': 0,
            'POINTS': parameters['schoollocations'],
            'POLYGONS': outputs['ReprojectSiteAreaLayer']['OUTPUT'],
            'CLIPS': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ClipPointsWithPolygons'] = processing.run('saga:clippointswithpolygons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}

        # Raster reclassification 4
        alg_params = {
            'BAND_A': 1,
            'BAND_B': None,
            'BAND_C': None,
            'BAND_D': None,
            'BAND_E': None,
            'BAND_F': None,
            'EXTRA': '--NoDataValue=0',
            'FORMULA': '(A-amin(A))/(amax(A)-amin(A))',
            'INPUT_A': outputs['ReprojectHazardLayer4']['OUTPUT'],
            'INPUT_B': None,
            'INPUT_C': None,
            'INPUT_D': None,
            'INPUT_E': None,
            'INPUT_F': None,
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RasterReclassification4'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}

        # Sample raster values
        alg_params = {
            'COLUMN_PREFIX': 'Value',
            'INPUT': outputs['Clip']['OUTPUT'],
            'RASTERCOPY': outputs['CombiningHazardToCalculateAverageRisk']['output'],
            'OUTPUT': parameters['SchoolHazardIndex']
        }
        outputs['SampleRasterValues'] = processing.run('native:rastersampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SchoolHazardIndex'] = outputs['SampleRasterValues']['OUTPUT']

        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}

        # Clip raster by mask layer
        alg_params = {
            'ALPHA_BAND': False,
            'CROP_TO_CUTLINE': True,
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': outputs['CombiningHazardToCalculateAverageRisk1']['output'],
            'KEEP_RESOLUTION': False,
            'MASK': outputs['FixGeometries']['OUTPUT'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'SET_RESOLUTION': False,
            'SOURCE_CRS': None,
            'TARGET_CRS': 'ProjectCrs',
            'X_RESOLUTION': None,
            'Y_RESOLUTION': None,
            'OUTPUT': parameters['HazardIndexPerformingReclassificationsWithNoReprojections']
        }
        outputs['ClipRasterByMaskLayer'] = processing.run('gdal:cliprasterbymasklayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['HazardIndexPerformingReclassificationsWithNoReprojections'] = outputs['ClipRasterByMaskLayer']['OUTPUT']

        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}

        # Add raster values to points
        alg_params = {
            'GRIDS': outputs['CombiningHazardToCalculateAverageRisk']['output'],
            'RESAMPLING': 0,
            'SHAPES': outputs['ClipPointsWithPolygons']['CLIPS'],
            'RESULT': parameters['SchoolHazardIndexPerformingLayerReprojectionsWithNoReclassifications']
        }
        outputs['AddRasterValuesToPoints'] = processing.run('saga:addrastervaluestopoints', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SchoolHazardIndexPerformingLayerReprojectionsWithNoReclassifications'] = outputs['AddRasterValuesToPoints']['RESULT']

        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}

        # Combining hazard to calculate average risk
        alg_params = {
            '-n': False,
            'GRASS_RASTER_FORMAT_META': '',
            'GRASS_RASTER_FORMAT_OPT': '',
            'GRASS_REGION_CELLSIZE_PARAMETER': 0,
            'GRASS_REGION_PARAMETER': None,
            'input': [outputs['RasterReclassification6']['OUTPUT'],outputs['RasterReclassification4']['OUTPUT'],outputs['RasterReclassification1']['OUTPUT'],outputs['RasterReclassification5']['OUTPUT'],outputs['RasterReclassification2']['OUTPUT'],outputs['RasterReclassification3']['OUTPUT']],
            'method': [0],
            'quantile': '',
            'range': [nan,nan],
            'weights': '',
            'output': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CombiningHazardToCalculateAverageRisk'] = processing.run('grass7:r.series', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(35)
        if feedback.isCanceled():
            return {}

        # Clip raster by mask layer
        alg_params = {
            'ALPHA_BAND': False,
            'CROP_TO_CUTLINE': True,
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': outputs['CombiningHazardToCalculateAverageRisk']['output'],
            'KEEP_RESOLUTION': False,
            'MASK': outputs['FixGeometries']['OUTPUT'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'SET_RESOLUTION': False,
            'SOURCE_CRS': None,
            'TARGET_CRS': 'ProjectCrs',
            'X_RESOLUTION': None,
            'Y_RESOLUTION': None,
            'OUTPUT': parameters['HazardIndexPerformingLayerReprojectionsAndPerformingReclassifications']
        }
        outputs['ClipRasterByMaskLayer'] = processing.run('gdal:cliprasterbymasklayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['HazardIndexPerformingLayerReprojectionsAndPerformingReclassifications'] = outputs['ClipRasterByMaskLayer']['OUTPUT']

        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}

        # Add raster values to points
        alg_params = {
            'GRIDS': outputs['ClipRasterByMaskLayer']['OUTPUT'],
            'RESAMPLING': 0,
            'SHAPES': outputs['ClipPointsWithPolygons']['CLIPS'],
            'RESULT': parameters['SchoolHazardIndexPerformingReclassificationsWithNoReprojections']
        }
        outputs['AddRasterValuesToPoints'] = processing.run('saga:addrastervaluestopoints', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SchoolHazardIndexPerformingReclassificationsWithNoReprojections'] = outputs['AddRasterValuesToPoints']['RESULT']

        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}

        # Add raster values to points
        alg_params = {
            'GRIDS': outputs['ClipRasterByMaskLayer']['OUTPUT'],
            'RESAMPLING': 0,
            'SHAPES': outputs['ClipPointsWithPolygons']['CLIPS'],
            'RESULT': parameters['SchoolHazardIndexPerformingLayerReprojectionsAndPerformingReclassifications']
        }
        outputs['AddRasterValuesToPoints'] = processing.run('saga:addrastervaluestopoints', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SchoolHazardIndexPerformingLayerReprojectionsAndPerformingReclassifications'] = outputs['AddRasterValuesToPoints']['RESULT']
        return results

    def name(self):
        return 'Natural Hazard Risk for Schools'

    def displayName(self):
        return 'Natural Hazard Risk for Schools'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return NaturalHazardRiskForSchools()
