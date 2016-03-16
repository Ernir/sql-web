from django.test import TestCase, Client


class SectionViewTests(TestCase):
    fixtures = ["test_data.json"]

    @classmethod
    def setUpTestData(cls):
        pass

    def test_if_200(self):
        client = Client()
        response = client.get("/vidfangsefni/mysql/")
        self.assertEqual(response.status_code, 200)