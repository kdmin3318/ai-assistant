"""Google OAuth 2.0 인증 - 토큰 저장/갱신."""

import json
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_google_credentials(
    credentials_path: Path,
    token_path: Path,
) -> Credentials:
    """Google OAuth 2.0 자격증명을 가져온다.

    토큰 파일이 있으면 로드하고, 만료되었으면 갱신한다.
    없으면 OAuth 플로우를 실행하여 새 토큰을 획득한다.
    """
    creds = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                raise FileNotFoundError(
                    f"Google credentials 파일을 찾을 수 없습니다: {credentials_path}\n"
                    "Google Cloud Console에서 OAuth 2.0 클라이언트 ID를 생성하고 "
                    "credentials.json을 프로젝트 루트에 배치하세요."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # 토큰 저장
        token_path.write_text(creds.to_json())

    return creds
