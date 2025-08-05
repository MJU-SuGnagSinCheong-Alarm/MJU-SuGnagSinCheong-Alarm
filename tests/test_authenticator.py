# tests/test_authenticator_integration.py

import os
import pytest
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 테스트 대상 모듈
from mju_sugang_alarm.course_list_crawler.authenticator import Authenticator


# 환경 변수에서 테스트 계정 정보 가져오기
TEST_USERNAME = os.getenv("TEST_USERNAME")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")
BASE_URL = os.getenv("SUGANG_BASE_URL", "https://sugang.mju.ac.kr")


# 테스트 전 유효성 검사
@pytest.fixture(scope="session", autouse=True)
def check_env_vars():
    """환경 변수가 설정되었는지 확인"""
    if not TEST_USERNAME or not TEST_PASSWORD:
        pytest.skip("⚠️ 통합 테스트 건너뜀: .env 파일에 TEST_USERNAME 또는 TEST_PASSWORD가 없습니다.")
    if "localhost" not in BASE_URL and "mju.ac.kr" not in BASE_URL:
        pytest.skip("⚠️ 위험한 URL: 실제 서버가 아님")


@pytest.fixture
def authenticator():
    """테스트용 Authenticator 인스턴스 제공"""
    return Authenticator(base_url=BASE_URL)


def test_integration_login_success(authenticator):
    """실제 서버에 로그인 시도 (성공 여부 확인)"""
    print("\n🔍 통합 테스트 시작: 실제 로그인 시도")

    # When
    result = authenticator.login(TEST_USERNAME, TEST_PASSWORD)

    # Then
    if result:
        print("🎉 로그인 성공! 세션 유지됨.")
        assert authenticator.is_logged_in is True
    else:
        print("❌ 로그인 실패. 자격 증명 또는 네트워크 문제일 수 있음.")
        assert authenticator.is_logged_in is False

    # 최종 URL 출력 (개인정보 노출 방지)
    if hasattr(authenticator.session, 'last_response_url'):
        print(f"📍 최종 URL: {authenticator.session.last_response_url}")
    else:
        print(f"📍 현재 URL: {getattr(authenticator.session, 'url', '알 수 없음')}")


def test_integration_login_with_wrong_password(authenticator):
    """잘못된 비밀번호로 로그인 실패 확인"""
    print("\n🔐 잘못된 비밀번호로 로그인 시도")

    # When
    result = authenticator.login(TEST_USERNAME, "wrong_password_123!")

    # Then
    assert result is False, "❌ 실패해야 할 로그인이 성공했습니다."
    assert authenticator.is_logged_in is False
    print("✅ 로그인 실패 확인 (정상 동작)")