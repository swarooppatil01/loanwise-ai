from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class EmploymentType(str, Enum):
    SALARIED = "salaried"
    SELF_EMPLOYED = "self_employed"
    PROFESSIONAL = "professional"
    BUSINESS_OWNER = "business_owner"
    OTHER = "other"


class LoanType(str, Enum):
    PERSONAL = "personal"
    HOME = "home"
    EDUCATION = "education"
    VEHICLE = "vehicle"


class ApplicationStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    PROCESSED = "processed"
    FAILED = "failed"
