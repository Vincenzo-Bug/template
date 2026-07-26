"""Default deny set for future automation or AI capabilities.

Keep high-risk capabilities disabled until a product-specific policy, threat
model, and tested authorization boundary explicitly allow them.
"""

PROHIBITED_AGENT_CAPABILITIES: frozenset[str] = frozenset(
    {
        "arbitrary_network",
        "external_side_effect",
        "filesystem",
        "private_key",
        "raw_sql",
        "secret_store",
        "shell",
        "system_command",
        "process_execution",
    }
)
