"""
Supabase Client
"""

from supabase import Client, create_client

from app.config.settings import settings


class SupabaseService:

    def __init__(self):

        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_ANON_KEY,
        )

    # -----------------------------

    def sign_up(
        self,
        email: str,
        password: str,
    ):

        return self.client.auth.sign_up(
            {
                "email": email,
                "password": password,
            }
        )

    # -----------------------------

    def sign_in(
        self,
        email: str,
        password: str,
    ):

        return self.client.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )

    # -----------------------------

    def refresh_session(
        self,
        refresh_token: str,
    ):

        return self.client.auth.refresh_session(
            refresh_token
        )

    # -----------------------------

    def get_user(
        self,
        token: str,
    ):

        return self.client.auth.get_user(token)

    # -----------------------------

    def sign_out(self):

        return self.client.auth.sign_out()


supabase_service = SupabaseService()

supabase = supabase_service.client

print("=" * 60)
print("SUPABASE_URL:", settings.SUPABASE_URL)
print("SUPABASE_ANON_KEY:", settings.SUPABASE_ANON_KEY)
print("=" * 60)