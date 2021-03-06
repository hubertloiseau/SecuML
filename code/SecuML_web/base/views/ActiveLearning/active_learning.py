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

from flask import render_template, send_file, jsonify

from SecuML_web.base import app, db, cursor

from SecuML.Experiment.ActiveLearningExperiment import ActiveLearningExperiment
from SecuML.Experiment import ExperimentFactory
from SecuML.Tools import dir_tools

@app.route('/sublabels/<project>/<dataset>/<experiment_id>/<iteration>/')
def sublabels(project, dataset, experiment_id, iteration):
    return render_template('ActiveLearning/sublabels.html')

@app.route('/getSublabelsBarplot/<project>/<dataset>/<experiment_id>/<iteration>/<label>/')
def getSublabelsBarplot(project, dataset, experiment_id, iteration, label):
    experiment = ExperimentFactory.getFactory().fromJson(project, dataset, experiment_id,
            db, cursor)
    filename  = dir_tools.getExperimentOutputDirectory(experiment) + str(iteration) + '/'
    filename += 'sublabels_monitoring/' + label + '_sublabels_monitoring.json'
    return send_file(filename)

@app.route('/getNumIterations/<project>/<dataset>/<experiment_id>/')
def getNumIterations(project, dataset, experiment_id):
    experiment = ExperimentFactory.getFactory().fromJson(project, dataset, experiment_id,
            db, cursor)
    dir_path = dir_tools.getExperimentOutputDirectory(experiment)
    filename = dir_path + 'labels_monitoring.csv'
    return str(dir_tools.countLines(filename) - 1)

@app.route('/getActiveLearningValidationConf/<project>/<dataset>/<experiment_id>/')
def getActiveLearningValidationConf(project, dataset, experiment_id):
    experiment = ExperimentFactory.getFactory().fromJson(project, dataset, experiment_id,
            db, cursor)
    return jsonify(experiment.validation_conf.toJson())
