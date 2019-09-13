from django.test import TestCase

from api.v1.serializers import WorkSerializerVersion1
from api.views import AllWorks, GetSerializerClasses, SingleWork
from rest_framework.test import APITestCase
from users.models import CustomUser

from works.models import Work


class SerializerRetrievalTest(TestCase):
    def test_can_get_correct_serializers_for_api_version(self):
        work_serializer = GetSerializerClasses("v1").work_serializer
        image_serializer = GetSerializerClasses("v1").image_serializer

        self.assertEqual(work_serializer.__name__, "WorkSerializerVersion1")
        self.assertEqual(image_serializer.__name__, "ImageSerializerVersion1")


class WorkViewsGETTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_one = CustomUser.objects.create(username="matisse")
        cls.user_one_work = Work.objects.create(
            owner=cls.user_one,
            title="Dance",
            year_from=1910,
            year_to=1910,
            technique="Oil on canvas",
            height=260,
            width=391,
            description=(
                "Five dancing figures painted in a strong red and set"
                " against a green landscape and deep blue sky."
            ),
        )

        cls.user_two = CustomUser.objects.create(username="rousseau")
        cls.user_two_work = Work.objects.bulk_create(
            [
                Work(
                    owner=cls.user_two,
                    title="Exotic Landscape",
                    year_to=1908,
                    technique="Oil on canvas",
                    description=(
                        "Monkeys picking up oranges in a jungle painted with"
                        " rich greens in the leaves, grass and trees."
                    ),
                ),
                Work(
                    owner=cls.user_two,
                    title="Fight Between a Tiger and a Buffalo",
                    year_to=1908,
                    technique="Oil on canvas",
                    description=(
                        "A imaginary scene of a tiger attacking a buffalo in"
                        " a fantastic jungle environment."
                    ),
                ),
                Work(
                    owner=cls.user_two,
                    title="The Dream",
                    year_to=1910,
                    technique="Oil on canvas",
                    description=(
                        "A surreal scene of Rousseau's mistress on a divan,"
                        "gazing over a landscape of flowers and animals."
                    ),
                ),
            ]
        )

    def test_can_get_all_works_for_user(self):
        res = self.client.get(
            "http://127.0.0.1:8000/api/v1/users/matisse/works/"
        )
        works = Work.objects.filter(owner__username=self.user_one)
        serializer = WorkSerializerVersion1(works, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_cannot_get_works_for_non_existing_user(self):
        res = self.client.get(
            "http://127.0.0.1:8000/api/v1/users/non-existing-user/works/"
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, [])

    def test_can_get_all_works_from_year_to_for_user(self):
        res = self.client.get(
            "http://127.0.0.1:8000/api/v1/users/rousseau/works/",
            {"year_to": 1908},
        )
        works = Work.objects.filter(
            owner__username=self.user_two, year_to=1908
        )
        serializer = WorkSerializerVersion1(works, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_cannot_get_works_from_non_existing_year_to(self):
        res = self.client.get(
            "http://127.0.0.1:8000/api/v1/users/rousseau/works/",
            {"year_to": "not a year"},
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data, [])

    def test_can_get_single_work_for_user(self):
        res = self.client.get(
            "http://127.0.0.1:8000/api/v1/users/rousseau/works/4/"
        )
        work = Work.objects.filter(owner__username=self.user_two, id=4)
        serializer = WorkSerializerVersion1(work, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_cannot_get_work_from_invalid_id(self):
        res_invalid_integer = self.client.get(
            "http://127.0.0.1:8000/api/v1/users/rousseau/works/1000/"
        )
        res_invalid_string = self.client.get(
            "http://127.0.0.1:8000/api/v1/users/rousseau/works/not-a-integer/"
        )

        self.assertEqual(res_invalid_integer.status_code, 200)
        self.assertEqual(res_invalid_integer.data, [])
        self.assertEqual(res_invalid_string.status_code, 404)
