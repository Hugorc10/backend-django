from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from drones.models import DroneCategory

# Create your tests here.
class DroneCategoryTests(APITestCase):
    def post_drone_category(self, name):
        url = reverse("dronecategory-list")
        data = { "name": name }
        response = self.client.post(url, data, format="json")
        return response

    # Testa o metodo POST
    def test_post_drone_category(self):
        new_drone_category_name = "Hexacopter"
        response = self.post_drone_category(new_drone_category_name)
        print("PK {0}".format(DroneCategory.objects.get().pk))

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, DroneCategory.objects.count())
        self.assertEquals(new_drone_category_name, DroneCategory.objects.get().name)

    # Testa unicidade do nome (Constraint)
    def test_post_existing_drone_category_name(self):
        new_drone_category_name = "Duplicated Copter"
        # data = { "name": new_drone_category_name }
        response1 = self.post_drone_category(new_drone_category_name)
        self.assertEqual(status.HTTP_201_CREATED, response1.status_code)
        response2 = self.post_drone_category(new_drone_category_name)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response2.status_code)

    def test_get_drone_categories_collection(self):
        new_drone_category_name = "Super Copter"
        self.post_drone_category(new_drone_category_name)

        url = reverse("dronecategory-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response_data = response.json()
        self.assertEqual(1, response_data["count"])
        self.assertEqual(new_drone_category_name, response_data["results"][0]["name"])



