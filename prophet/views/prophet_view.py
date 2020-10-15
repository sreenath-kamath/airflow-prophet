from flask import Blueprint
from flask_admin import BaseView, expose
from airflow.models import DagBag


prophet_blueprint = Blueprint(
    "prophet", __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/self_service"
)


class DagStatsView(BaseView):
    """
    A view that exposes basic stats around a dag.
    """

    @expose("/")
    def dag_stats(self):
        return self.render("main.html", dags=DagBag().dags.keys())