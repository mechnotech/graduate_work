from flask import Blueprint

from utils.tools import get_redirecting

links = Blueprint('links', __name__)


@links.route('get_link_list', methods=['GET'])
def get_link_list():
    result = get_redirecting()
    return result
