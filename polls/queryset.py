from django.db.models import QuerySet


class DiscountCodeQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ClientQuerySet(QuerySet):
    def email(self, email):
        return self.filter(email=email)