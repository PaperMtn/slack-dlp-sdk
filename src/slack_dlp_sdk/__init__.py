"""Slack Data Loss Prevention (DLP) SDK"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from slack_dlp_sdk.client import SlackDLPClient
from slack_dlp_sdk.exceptions import (
    SlackAPIError,
    SlackAuthError,
    SlackHTTPError,
    SlackRateLimitedError,
)
from slack_dlp_sdk.sdk.models import (
    RuleAction,
    SystemDetector,
    ChannelType,
    ChannelShareTargetType,
)

try:
    __version__ = version("slack-dlp-sdk")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    "SlackDLPClient",
    "SlackAPIError",
    "SlackAuthError",
    "SlackHTTPError",
    "SlackRateLimitedError",
    "RuleAction",
    "SystemDetector",
    "ChannelType",
    "ChannelShareTargetType",
]
