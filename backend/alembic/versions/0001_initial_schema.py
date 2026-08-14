"""create initial LoanWise schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-08-13
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


user_role = sa.Enum("USER", "ADMIN", name="user_role")

employment_type = sa.Enum(
    "SALARIED", "SELF_EMPLOYED", "PROFESSIONAL", "BUSINESS_OWNER", "OTHER",
    name="employment_type",
)

loan_type = sa.Enum(
    "PERSONAL", "HOME", "EDUCATION", "VEHICLE",
    name="loan_type",
)

application_loan_type = sa.Enum(
    "PERSONAL", "HOME", "EDUCATION", "VEHICLE",
    name="application_loan_type",
)

application_status = sa.Enum(
    "DRAFT", "SUBMITTED", "PROCESSED", "FAILED",
    name="application_status",
)


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False, server_default="USER"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)

    op.create_table(
        "user_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("employment_type", employment_type, nullable=True),
        sa.Column("monthly_income", sa.Numeric(14, 2), nullable=True),
        sa.Column("monthly_obligations", sa.Numeric(14, 2), nullable=True),
        sa.Column("credit_score", sa.Integer(), nullable=True),
        sa.Column("employment_duration_months", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("user_id", name="uq_user_profiles_user_id"),
    )
    op.create_index("ix_user_profiles_user_id", "user_profiles", ["user_id"], unique=True)

    op.create_table(
        "loan_products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("lender", sa.String(length=120), nullable=False),
        sa.Column("loan_type", loan_type, nullable=False),
        sa.Column("min_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("max_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("min_income", sa.Numeric(14, 2), nullable=False),
        sa.Column("min_credit_score", sa.Integer(), nullable=False),
        sa.Column("max_dti", sa.Numeric(5, 4), nullable=False),
        sa.Column("min_interest_rate", sa.Numeric(5, 2), nullable=False),
        sa.Column("max_interest_rate", sa.Numeric(5, 2), nullable=False),
        sa.Column("min_tenure_months", sa.Integer(), nullable=False),
        sa.Column("max_tenure_months", sa.Integer(), nullable=False),
        sa.Column("processing_fee_percent", sa.Numeric(5, 2), nullable=False),
        sa.Column("employment_types", sa.Text(), nullable=False),
        sa.Column("special_conditions", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_loan_products_name", "loan_products", ["name"], unique=False)

    op.create_table(
        "loan_eligibility_rules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("loan_product_id", sa.Integer(), nullable=False),
        sa.Column("rule_type", sa.String(length=80), nullable=False),
        sa.Column("rule_value", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["loan_product_id"], ["loan_products.id"], ondelete="CASCADE"),
    )
    op.create_index(
        "ix_loan_eligibility_rules_loan_product_id",
        "loan_eligibility_rules",
        ["loan_product_id"],
        unique=False,
    )

    op.create_table(
        "loan_applications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("loan_type", application_loan_type, nullable=False),
        sa.Column("loan_amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("preferred_tenure_months", sa.Integer(), nullable=False),
        sa.Column("purpose", sa.String(length=500), nullable=False),
        sa.Column("status", application_status, nullable=False, server_default="DRAFT"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index(
        "ix_loan_applications_user_id",
        "loan_applications",
        ["user_id"],
        unique=False,
    )

    op.create_table(
        "recommendations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("application_id", sa.Integer(), nullable=False),
        sa.Column("loan_product_id", sa.Integer(), nullable=False),
        sa.Column("score", sa.Numeric(6, 3), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("eligible", sa.Boolean(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["application_id"], ["loan_applications.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["loan_product_id"], ["loan_products.id"], ondelete="CASCADE"),
    )
    op.create_index(
        "ix_recommendations_application_id",
        "recommendations",
        ["application_id"],
        unique=False,
    )
    op.create_index(
        "ix_recommendations_loan_product_id",
        "recommendations",
        ["loan_product_id"],
        unique=False,
    )

    op.create_table(
        "recommendation_factors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("recommendation_id", sa.Integer(), nullable=False),
        sa.Column("factor", sa.String(length=100), nullable=False),
        sa.Column("value", sa.Numeric(8, 4), nullable=False),
        sa.Column("weight", sa.Numeric(8, 4), nullable=False),
        sa.Column("contribution", sa.Numeric(8, 4), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["recommendation_id"], ["recommendations.id"], ondelete="CASCADE"),
    )
    op.create_index(
        "ix_recommendation_factors_recommendation_id",
        "recommendation_factors",
        ["recommendation_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_recommendation_factors_recommendation_id", table_name="recommendation_factors")
    op.drop_table("recommendation_factors")

    op.drop_index("ix_recommendations_loan_product_id", table_name="recommendations")
    op.drop_index("ix_recommendations_application_id", table_name="recommendations")
    op.drop_table("recommendations")

    op.drop_index("ix_loan_applications_user_id", table_name="loan_applications")
    op.drop_table("loan_applications")

    op.drop_index(
        "ix_loan_eligibility_rules_loan_product_id",
        table_name="loan_eligibility_rules",
    )
    op.drop_table("loan_eligibility_rules")

    op.drop_index("ix_loan_products_name", table_name="loan_products")
    op.drop_table("loan_products")

    op.drop_index("ix_user_profiles_user_id", table_name="user_profiles")
    op.drop_table("user_profiles")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    bind = op.get_bind()
    application_status.drop(bind, checkfirst=True)
    application_loan_type.drop(bind, checkfirst=True)
    loan_type.drop(bind, checkfirst=True)
    employment_type.drop(bind, checkfirst=True)
    user_role.drop(bind, checkfirst=True)
