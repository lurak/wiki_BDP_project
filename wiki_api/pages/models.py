from django.db import models


class Page(models.Model):
    """
    Class to work with page table in DB
    """

    page_id = models.TextField('page_id')
    page_name = models.TextField('page_name')
    created_at = models.DateTimeField('created_at')
    user_id = models.TextField('user_id')
    domain_name = models.TextField('domain_name')

    def __str__(self):
        return str(self.page_name)

    @classmethod
    def get_all_domains(cls):
        """
        Return the list of existing domains for which pages were created.
        :return: list of existing domains
        """
        domains = list()
        data = Page.objects.all().distinct('domain_name')
        for row in data:
            domains.append(row.domain_name)
        return domains

    @classmethod
    def get_pages_by_user(cls, user_id):
        """
        Return all the pages which were created by the user with a specified user_id
        :param user_id: user id
        :return: list of pages
        """
        pages = list()
        data = Page.objects.filter(user_id=user_id)
        for row in data:
            pages.append(row.page_name)
        return pages

    @classmethod
    def get_number_of_articles(cls, domain_name):
        """
        Return the number of articles created for a specified domain
        :param domain_name: name of domain
        :return: number of articles
        """
        data = Page.objects.filter(domain_name=domain_name)
        return data.count()

    @classmethod
    def get_page_by_id(cls, page_id):
        """
        Return the page with the specified page_id
        :param page_id: page id
        :return: page
        """
        data = Page.objects.filter(page_id=page_id)
        return data

    @classmethod
    def get_users_by_time(cls, date_start, date_end):
        """
        Return the id, name, and the number of created pages of all the users
        who created at least one page in a specified time range.
        :param date_start: start of time range
        :param date_end: end of time range
        :return: list of users
        """
        data = Page.objects.filter(created_at__gt=date_start, created_at__lt=date_end)
        res = list()
        user_ids = set()
        for user in data:
            if user.user_id not in user_ids:
                res.append({"user": user.user_id,
                            "name": User.get_by_id(user.user_id)[0].user_name,
                            "number": len(data.filter(user_id=user.user_id))})
            user_ids.add(user.user_id)
        return res


class User(models.Model):
    """
    Class to work with user table in DB
    """

    user_id = models.TextField('user_id', unique=True)
    user_name = models.TextField('user_name')
    user_is_bot = models.BooleanField('user_id_bot')

    @classmethod
    def get_by_id(cls, user_id):
        """
        Get data about user by id
        :param user_id: user id
        :return: info about user
        """
        data = User.objects.filter(user_id=user_id)
        return data
