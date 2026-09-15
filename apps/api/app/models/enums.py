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


class TraceEntityType(enum.Enum):
    BUSINESS_GOAL = "BUSINESS_GOAL"
    REQUIREMENT = "REQUIREMENT"
    USE_CASE = "USE_CASE"
    USER_STORY = "USER_STORY"


class TraceRelation(enum.Enum):
    DERIVES_FROM = "DERIVES_FROM"
    SATISFIES = "SATISFIES"
    CONFLICTS_WITH = "CONFLICTS_WITH"


DEPENDENCY_RELATIONS = {
    TraceRelation.DERIVES_FROM,
    TraceRelation.SATISFIES,
}
