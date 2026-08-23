"""Tests for mock database fixtures."""

from __future__ import annotations

import base64
import io
import json
from http import HTTPStatus

import pytest

pytest.importorskip(modname="mock_vws")

import requests
from mock_vws.database import CloudDatabase, VuMarkDatabase
from vws_auth_tools import authorization_header, rfc_1123_date

from vws_test_fixtures.databases import ModelTargetCredentials


def test_mock_cloud_database(*, mock_cloud_database: CloudDatabase) -> None:
    """``mock_cloud_database`` yields a working cloud database."""
    assert mock_cloud_database.server_access_key
    assert mock_cloud_database.server_secret_key
    assert mock_cloud_database.client_access_key
    assert mock_cloud_database.client_secret_key

    request_path = "/summary"
    date = rfc_1123_date()
    auth = authorization_header(
        access_key=mock_cloud_database.server_access_key,
        secret_key=mock_cloud_database.server_secret_key,
        method="GET",
        content=b"",
        content_type="",
        date=date,
        request_path=request_path,
    )
    response = requests.get(
        url="https://vws.vuforia.com" + request_path,
        headers={
            "Authorization": auth,
            "Date": date,
        },
        timeout=30,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["result_code"] == "Success"


def test_mock_vumark_database(
    *,
    mock_vumark_database: VuMarkDatabase,
) -> None:
    """``mock_vumark_database`` yields a database with a template
    target.
    """
    assert mock_vumark_database.server_access_key
    assert mock_vumark_database.server_secret_key
    (target,) = mock_vumark_database.vumark_targets
    assert target.name == "vumark-template"


def test_mock_model_target_credentials(
    *,
    mock_model_target_credentials: ModelTargetCredentials,
) -> None:
    """Model Target credentials work against the active mock."""
    response = requests.post(
        url="https://vws.vuforia.com/oauth2/token",
        auth=(
            mock_model_target_credentials.client_id,
            mock_model_target_credentials.client_secret,
        ),
        data={"grant_type": "client_credentials"},
        timeout=30,
    )
    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json()


def test_bad_image_file_rejected_by_mock(
    *,
    bad_image_file: io.BytesIO,
    mock_cloud_database: CloudDatabase,
) -> None:
    """``bad_image_file`` params are rejected by mock VWS as
    ``BadImage``.
    """
    image_data = bad_image_file.getvalue()

    body = {
        "name": "example_name",
        "width": 1.0,
        "image": base64.b64encode(s=image_data).decode(encoding="ascii"),
        "active_flag": True,
    }
    content = json.dumps(obj=body).encode(encoding="utf-8")
    request_path = "/targets"
    content_type = "application/json"
    date = rfc_1123_date()
    auth = authorization_header(
        access_key=mock_cloud_database.server_access_key,
        secret_key=mock_cloud_database.server_secret_key,
        method="POST",
        content=content,
        content_type=content_type,
        date=date,
        request_path=request_path,
    )
    response = requests.post(
        url="https://vws.vuforia.com" + request_path,
        headers={
            "Authorization": auth,
            "Date": date,
            "Content-Type": content_type,
        },
        data=content,
        timeout=30,
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["result_code"] == "BadImage"
