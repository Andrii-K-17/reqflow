import enum


class Priority(enum.StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class StakeholderCategory(enum.Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    EXTERNAL = "EXTERNAL"
