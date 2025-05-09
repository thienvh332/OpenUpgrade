from openupgradelib import openupgrade


def _column_exists(cr, table, column):
    cr.execute(
        """
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = %s AND column_name = %s
    """,
        (table, column),
    )
    return cr.fetchone() is not None


def _update_hr_presence_state(env):
    table = "hr_employee"
    column = "hr_presence_state"

    if _column_exists(env.cr, table, column):
        # Copy old column values to backup legacy column
        openupgrade.copy_columns(
            env.cr,
            {
                table: [(column, None, None)],
            },
        )

        # Map old value to new
        old_column = openupgrade.get_legacy_name(column)
        openupgrade.map_values(
            env.cr,
            old_column,
            column,
            [("to_define", "out_of_working_hour")],
            table=table,
        )


_new_columns = [
    (
        "hr.employee",
        "distance_home_work_unit",
        "selection",
        "kilometers",
        "hr_employee",
    ),
]

_new_fields = [
    ("is_flexible", "hr.employee", "hr_employee", "boolean", False, "hr"),
    ("is_fully_flexible", "hr.employee", "hr_employee", "boolean", False, "hr"),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_columns(
        env.cr, {"employee_category_rel": [("emp_id", "employee_id")]}
    )
    openupgrade.add_columns(env, _new_columns)
    openupgrade.add_fields(env, _new_fields)
    _update_hr_presence_state(env)
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE hr_employee
        SET is_flexible = false, is_fully_flexible = false
        """,
    )

    openupgrade.logged_query(
        env.cr,
        """
        UPDATE hr_employee
        SET marital = 'single'
        WHERE marital IS NULL
        """,
    )
