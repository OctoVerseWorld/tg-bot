import datetime

from models.dto.users.users import UserDTO
from starlette.requests import Request

from src.application.uow.uow import IUnitOfWork
from src.config.session_tokens import session_token_settings
from src.domain.services.auth.session_tokens import SessionAuthService, SessionService
from src.utils.datetime.datetime import get_current_utc_datetime
from src.utils.exceptions import http_exc


class SessionTokenUseCase:
    @classmethod
    async def deactivate_session(cls,
                                 uow: IUnitOfWork,
                                 request: Request,
                                 current_user: UserDTO,
                                 session_token: str) -> None:
        """Deactivate session
        :param request:
        :param uow:
        :param current_user:
        :param session_token:
        :return:
        """
        async with uow:
            session_for_delete = await SessionService.get_session_by_token(uow, session_token)
            if session_for_delete.user_id != current_user.id:
                raise http_exc.ForbiddenHTTPException()

            current_session = await SessionService.get_session_by_token(
                uow,
                request.cookies.get(SessionAuthService.cookie_name)
            )

            if current_session.login_at > get_current_utc_datetime(
                    sub=datetime.timedelta(hours=session_token_settings.CAN_KILL_OTHER)):
                raise http_exc.ForbiddenHTTPException("You can't delete current session. "
                                                      "Because ur session is too young.")

            await SessionService.deactivate_session(uow, session_token)
            await uow.commit()
