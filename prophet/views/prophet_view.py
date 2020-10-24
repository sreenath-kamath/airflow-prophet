from airflow.utils.db import provide_session
from flask import (
    Blueprint, redirect, request, Markup, Response, render_template,
    make_response, flash, jsonify, url_for)
from flask_admin import BaseView, expose
from airflow.models import DagBag, DagRun, DagModel
from flask_wtf import FlaskForm
from wtforms import SelectField

from statistics import mean

prophet_blueprint = Blueprint(
    "prophet", __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/self_service"
)

class DagChoiceForm(FlaskForm):
    dag_id = SelectField('Dags')
    num_runs = SelectField('NumRuns')


class DagStatsView(BaseView):
    """
    A view that exposes basic stats around a dag.
    """

    @expose("/")
    @provide_session
    def dag_stats(self, session=None):
        selected_dag_id = request.args.get('dag_id')

        DG = DagModel
        dags = session \
                .query(DG) \
                .all()

        dags = [dag.dag_id for dag in dags]

        # Form options
        form = DagChoiceForm()
        form.dag_id.choices = dags
        num_runs = [1, 7, 15, 30]
        form.num_runs.choices = num_runs

        dag_runs = []
        average_duration = 0
        #Fetching the dag stats if the dag_id is not none
        if selected_dag_id is not None:
            DR = DagRun
            dag_runs = session\
                .query(DR)\
                .filter(DR.dag_id == selected_dag_id)

            durations = []
            for dag_run in dag_runs:
                if dag_run.state != 'running':
                    durations.append(
                        (dag_run.end_date - dag_run.start_date).seconds
                    )
            if len(durations) > 0:
                average_duration = mean(durations)

        return self.render("main.html",
                           form=form,
                           selected_dag_id=selected_dag_id,
                           dag_runs=dag_runs,
                           average_duration=average_duration)
