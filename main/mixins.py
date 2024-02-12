from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden

class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin to require that the user is an admin.
    """

    def test_func(self):
        """
        Custom test function to check if the user is an admin.
        """
        return self.request.user.is_authenticated and self.request.user.is_staff and self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Handle the case when the user is not an admin.
        Override this method to customize the behavior.
        """
        return HttpResponseForbidden("You do not have permission to access this page.")
