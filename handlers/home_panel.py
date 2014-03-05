from handler import Handler
from handler import cookie_validation
from models import Company
from models import Invoice

from lib.decorators import user_required

import logging

class HomePanelHandler(Handler):
    @user_required
    def get(self):
        self.render("/views/home-panel.html")