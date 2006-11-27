# -*- coding: UTF-8 -*-

# This file is part of JPA.
# Copyright: (C) 2003 - 2006 Jarek Zgoda <jzgoda@o2.pl>
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

"""Google identity (login) implementation using ProgrammaticLogin, based on
http://code.google.com/apis/accounts/AuthForInstalledApps.html"""

__revision__ = '$Id$'

from webclient.identity import AuthorizationException, Identity


# base service exceptions
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


# real user identity at Google
class GoogleIdentity(Identity):
    """User identity at Google services"""

    def authorize(self):
        pass
