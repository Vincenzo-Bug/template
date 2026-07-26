"""Default capability-boundary tests."""

from app.core.security import PROHIBITED_AGENT_CAPABILITIES


def test_high_risk_capabilities_are_explicitly_prohibited() -> None:
    """The declared deny set must cover all critical agent escape paths."""
    required = {
        "external_side_effect",
        "filesystem",
        "private_key",
        "raw_sql",
        "secret_store",
        "shell",
        "system_command",
        "process_execution",
    }

    assert required <= PROHIBITED_AGENT_CAPABILITIES
