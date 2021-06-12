from django.db import models


class Page(models.Model):

    page_id = models.TextField('page_id')
    page_name = models.TextField('page_name')
    created_at = models.DateTimeField('created_at')
    user_id = models.TextField('user_id')
    domain_name = models.TextField('domain_name')

    def __str__(self):
        return str(self.page_name)

    @classmethod
    def get_all_domains(cls):
        domains = list()
        data = Page.objects.all()
        for row in data:
            domains.append(row.domain_name)
        return list(set(domains))

    @classmethod
    def get_pages_by_user(cls, user_id):
        pages = list()
        data = Page.objects.filter(user_id=user_id)
        for row in data:
            pages.append(row.page_name)
        return pages

    @classmethod
    def get_number_of_articles(cls, domain_name):
        data = Page.objects.filter(domain_name=domain_name)
        return data.count()

    @classmethod
    def get_page_by_id(cls, page_id):
        data = Page.objects.filter(page_id=page_id)
        return data

    @classmethod
    def get_users_by_time(cls, date_start, date_end):
        data = Page.objects.filter(created_at__gt=date_start, created_at__lt=date_end)
        res = list()
        user_ids = set()
        for user in data:
            if user.user_id not in user_ids:
                res.append({"user": user.user_id, "number": len(data.filter(user_id=user.user_id))})
            user_ids.add(user.user_id)
        return res
