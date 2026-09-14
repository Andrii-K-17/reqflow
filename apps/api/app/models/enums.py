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


class RequirementType(enum.Enum):
    BUSINESS = "BUSINESS"
    USER = "USER"
    FUNCTIONAL = "FUNCTIONAL"
    NONFUNCTIONAL = "NONFUNCTIONAL"
    SYSTEM = "SYSTEM"


class RequirementStatus(enum.Enum):
    DRAFT = "DRAFT"
    REVIEWED = "REVIEWED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


REQUIREMENT_CODE_PREFIX: dict[RequirementType, str] = {
    RequirementType.BUSINESS: "BR",
    RequirementType.USER: "UR",
    RequirementType.FUNCTIONAL: "FR",
    RequirementType.NONFUNCTIONAL: "NFR",
    RequirementType.SYSTEM: "SR",
}
