# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # pre-create xmlid for snailmail service if iap migration has created an sms service
    openupgrade.logged_query(
        env.cr,
        """
        INSERT INTO ir_model_data
        (
            create_uid, create_date, write_uid, write_date, name,
            module, model, res_id
        )
        SELECT
            create_uid, create_date, write_uid, write_date, 'iap_service_snailmail',
            'snailmail', 'iap.service', id
        FROM iap_service
        WHERE technical_name='snailmail'
        """,
    )
