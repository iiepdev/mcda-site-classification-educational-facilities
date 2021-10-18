"""
Model exported as python.
Name : Natural Hazard Risks for Schools
Group : Final models
With QGIS : 32003
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsExpression
import processing


class NaturalHazardRisksForSchools(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterNumber('Numberofriskstocompute', 'Number of risks to compute', type=QgsProcessingParameterNumber.Integer, minValue=2, maxValue=6, defaultValue=6))
        self.addParameter(QgsProcessingParameterRasterLayer('Hazardlayer1', 'Hazard layer 1', defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('WeightforHazardlayer1', 'Weight for Hazard layer 1', type=QgsProcessingParameterNumber.Double, minValue=0, maxValue=1, defaultValue=1))
        self.addParameter(QgsProcessingParameterRasterLayer('Hazardlayer2', 'Hazard layer 2', defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('WeightforHazardlayer2', 'Weight for Hazard layer 2', type=QgsProcessingParameterNumber.Double, minValue=0, maxValue=1, defaultValue=1))
        self.addParameter(QgsProcessingParameterRasterLayer('Hazardlayer3', 'Hazard layer 3', optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('WeightforHazardlayer3', 'Weight for Hazard layer 3', optional=True, type=QgsProcessingParameterNumber.Double, minValue=0, maxValue=1, defaultValue=1))
        self.addParameter(QgsProcessingParameterRasterLayer('Hazardlayer4', 'Hazard layer 4', optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('WeightforHazardlayer4', 'Weight for Hazard layer 4', optional=True, type=QgsProcessingParameterNumber.Double, minValue=0, maxValue=1, defaultValue=1))
        self.addParameter(QgsProcessingParameterRasterLayer('Hazardlayer5', 'Hazard layer 5', optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('WeightforHazardlayer5', 'Weight for Hazard layer 5', optional=True, type=QgsProcessingParameterNumber.Double, minValue=0, maxValue=1, defaultValue=1))
        self.addParameter(QgsProcessingParameterRasterLayer('Hazardlayer6', 'Hazard layer 6', optional=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterNumber('WeightforHazardlayer6', 'Weight for Hazard layer 6', optional=True, type=QgsProcessingParameterNumber.Double, minValue=0, maxValue=1, defaultValue=1))
        self.addParameter(QgsProcessingParameterVectorLayer('Schools', 'Schools', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('Studyarea', 'Study area', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('HazardIndex', 'Hazard Index', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('HazardIndexSchools', 'Hazard Index - Schools', type=QgsProcessing.TypeVectorPoint, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}

        # Clip
        alg_params = {
            'INPUT': parameters['Schools'],
            'OVERLAY': parameters['Studyarea'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Clip'] = processing.run('native:clip', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Merge
        alg_params = {
            'DATA_TYPE': 5,  # Float32
            'EXTRA': '',
            'INPUT': QgsExpression('CASE\r\nWHEN  @Numberofriskstocompute =2 THEN array( @Hazardlayer1 , @Hazardlayer2 ) \r\nWHEN  @Numberofriskstocompute =3 THEN array(  @Hazardlayer1 , @Hazardlayer2 , @Hazardlayer3 ) \r\nWHEN  @Numberofriskstocompute =4 THEN array(  @Hazardlayer1 , @Hazardlayer2 , @Hazardlayer3 , @Hazardlayer4  ) \r\nWHEN  @Numberofriskstocompute =5 THEN array( @Hazardlayer1 , @Hazardlayer2 , @Hazardlayer3 , @Hazardlayer4 , @Hazardlayer5  ) \r\nWHEN  @Numberofriskstocompute =6 THEN array(  @Hazardlayer1 , @Hazardlayer2 , @Hazardlayer3 , @Hazardlayer4 , @Hazardlayer5 , @Hazardlayer6 ) \r\nEND').evaluate(),
            'NODATA_INPUT': None,
            'NODATA_OUTPUT': None,
            'OPTIONS': '',
            'PCT': False,
            'SEPARATE': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Merge'] = processing.run('gdal:merge', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Raster calculator
        alg_params = {
            'BAND_A': 1,
            'BAND_B': 2,
            'BAND_C': QgsExpression('CASE\r\nWHEN @Numberofriskstocompute =3 OR @Numberofriskstocompute =4 OR @Numberofriskstocompute =5 OR  @Numberofriskstocompute =6 THEN 3\r\nEND').evaluate(),
            'BAND_D': QgsExpression('CASE\r\nWHEN  @Numberofriskstocompute =4 OR @Numberofriskstocompute =5 OR  @Numberofriskstocompute =6 THEN 4\nEND').evaluate(),
            'BAND_E': QgsExpression('CASE\r\nWHEN @Numberofriskstocompute =5 OR  @Numberofriskstocompute =6 THEN 5\nEND').evaluate(),
            'BAND_F': QgsExpression('CASE\r\nWHEN @Numberofriskstocompute =6 THEN 6\r\nEND').evaluate(),
            'EXTRA': '',
            'FORMULA': QgsExpression('CASE\r\nWHEN  @Numberofriskstocompute =2 THEN concat(\'A*\',to_string( @WeightforHazardlayer1),\'+B*\',to_string( @WeightforHazardlayer2))\r\nWHEN  @Numberofriskstocompute =3 THEN concat(\'A*\',to_string( @WeightforHazardlayer1),\'+B*\',to_string( @WeightforHazardlayer2), \'+C*\',to_string( @WeightforHazardlayer3))\r\nWHEN  @Numberofriskstocompute =4 THEN concat(\'A*\',to_string( @WeightforHazardlayer1),\'+B*\',to_string( @WeightforHazardlayer2), \'+C*\',to_string( @WeightforHazardlayer3), \'+D*\',to_string( @WeightforHazardlayer4))\r\nWHEN  @Numberofriskstocompute =5 THEN concat(\'A*\',to_string( @WeightforHazardlayer1),\'+B*\',to_string( @WeightforHazardlayer2), \'+C*\',to_string( @WeightforHazardlayer3), \'+D*\',to_string( @WeightforHazardlayer4), \'+E*\',to_string( @WeightforHazardlayer5))\r\nWHEN  @Numberofriskstocompute =6 THEN concat(\'A*\',to_string( @WeightforHazardlayer1),\'+B*\',to_string( @WeightforHazardlayer2), \'+C*\',to_string( @WeightforHazardlayer3), \'+D*\',to_string( @WeightforHazardlayer4), \'+E*\',to_string( @WeightforHazardlayer5), \'+F*\',to_string( @WeightforHazardlayer6 ))\r\nEND').evaluate(),
            'INPUT_A': outputs['Merge']['OUTPUT'],
            'INPUT_B': outputs['Merge']['OUTPUT'],
            'INPUT_C': QgsExpression('CASE\r\nWHEN @Numberofriskstocompute =3 OR @Numberofriskstocompute =4 OR @Numberofriskstocompute =5 OR  @Numberofriskstocompute =6 THEN @Merge_OUTPUT \r\nEND').evaluate(),
            'INPUT_D': QgsExpression('CASE\r\nWHEN  @Numberofriskstocompute =4 OR @Numberofriskstocompute =5 OR  @Numberofriskstocompute =6 THEN @Merge_OUTPUT \r\nEND').evaluate(),
            'INPUT_E': QgsExpression('CASE\r\nWHEN  @Numberofriskstocompute =5 OR  @Numberofriskstocompute =6 THEN @Merge_OUTPUT \r\nEND').evaluate(),
            'INPUT_F': QgsExpression('CASE\r\nWHEN  @Numberofriskstocompute = 6 THEN @Merge_OUTPUT \r\nEND').evaluate(),
            'NO_DATA': None,
            'OPTIONS': '',
            'RTYPE': 5,  # Float32
            'OUTPUT': parameters['HazardIndex']
        }
        outputs['RasterCalculator'] = processing.run('gdal:rastercalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['HazardIndex'] = outputs['RasterCalculator']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Sample raster values
        alg_params = {
            'COLUMN_PREFIX': 'HazardIndex',
            'INPUT': outputs['Clip']['OUTPUT'],
            'RASTERCOPY': outputs['RasterCalculator']['OUTPUT'],
            'OUTPUT': parameters['HazardIndexSchools']
        }
        outputs['SampleRasterValues'] = processing.run('native:rastersampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['HazardIndexSchools'] = outputs['SampleRasterValues']['OUTPUT']
        return results

    def name(self):
        return 'Natural Hazard Risks for Schools'

    def displayName(self):
        return 'Natural Hazard Risks for Schools'

    def group(self):
        return 'Final models'

    def groupId(self):
        return 'Final models'

    def createInstance(self):
        return NaturalHazardRisksForSchools()
