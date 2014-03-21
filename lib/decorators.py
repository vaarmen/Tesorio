# standard library imports
import logging
# related third party imports
from google.appengine.api import users
# local application/library specific imports
from config import config

def user_required(handler):
  """
    Decorator that checks if there's a user associated with the current session.
    Will also fail if there's no session present.
  """
  def check_login(self, *args, **kwargs):
    auth = self.auth
    if not auth.get_user_by_session():
      self.redirect('/login', abort=True)
    else:
      return handler(self, *args, **kwargs)

  return check_login


def admin_required(handler):
    """
         Decorator for checking if there's a admin user associated
         with the current session.
         Will also fail if there's no session present.
    """

    def check_admin(self, *args, **kwargs):
        """
            If handler has no login_url specified invoke a 403 error
        """
        if not users.is_current_user_admin() and config.get('environment') == "production":
            self.response.write(
                '<div style="padding-top: 200px; height:178px; width: 500px; color: white; margin: 0 auto; font-size: 52px; text-align: center; background: url(\'http://3.bp.blogspot.com/_d_q1e2dFExM/TNWbWrJJ7xI/AAAAAAAAAjU/JnjBiTSA1xg/s1600/Bank+Vault.jpg\')">Forbidden Access <a style=\'color: white;\' href=\'%s\'>Login</a></div>' %
                users.create_login_url(self.request.path_url + self.request.query_string))
            return
        else:
            return handler(self, *args, **kwargs)

    return check_admin