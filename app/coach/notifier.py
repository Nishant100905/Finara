"""
Notification service for Financial Coach.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class CoachNotifier:
    """
    Notification abstraction.

    Future integrations:

    - Email
    - SMS
    - Push Notifications
    - WhatsApp
    - Telegram
    """

    def send_email(
        self,
        recipient: str,
        subject: str,
        message: str,
    ) -> bool:

        logger.info(
            "Email notification -> %s",
            recipient,
        )

        return True

    def send_push(
        self,
        user_id: str,
        message: str,
    ) -> bool:

        logger.info(
            "Push notification -> %s",
            user_id,
        )

        return True

    def send_sms(
        self,
        phone: str,
        message: str,
    ) -> bool:

        logger.info(
            "SMS notification -> %s",
            phone,
        )

        return True

    def send_whatsapp(
        self,
        phone: str,
        message: str,
    ) -> bool:

        logger.info(
            "WhatsApp notification -> %s",
            phone,
        )

        return True


coach_notifier = CoachNotifier()