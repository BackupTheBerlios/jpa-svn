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

import urllib
import httplib

# base service exceptions
class AuthorizationException(Exception):
    """Basic authorization service exception."""
    pass


class GoogleAuthException(AuthorizationException):
    """Basic authorization service exception, continuation is possible."""
    pass


class GoogleAuthError(AuthorizationException):
    """Basic authorization service error, can not continue."""
    pass


# implementations of service exceptions
class BadAuthenticationError(GoogleAuthError):
    """Wrong password or unknown user name."""

    def __str__(self):
        return 'Wrong password or unknown user name.'


class NotVerifiedError(GoogleAuthError):
    """Account has not been verified."""

    def __str__(self):
        return ('Your account has not been verified. '
            'Please, login to your Google account directly '
            'to resolve the issue.')


class TermsNotAgreedError(GoogleAuthError):
    """User did not agree to TOS."""

    def __str__(self):
        return ('You had not agreed to terms of service. '
            'Please, login to your Google account directly '
            'to resolve the issue.')


class UnknownError(GoogleAuthError):
    """Unknown or unspecified service error."""

    def __str__(self):
        return 'Unknown or unspecified error.'


class AccountDeletedError(GoogleAuthError):
    """User account has been deleted."""

    def __str__(self):
        return 'Your account has been deleted.'


class AccountDisabledError(GoogleAuthError):
    """User account has been suspended."""

    def __str__(self):
        return 'Your account has been disabled.'


class ServiceUnavailableError(GoogleAuthError):
    """Authorization service is temporarily unavailable."""

    def __str__(self):
        return 'Authorization service temporarily unavailable.'


class CaptchaRequiredException(GoogleAuthException):
    """Service asks additional security measure (CAPTCHA image)."""

    def __str__(self):
        return 'Additional authentication required.'


# service constants
SVC_HOST = 'www.google.com'
SVC_PATH = '/accounts/ClientLogin'
CAPTCHA_PATH = '/accounts/%s'
AUTH_HEADERS = {
    'Content-type': 'application/x-www-form-urlencoded',
}
RESPONSE403 = {
    'BadAuthentication': BadAuthenticationError,
    'NotVerified': NotVerifiedError,
    'TermsNotAgreed': TermsNotAgreedError,
    'CaptchaRequired': CaptchaRequiredException,
    'Unknown': UnknownError,
    'AccountDeleted': AccountDeletedError,
    'AccountDisabled': AccountDisabledError,
    'ServiceUnavailable': ServiceUnavailableError,
}


class GoogleAuth:
    """Class that handles authentication at Google services."""

    def __init__(self, email, password, auth_source='generic/lib', proxy=None):
        """Google authorization service client constructor. Required arguments
        are email and password. If you want to specify your agent name, set it
        in auth_source argument. If you need to use HTTP proxy, pass the proxy
        dictionary with host and port values (as strings)."""
        self.proxy = None
        if proxy:
            self.host = '%s:%d' % (proxy['host'], proxy['port'])
            self.path = 'https://%s%s' % (SVC_HOST, SVC_PATH)
        else:
            self.host = SVC_HOST
            self.path = SVC_PATH
        self.login_params = {
            'Email': email,
            'Passwd': password,
            'service': 'xapi',
            'source': auth_source,
        }

    def login(self, service='xapi', captcha_auth=None):
        """This method tries to login user to Google services. If service
        argument is not provided, generic xapi service code is used.
        Optional captcha_auth argument contains dictionary of captcha token and
        the word from captcha image. It should be used solely for reissuing
        authorization request in case when Google asks for captcha.
        The method will fail on receiving 403 and raise appropriate exception,
        as defined above. Such raised exception will contain the whole server
        response."""
        http = httplib.HTTPSConnection(self.host)
        if service != 'xapi':
            self.login_params['service'] = service
        if captcha_auth is not None:
            self.login_params['logintoken'] = captcha_auth['token']
            self.login_params['logincaptcha'] = captcha_auth['captcha']
        params = urllib.urlencode(self.login_params)
        http.request('POST', self.path, params, AUTH_HEADERS)
        response = http.getresponse()
        raw_body = response.read().strip().split('\n')
        response_body = {}
        for line in raw_body:
            k, v = line.split('=', 1)
            response_body[k] = v
        if response.status == 200:
            try:
                return response_body['Auth']
            except KeyError:
                raise GoogleAuthError, 'Bad response from service'
        elif response.status == 403:
            handler_403 = RESPONSE403[response_body['Error']]
            raise handler_403, response_body

    def get_captcha_image(self, response_body):
        """This method downloads CAPTCHA image from Google authorization
        service and returns it along with authorization token."""
        image_path = CAPTCHA_PATH % response_body['CaptchaUrl']
        if self.proxy:
            host = '%s:%d' % (self.proxy['host'], self.proxy['port'])
            path = 'https://%s%s' % (SVC_HOST, image_path)
        else:
            host = SVC_HOST
            path = image_path
        http = httplib.HTTPSConnection(self.host)
        http.request('GET', path)
        response = http.getresponse()
        if response.status == 200:
            return response_body['CaptchaToken'], response.read()
