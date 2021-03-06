## SecuML
## Copyright (C) 2016  ANSSI
##
## SecuML is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## SecuML is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License along
## with SecuML. If not, see <http://www.gnu.org/licenses/>.

import abc

from SecuML.SupervisedLearning.Configuration import SupervisedLearningConfFactory
from SecuML.SupervisedLearning.Configuration.TestConfiguration import TestConfiguration

class LearningParameter(object):

    def __init__(self, values):
        self.values = values
        self.best_value = None

    def setBestValue(self, best_value):
        self.best_value = best_value

    @staticmethod
    def fromJson(obj):
        conf = LearningParameter(obj['values'])
        conf.setBestValue(obj['best_value'])
        return conf

    def toJson(self):
        conf = {}
        conf['__type__'] = 'LearningParameter'
        conf['values'] = self.values
        conf['best_value'] = self.best_value
        return conf

class SupervisedLearningConfiguration(object):

    def __init__(self, num_folds, sample_weight, alerts_conf = None):
        self.num_folds = num_folds
        self.sample_weight = sample_weight
        self.model_class = None
        self.test_conf = TestConfiguration(
                alerts_conf = alerts_conf)

    def setTestDataset(self, test_dataset, exp):
        self.test_conf.setTestDataset(test_dataset, exp)

    def setRandomSplit(self, test_size):
        self.test_conf.setRandomSplit(test_size)

    def setUnlabeled(self, labels_annotations = 'labels'):
        self.test_conf.setUnlabeled(labels_annotations)

    def generateSuffix(self):
        suffix  = '__' + self.getModelClassName()
        if self.sample_weight:
            suffix += '__' + 'SampleWeight'
        suffix += self.test_conf.generateSuffix()
        return suffix

    @abc.abstractmethod
    def getModelClassName(self):
        return

    @abc.abstractmethod
    def getParamGrid(self):
        return

    @abc.abstractmethod
    def setBestValues(self, grid_search):
        return

    @abc.abstractmethod
    def getBestValues(self):
        return

    @staticmethod
    def setTestConfiguration(conf, obj, exp):
        conf.test_conf = TestConfiguration.fromJson(obj['test_conf'], exp)

    @staticmethod
    def fromJson(obj, exp):
        conf = SupervisedLearningConfiguration(obj['num_folds'], obj['sample_weight'])
        SupervisedLearningConfiguration.setTestConfiguration(conf, obj, exp)
        return conf

    def toJson(self):
        conf = {}
        conf['__type__'] = 'SupervisedLearningConfiguration'
        conf['num_folds'] = self.num_folds
        conf['sample_weight'] = self.sample_weight
        conf['test_conf'] = self.test_conf.toJson()
        return conf

SupervisedLearningConfFactory.getFactory().registerClass('SupervisedLearningConfiguration',
        SupervisedLearningConfiguration)
