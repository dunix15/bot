from django.db.models import QuerySet


class DiscountCodeQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)


class ClientQuerySet(QuerySet):
    def email(self, email):
        return self.filter(email=email)

    def fb_id(self, fb_id):
        return self.filter(fb_id=fb_id)