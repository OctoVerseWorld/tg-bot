from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Form
from models.dto.users.users import UserDTO
from models.utils.choices.otp_type import OTPType
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from src.application.uow.uow import IUnitOfWork
from src.domain.services.auth.session_tokens import SessionAuthService
from src.domain.services.otp.otp import OTPService
from src.utils.exceptions import http_exc
from src.utils.passwords import PasswordsService


class AuthUseCase:
    auth_service = SessionAuthService

    @classmethod
    async def current_user(cls,
                           request: Request,
                           uow: Annotated[IUnitOfWork, Depends(IUnitOfWork)],
                           ) -> UserDTO:
        """Get current user by access token
        :param request:
        :param uow:
        :return:
        :raises: UnauthorizedHTTPException.
        """
        async with uow:
            user = await cls.auth_service.authenticate(uow, request)
            await uow.commit()
        return user

    @classmethod
    async def login(cls,
                    request: Request,
                    uow: Annotated[IUnitOfWork, Depends(IUnitOfWork)],
                    phone: str = Form(...),
                    password: str = Form(...),
                    otp_code: str = Form(...),
                    ) -> Response:
        """Login user
        :param phone:
        :param password:
        :param otp_code:
        :param request:
        :param uow:
        :return:
        :raises: UnauthorizedHTTPException.
        """

        async with uow:
            user = await uow.users.get_one_by_phone(phone)
            if user is None:
                raise http_exc.UnauthorizedHTTPException
            if not await OTPService.is_verified(uow, phone, OTPType.LOGIN, otp_code):
                raise http_exc.UnauthorizedHTTPException
            if not PasswordsService.verify_password(password, user.password.get_secret_value()):
                raise http_exc.UnauthorizedHTTPException
            response = JSONResponse(content={'message': 'ok'})
            await cls.auth_service.on_login_event(uow, request, response, user)
            await uow.commit()
        return response

    @classmethod
    async def logout(cls,
                     request: Request,
                     uow: Annotated[IUnitOfWork, Depends(IUnitOfWork)],
                     ) -> Response:
        """Logout user
        :param request:
        :param uow:
        :return:
        :raises: UnauthorizedHTTPException.
        """
        async with uow:
            user = await cls.auth_service.authenticate(uow, request)
            response = JSONResponse(content={'message': 'ok'})
            await cls.auth_service.on_logout_event(uow, request, response, user)
            await uow.commit()
        return response
