from marshmallow import Schema, fields

from datetime import datetime
from src.api.middleware.auth import auth_cleanup, auth_guard
from src.api.utils.Result import Error, OK, Status
from src.api.utils.dictify import dictify_reservation
from src.branch.BranchService import BranchService
from src.utils.errors import AlreadyExistsError, InputError

guard = auth_guard
cleanup = auth_cleanup


class PostSchema(Schema):
    table_number = fields.Int(required=True)
    num_people = fields.Int(required=True)
    customer_name = fields.String(required=True)
    reservation_timestamp = fields.Int(required=True)


def post(body: dict, branch_id: str):
    table_number = body["table_number"]
    num_people = body["num_people"]
    customer_name = body["customer_name"]
    reservation_timestamp = body["reservation_timestamp"]
    datetime_obj = datetime.fromtimestamp(reservation_timestamp)

    if branch_id is None:
        Error(Status.BAD_REQUEST, "SHOULDNT BE POSSIBLE")

    branch = BranchService.get_by_id(branch_id)
    if branch is None:
        return Error(Status.NOT_FOUND, "Branch not found.")

    table = branch.tables().get_by_number(table_number)
    if table is None:
        return Error(Status.NOT_FOUND, "Table not found")

    try:
        reservation = branch.reservations().create(
            table, customer_name, datetime_obj, num_people)
    except AlreadyExistsError as e:
        return Error(Status.CONFLICT, e.message)
    except InputError as e:
        return Error(Status.BAD_REQUEST, e.message)

    return OK(dictify_reservation(reservation))
