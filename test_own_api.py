import random
from unittest import TestCase
import requests
import json
import time
import random

from db import Sql
BASE_URL = "http://localhost:5000/api/"


class TestRecipeApe(TestCase):

    def test_get_random_recipe(self):
        url = BASE_URL + "recipes/random/query=random"
        start_time = time.time()
        response = requests.get(url=url)
        response_time = round((time.time() - start_time) * 1000)

        assert response.status_code == 200
        assert response.text is not None
        assert response_time <= 2000

    def test_get_recipe_by_name(self):
        recipe_name = "pizza"
        url = BASE_URL + f"recipes/search/query={recipe_name}"
        start_time = time.time()
        response = requests.get(url=url)
        response_time = round((time.time() - start_time) * 1000)

        response_json = response.json()

        title_words = response_json["title"].lower().split(" ")

        assert response.status_code == 200
        assert response.text is not None
        assert response_time <= 2000
        assert recipe_name in title_words

    def test_get_recipe_by_ingredients(self):
        ingredients_input = {"spaghetti":False, "beef":False}
        ingredients_str = ",+".join(list(ingredients_input.keys()))
        url = BASE_URL + f"recipes/byingredients/ingredients={ingredients_str}"

        start_time = time.time()
        response = requests.get(url=url)
        response_time = round((time.time() - start_time) * 1000)

        response_json = response.json()

        ingredients_in_recipe = []
        for ingredient in response_json["extendedIngredients"]:
            ingredients_in_recipe.append(ingredient["name"].lower().split(" "))

        for ingredients in ingredients_in_recipe:
            for ingredient in ingredients:
                if ingredient in ingredients_input.keys():
                    ingredients_input[ingredient] = True

        assert response.status_code == 200
        assert response.text is not None
        assert response_time <= 2000
        assert all(list(ingredients_input.values()))

    def test_post_user(self):
        url = BASE_URL + f"recipe/adduserslist"
        user_code = random.randint(a=0, b=10000)
        user_name = "Anton Shchur"

        user_json = {"name": user_name, "userCode": user_code}

        start_time = time.time()
        response = requests.post(url, json=user_json)
        response_time = round((time.time() - start_time) * 1000)

        sql = Sql(database="master")
        cursor = sql.cnxn.cursor()
        select_query = f"SELECT COUNT(*) FROM Users WHERE Users.name = 'Anton Shchur' and Users.userCode ={user_code}"
        cursor.execute(select_query)


        assert response.status_code == 200
        assert response.text is not None
        assert response_time <= 2000
        assert cursor.fetchall()[0][0] == 1
        assert response.json().get("name", False) == user_name
        assert response.json().get("userCode", False) == user_code

    def test_post_user_recipe(self):
        url = BASE_URL + f"recipe/adduserslist"
        user_code = random.randint(a=0, b=10000)
        user_name = "Anton Shchur"

        user_json = {"name": user_name, "userCode": user_code}
        requests.post(url, json=user_json)

        url_for_post_recipe = BASE_URL + f"recipes/AddRecipe/usercode={user_code}"

        recipe_json = {"id": 8888,
                       "title": "Recipe",
                       "image": "Image.png",
                       "sourceUrl": "https",
                       "summary": "Easy recipe",
                       "extendedIngredients": [{"id": 2044,
                                                "aisle": "Produce",
                                                "consistency": "solid",
                                                "name": "basil",
                                                "original": "1/2 cup Thai basil or you can use regular basil",
                                                "originalString": "1/2 cup Thai basil or you can use regular basil",
                                                "originalName": "Thai basil or you can use regular basil",
                                                "amount": 0.5,
                                                "unit": "cup"}],
                       "Instruction": "instruction",
                       "spoonacularSourceUrl": "http"
                       }

        requests.post(url_for_post_recipe, json=recipe_json)
        url_for_get_recipe = BASE_URL + f"recipes/getUsersRecipe/usercode={user_code}"

        start_time = time.time()
        response_for_get = requests.get(url_for_get_recipe)
        response_time = round((time.time() - start_time) * 1000)

        assert response_for_get.status_code == 200
        assert response_for_get.text is not None
        assert response_time <= 2000
        assert response_for_get.json() == recipe_json

    def test_delete_recipe(self):
        url = BASE_URL + f"recipe/adduserslist"
        user_code = 5000
        recipe_id = 4999
        user_name = "Anton Shchur"
        user_json = {"name": user_name, "userCode": user_code}
        requests.post(url, json=user_json)
        url_for_post_recipe = BASE_URL + f"recipes/AddRecipe/usercode={user_code}"
        recipe_json = {"id": recipe_id,
                       "title": "Recipe",
                       "image": "Image.png",
                       "sourceUrl": "https",
                       "summary": "Easy recipe",
                       "extendedIngredients": [{"id": 2044,
                                                "aisle": "Produce",
                                                "consistency": "solid",
                                                "name": "basil",
                                                "original": "1/2 cup Thai basil or you can use regular basil",
                                                "originalString": "1/2 cup Thai basil or you can use regular basil",
                                                "originalName": "Thai basil or you can use regular basil",
                                                "amount": 0.5,
                                                "unit": "cup"}],
                       "Instruction": "instruction",
                       "spoonacularSourceUrl": "http"
                       }
        requests.post(url_for_post_recipe, json=recipe_json)
        url_for_delete = BASE_URL + f"recipes/deleteRecipe/usercode={user_code},recipeid={recipe_id}"
        start_time = time.time()
        response_for_delete = requests.delete(url_for_delete)
        response_time = round((time.time() - start_time) * 1000)
        sql = Sql(database="master")
        cursor = sql.cnxn.cursor()
        select_query = "SELECT COUNT(*) FROM Recipes WHERE Recipes.recipeCode = 4999 " \
                       "and Recipes.UserId in (SELECT Users.id FROM Users WHERE userCode = 5000)"
        cursor.execute(select_query)

        assert response_for_delete.status_code == 204
        assert response_time <= 2000
        assert cursor.fetchall()[0][0] == 0