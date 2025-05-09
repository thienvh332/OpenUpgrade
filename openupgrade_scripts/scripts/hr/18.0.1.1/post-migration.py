from openupgradelib import openupgrade

_deleted_xml_records = [
    "hr.action_hr_employee_create_user",
    "hr.hr_presence_control_login",
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env, "hr", "18.0.1.1/noupdate_changes.xml")
    openupgrade.delete_record_translations(
        env.cr, "hr", ["contract_type_part_time"], ["name"]
    )
    openupgrade.delete_records_safely_by_xml_id(
        env,
        _deleted_xml_records,
    )

    # Set hr_presence_state to 'archive' where employee is not active
    employees = (
        env["hr.employee"]
        .with_context(active_test=False)
        .search([("active", "=", False)])
    )
    for emp in employees:
        emp.hr_presence_state = "archive"
