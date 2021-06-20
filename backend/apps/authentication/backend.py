import jwt

from django.conf import settings
from rest_framework import authentication, exceptions

from .models.users import User
from .models.logout_token import LogoutToken
import logging

logger = logging.getLogger(__name__)


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()
        if not auth_header:
            return None
        if len(auth_header) == 1:
            return None
        elif len(auth_header) > 2:
            return None
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')
        if prefix.lower() != auth_header_prefix:
            return None
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        This method is need to update
        If you want to save the token in here
        """
        try:
            token_invalid = LogoutToken.objects.filter(token=token)
            if len(token_invalid) > 0:
                raise exceptions.AuthenticationFailed('This token is logout from our system')
            payload = jwt.decode(token, settings.SECRET_KEY)
        except Exception as ex:
            msg = 'Invalid authentication. Could not decode token.'
            logger.error(' Authentication Error: ' + msg)
            raise exceptions.AuthenticationFailed(msg)
        try:
            user = User.objects.get(email=payload['email'], password=payload['password'], )
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            logger.error(' Authentication Error: ' + msg)
            raise exceptions.AuthenticationFailed(msg)
        if not user.is_active:
            msg = 'This user has been deactivated.'
            logger.error(' Authentication Error: ' + msg)
            raise exceptions.AuthenticationFailed(msg) 
            
        if user.is_staff == True:
            if user.staff_user_id.count() > 0:
                staff_info = user.staff_user_id.first()
                if staff_info.admin_locked:
                    msg = 'This user has been administrative locked by admin.'
                    logger.error(' Authentication Error: ' + msg)
                    raise exceptions.AuthenticationFailed(msg)
                if staff_info.password_locked:
                    msg = 'This user has been locked for multiple password failed attempt.'
                    logger.error(' Authentication Error: ' + msg)
                    raise exceptions.AuthenticationFailed(msg)
            else:
                msg = 'This user has no staff information. Please contact with system administrative.'
                logger.error(' Authentication Error: ' + msg)
                raise exceptions.AuthenticationFailed(msg)

        return (user, token)
