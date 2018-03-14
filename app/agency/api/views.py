from flask import jsonify
from flask_login import current_user, login_required

from app.agency.api import agency_api_blueprint
from app.models import Agencies


@agency_api_blueprint.route('/active_users/<string:agency_ein>', methods=['GET'])
@login_required
def get_active_users(agency_ein):
    """

    :param agency_ein:
    :return:
    """
    if current_user.is_agency_admin(agency_ein):
        active_users = sorted(
            [(user.guid, user.name)
             for user in Agencies.query.filter_by(ein=agency_ein).one().active_users],
            key=lambda x: x[1])
        active_users.insert(0, ('', 'All'))
        return jsonify({"active_users": active_users, "is_admin": True}), 200

    elif current_user.is_agency_active(agency_ein):
        active_users = [
            ('', 'All'),
            (current_user.guid, 'My Requests')
        ]
        return jsonify({"active_users": active_users, "is_admin": False}), 200

    else:
        return jsonify({}), 404