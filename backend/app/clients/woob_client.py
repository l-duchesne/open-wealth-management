import logging

from woob.core import Woob
from woob.tools.backend import Module
from woob.capabilities.bank import Account,Investment
LOG = logging.getLogger(__name__)


def connect_to_account() -> Module:
    w = Woob()
    module = w.build_backend('fortuneo', params={
        'login': '*****',
        'password': '*****',
    }, name="fortuneo")

    return module


def get_accounts() :
    module = connect_to_account()
    accounts = list(module.iter_accounts())
    return module, accounts


