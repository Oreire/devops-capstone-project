"""
Account Service

This microservice handles the lifecycle of Accounts
"""
# pylint: disable=unused-import
from flask import jsonify, request, make_response, abort, url_for   # noqa: F401
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application
from service.models import db
from flask_api import status

def test_account_not_found(self):
    """It should return 404 when Account is not found"""
    resp = self.client.get("/accounts/0")  # ID 0 is assumed not to exist
    self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)



from service.common.cli_commands import db_create
app.cli.add_command(db_create)


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
        ),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based on the data in the posted body
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    location_url = url_for("get_account", account_id=account.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
# READ AN ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["GET"], endpoint="get_account")
def get_account(account_id):
    """
    Reads an Account

    This endpoint retrieves an Account based on the account_id provided.
    If the Account does not exist, it returns a 404 error.
    """
    app.logger.info("Request to read an Account with id: %s", account_id)

    account = Account.find(account_id)
    if not account:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Account with id [{account_id}] could not be found."
        )

    return account.serialize(), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################

# ... place your code here to UPDATE an account ...


######################################################################
# DELETE AN ACCOUNT
######################################################################

# ... place your code here to DELETE an account ...


######################################################################
# FLASK CLI COMMANDS
######################################################################


@app.cli.command("db-create")


@app.cli.command("db-create")
def db_create():
    """Creates the database tables"""
    app.logger.info("Initializing database")
    db.create_all()
    print("Database created")


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )

