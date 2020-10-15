from airflow.plugins_manager import AirflowPlugin
from flask_admin.base import MenuLink
from prophet.views.prophet_view import DagStatsView, prophet_blueprint

dag_stats_view = DagStatsView(
    category='Prophet',
    name='DagStats',
    endpoint='dag_stats'
)


class ProphetPlugin(AirflowPlugin):
    """
    The prophet plugin used to expose all the admin tools.
    """
    name = "ProphetAirflowPlugin"
    flask_blueprints = [prophet_blueprint]
    admin_views = [dag_stats_view]

