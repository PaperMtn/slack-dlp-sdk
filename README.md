# Slack DLP SDK for Python

![Python 2.7 and 3 compatible](https://img.shields.io/pypi/pyversions/slack-dlp-sdk)
![PyPI version](https://img.shields.io/pypi/v/slack-dlp-sdk.svg)
![License: MIT](https://img.shields.io/pypi/l/slack-dlp-sdk.svg)

> [!NOTE]
> This SDK is not affiliated with or endorsed by Slack Technologies, Inc.

A Python SDK for interacting with Slack's Data Loss Prevention (DLP) features. This SDK allows retrieving, managing, and monitoring DLP policies and alerts for a Slack Enterprise.

It also provides a CLI for interacting with Slack DLP features directly from the command line.

## Prerequisites
1. Slack Enterprise Grid plan.
   - Slack DLP features are only available for Enterprise Grid customers.

2. The `d` cookie from a user with the `DLP Admin` role in the Slack Enterprise.
   - This cookie used to authenticate API requests made by the SDK. Instructions on how to retrieve the `d` cookie can be found on my blog [here](https://www.papermtn.co.uk/retrieving-and-using-slack-cookies-for-authentication/)

> [!NOTE]
> Best practice is to create a dedicated service account for this purpose that otherwise has as few permissions as possible.

## Using the SDK

### Authentication
To authenticate with the Slack DLP SDK, you need to provide the following when initializing the `SlackDLPClient`:
- `d_cookie`: The value of the `d` cookie from a user with the `DLP Admin` role.
- `enterprise_domain`: The domain of the Slack Enterprise, e.g. `your-enterprise.slack.com`.

```python
from slack_dlp_sdk import SlackDLPClient

client = SlackDLPClient(
   d_cookie="your_d_cookie_value",
   enterprise_domain="your-enterprise.slack.com",
   # Optional: Set a custom timeout (default is 30 seconds)
   timeout=60
)
```

### Alert Management

**Get all DLP Alerts**

```python
from slack_dlp_sdk import SlackDLPClient

# Initialize the Slack DLP Client
client = SlackDLPClient(...)

# Get all DLP Alerts
alerts = client.get_dlp_alerts()

# Get only archived DLP Alerts
archived_alerts = client.get_dlp_alerts(archived=True)

# Get alerts since an epoch timestamp
alerts = client.get_dlp_alerts(earliest=1767268800)

# Get alerts up to an epoch timestamp
alerts = client.get_dlp_alerts(latest=1767268800)

# Get active alerts in the past hour
import time
current_time = int(time.time())
one_hour_ago = current_time - 3600

alerts = client.get_dlp_alerts(
   earliest=one_hour_ago,
   latest=current_time
)
```

**Get a specific DLP Alert by ID**

```python
from slack_dlp_sdk import SlackDLPClient

# Initialize the Slack DLP Client
client = SlackDLPClient(...)

alert = client.get_dlp_alert_details(alert_id="alert123def")
```

**Archive a DLP Alert**

```python
from slack_dlp_sdk import SlackDLPClient

# Initialize the Slack DLP Client
client = SlackDLPClient(...)

# Archive a DLP Alert
client.archive_dlp_alert(alert_ids="alert123def")

# Archive multiple DLP Alerts
# Provide the alert IDs as a comma-separated string or a list
client.archive_dlp_alert(alert_ids=["alert123def", "alert456ghi"])

client.archive_dlp_alert(alert_ids="alert123def, alert456ghi")
```

**Unarchive a DLP Alert**

```python
from slack_dlp_sdk import SlackDLPClient

# Initialize the Slack DLP Client
client = SlackDLPClient(...)

# Unarchive a DLP Alert
client.unarchive_dlp_alert(alert_id="alert123def")

# Unarchive multiple DLP Alerts
# Provide the alert IDs as a comma-separated string or a list
client.unarchive_dlp_alert(alert_ids=["alert123def", "alert456ghi"])

client.unarchive_dlp_alert(alert_ids="alert123def, alert456ghi")
```

### Rule Management

**Get all DLP Rules** 

```python
from slack_dlp_sdk import SlackDLPClient

# Initialize the Slack DLP Client
client = SlackDLPClient(...)

rules = client.get_dlp_rules()
```

**Get a specific DLP Rule by ID**

```python
from slack_dlp_sdk import SlackDLPClient

# Initialize the Slack DLP Client
client = SlackDLPClient(...)

rule = client.get_dlp_rule(rule_id="abc123def")
```

**Create a new DLP Rule**

```python
from slack_dlp_sdk import (
   SlackDLPClient,
   SystemDetector,
   RuleAction,
   ChannelShareTargetType,
   ChannelType
)
# Initialize the Slack DLP Client
client = SlackDLPClient(...)

# Create a new DLP Rule
new_rule = client.create_dlp_rule(
   name="Test Rule",
   detectors=[SystemDetector.NATIONAL_ID_UNITED_KINGDOM],
   action=RuleAction.ALERT_ONLY,
   channel_share_target=ChannelShareTargetType.ALL,
   channel_type=[ChannelType.PUBLIC, ChannelType.PRIVATE],
   custom_message="Test Message"
)
```
**Update an existing DLP Rule**

```python
from slack_dlp_sdk import (
   SlackDLPClient,
   SystemDetector,
   RuleAction,
   ChannelShareTargetType,
   ChannelType
)
# Initialize the Slack DLP Client
client = SlackDLPClient(...)

# Update an existing DLP Rule
updated_rule = client.update_dlp_rule(
            rule_id="abc123def456",
            name="Updated Test Rule",
            detectors=[SystemDetector.ALL_CREDIT_CARDS],
            action=RuleAction.TOMBSTONE,
            channel_share_target=ChannelShareTargetType.ALL,
            channel_type=[ChannelType.DMS],
            custom_message="Updated Test Message"
        )

# Update an existing DLP Rule with a custom regex detector
# and target a specific workspace
updated_rule_with_regex = client.update_dlp_rule(
            rule_id="abc123def456",
            name="Updated Test Rule with Regex",
            detectors=[{"type": "REGEX", "pattern": r"\\b\\d{3}-\\d{2}-\\d{4}\\b"}],
            action=RuleAction.TOMBSTONE,
            channel_share_target=ChannelShareTargetType.ALL,
            channel_type=[ChannelType.DMS],
            custom_message="Updated Test Message with Regex",
            workspace_targets=["T0123456789A"]
        )
```

**Deactivate a DLP Rule**

```python
from slack_dlp_sdk import SlackDLPClient

# Initialize the Slack DLP Client
client = SlackDLPClient(...)

# Deactivate a DLP Rule
client.deactivate_dlp_rule(rule_id="abc123def456")
```

**Reactivate a DLP Rule**

```python
from slack_dlp_sdk import SlackDLPClient
# Initialize the Slack DLP Client
client = SlackDLPClient(...)

# Reactivate a DLP Rule
client.reactivate_dlp_rule(rule_id="abc123def456")
```

## CLI

The SDK includes a command-line interface (CLI) for interacting with Slack DLP features. To use the CLI, install the package and run the `slack-dlp` command.

```bash
pip install slack-dlp-sdk
slack-dlp --help
```

### Usage

```bash
usage: slack-dlp [-h] [--slack-cookie SLACK_COOKIE] [--enterprise-domain ENTERPRISE_DOMAIN] {rule,alert} ...

Slack DLP SDK CLI

positional arguments:
  {rule,alert}
    rule                Manage DLP rules
    alert               Manage DLP alerts

options:
  -h, --help            show this help message and exit
  --slack-cookie SLACK_COOKIE
                        Slack 'd' cookie value (prefer env var D_COOKIE).
  --enterprise-domain ENTERPRISE_DOMAIN
                        Slack enterprise domain (prefer env var ENTERPRISE_DOMAIN).
```