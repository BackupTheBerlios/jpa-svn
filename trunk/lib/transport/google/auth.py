# -*- coding: UTF-8 -*-

# This file is part of JPA.
# Copyright: (C) 2003 - 2005 Jarek Zgoda <jzgoda@o2.pl>
#
# JPA is free software; you can redistribute it and/or modify it under 
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 2 of the License.
#
# JPA is distributed in the hope that it will be useful, but WITHOUT ANY 
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
# details.
#
# You should have received a copy of the GNU General Public License along with 
# JPA; if not, write to the Free Software Foundation, Inc., 
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""Google API authentication system (aka ProgrammaticLogin, see
http://code.google.com/apis/accounts/AuthForInstalledApps.html"""

__revision__ = '$Id$'

import httplib

from lib.appconst import SOURCE, DEBUG

# service constants
HOST = 'www.google.com'
PATH = '/accounts/ClientLogin'
HEADERS = {
    'Content-type': 'application/x-www-form-urlencoded',
    }
RESPONSE403 = {
    'BadAuthentication': _('Wrong password or unknown user name.'),
    'NotVerified': _('Your account has not been verified. Please, login to your Google account directly to resolve the issue.'),
    'TermsNotAgreed': _('You had not agreed to terms of service. Please, login to your Google account directly to resolve the issue.'),
    'CaptchaRequired': _('Additional authentication required.'),
    'Unknown': _('Unknown or unspecified error.'),
    'AccountDeleted': _('Your account has been deleted.'),
    'AccountDisabled': _('Your account has been disabled.'),
    'ServiceUnavailable': _('Authorization service temporarily unavailable.'),
    }


# service exceptions
class AurhorizationException(Exception):
    """Basic authorization service exception."""
    pass

class GoogleAuthException(AuthorizationException):
    """Basic authorization service exception, continuation is possible."""
    pass

class GoogleAuthError(AuthorizationException):
    """Basic authorization service error, can not continue."""
    pass

class BadAuthenticationError(GoogleAuthError):
    """Wrong password or unknown user name."""
    pass

class NotVerifiedError(GoogleAuthError):
    """Account has not been verified."""
    pass

class TermsNotAgreedError(GoogleAuthError):
    """User dod not agree to TOS."""
    pass

class UnknownError(GoogleAuthError):
    """Unknown or unspecified service error."""
    pass

class AccountDeletedError(GoogleAuthError):
    """User account has been deleted."""
    pass

class AccountDisabledError(GoogleAuthError):
    """User account has been suspended."""
    pass

class ServiceUnavailableError(GoogleAuthError):
    """Authorization service is temporarily unavailable."""
    pass

class CaptchaRequiredException(GoogleAuthException):
    """Service asks additional security measure (CAPTCHA image)."""
    pass


class GoogleAccount:

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def login(self):
        http = httplib.HTTPSConnection(HOST)
