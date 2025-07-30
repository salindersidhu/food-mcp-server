import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Create an MCP server
mcp = FastMCP("MealBot")

# API Setup
MEALDB_BASE_URL = "https://www.themealdb.com/api/json/v1/1/"
USDA_BASE_URL = "https://api.nal.usda.gov/fdc/v1/"
USDA_API_KEY = os.getenv("USDA_API_KEY")


@mcp.tool(title="Meal Ingredients Fetcher")
async def fetch_meal_ingredients_by_name(name: str) -> dict:
    """
    Fetch meals by their name.

    Args:
        name (str): The name of the meal to search for.

    Returns:
        dict: A dictionary with a single key "meals", which is a list of meal objects.
        Each meal object contains:
            - idMeal (str): The ID of the meal.
            - strMeal (str): The name of the meal.
            - strCategory (str): The meal's category.
            - strArea (str): The area/cuisine of the meal.
            - strYoutube (str or None): YouTube video URL.
            - strInstructions (str): Cooking instructions.

        Example:
        {
            "meals": [
                {
                    "idMeal": "52771",
                    "strMeal": "Spicy Arrabiata Penne",
                    "strCategory": "Vegetarian",
                    "strArea": "Italian",
                    "strYoutube": "https://www.youtube.com/watch?v=1IszT_guI08",
                    "strInstructions": "Bring a large pot of water to a boil. ..."
                }
            ]
        }
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MEALDB_BASE_URL}search.php?s={name}")
        data = response.json()

        if data.get("meals") is None:
            return {"meals": []}

        filtered_meals = [
            {
                "idMeal": meal.get("idMeal"),
                "strMeal": meal.get("strMeal"),
                "strCategory": meal.get("strCategory"),
                "strArea": meal.get("strArea"),
                "strYoutube": meal.get("strYoutube"),
                "strInstructions": meal.get("strInstructions"),
            }
            for meal in data["meals"]
        ]
        return {"meals": filtered_meals}


@mcp.tool(title="Meal Instructions Fetcher")
async def fetch_meal_instructions_by_id(id: str):
    """
    Fetch meal instructions and ingredients by meal ID.

    Args:
        name (str): The meal ID to look up.

    Returns:
        list: A list of meal objects, each containing:
            - idMeal (str)
            - strMeal (str)
            - strCategory (str)
            - strArea (str)
            - strYoutube (str or None)
            - strIngredient1..20 (str or None)
            - strMeasure1..20 (str or None)

        Example:
        {
            "meals": [
                {
                    "idMeal": "52771",
                    "strMeal": "Spicy Arrabiata Penne",
                    "strCategory": "Vegetarian",
                    "strArea": "Italian",
                    "strYoutube": "https://www.youtube.com/watch?v=1IszT_guI08",
                    "strIngredient1": "Penne Rigate",
                    "strMeasure1": "2 cups",
                    ...
                }
            ]
        }
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MEALDB_BASE_URL}lookup.php?i={id}")
        data = response.json()

        if data.get("meals") is None:
            return {"meals": []}

        filtered_meals = []
        for meal in data["meals"]:
            filtered = {
                "idMeal": meal.get("idMeal"),
                "strMeal": meal.get("strMeal"),
                "strCategory": meal.get("strCategory"),
                "strArea": meal.get("strArea"),
                "strYoutube": meal.get("strYoutube"),
            }
            # Add strIngredient1..20 and strMeasure1..20
            for i in range(1, 21):
                filtered[f"strIngredient{i}"] = meal.get(f"strIngredient{i}")
                filtered[f"strMeasure{i}"] = meal.get(f"strMeasure{i}")
            filtered_meals.append(filtered)
        return {"meals": filtered_meals}


@mcp.tool(title="Meal Categories Fetcher")
async def fetch_meal_categories() -> dict:
    """
    Fetch all meal categories.

    Returns:
        dict: A dictionary with a single key "categories", which is a list of category objects.
        Each category object contains:
            - idCategory (str): The ID of the category.
            - strCategory (str): The name of the category.
            - strCategoryThumb (str): URL to the category thumbnail image.
            - strCategoryDescription (str): Description of the category.

        Example:
        {
            "categories": [
                {
                    "idCategory": "1",
                    "strCategory": "Beef",
                    "strCategoryThumb": "https://www.themealdb.com/images/category/beef.png",
                    "strCategoryDescription": "Beef is the culinary name for meat from cattle, ..."
                },
                ...
            ]
        }
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MEALDB_BASE_URL}categories.php")
        return response.json()


@mcp.tool(title="Meal Fetcher by Location")
async def fetch_meal_by_location(location: str) -> dict:
    """
    Fetch meals by location.

    Returns:
        dict: A dictionary with a single key "meals", which is a list of meal objects.
        Each meal object contains:
            - strMeal (str): The name of the meal.
            - strMealThumb (str): URL to the meal thumbnail image.
            - idMeal (str): The ID of the meal. 
        Example:
        {
            "meals": [
                {
                    "strMeal": "BeaverTails",
                    "strMealThumb": "https://www.themealdb.com/images/media/meals/ryppsv1511815505.jpg",
                    "idMeal": "52928"
                },
                ...
            ]
        }
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MEALDB_BASE_URL}filter.php?a={location}")
        return response.json()


@mcp.tool(title="Ingredient Nutrition Fetcher")
async def fetch_ingredient_nutrition(ingredient: str) -> dict:
    """
    Fetch nutritional information for an ingredient.

    Args:
        ingredient (str): The name of the ingredient to search for.

    Returns:
        dict: A dictionary containing nutritional information for the ingredient.
        The dictionary includes:
            - description (str): The name/description of the food
            - nutrients (list): List of nutrients, each containing:
                - name (str): Name of the nutrient (e.g., "Energy", "Protein", "Total lipid (fat)")
                - amount (float): Amount of the nutrient
                - unit (str): Unit of measurement (e.g., "kcal", "g")

        Example:
        {
            "description": "Chicken breast, raw",
            "nutrients": [
                {
                    "name": "Energy",
                    "amount": 120.0,
                    "unit": "kcal"
                }
            ]
        }
    """
    async with httpx.AsyncClient() as client:
        # Step 1: Search for the food item
        search_params = {
            "api_key": USDA_API_KEY,
            "query": ingredient,
            "dataType": ["Foundation", "SR Legacy"],
            "pageSize": 1,
            "sortBy": "score"
        }
        
        search_response = await client.get(
            f"{USDA_BASE_URL}foods/search",
            params=search_params
        )
        search_data = search_response.json()

        if not search_data.get("foods"):
            return {"description": None, "nutrients": []}

        # Get the fdcId from the first (best matching) result
        food = search_data["foods"][0]
        food_id = food["fdcId"]

        # Step 2: Get detailed nutritional information
        detail_params = {
            "api_key": USDA_API_KEY
        }
        
        detail_response = await client.get(
            f"{USDA_BASE_URL}food/{food_id}",
            params=detail_params
        )
        detail_data = detail_response.json()

        # Extract relevant nutritional information
        nutrients = []
        for nutrient in detail_data.get("foodNutrients", []):
            if "amount" in nutrient and nutrient["amount"] is not None:
                nutrients.append({
                    "name": nutrient["nutrient"]["name"],
                    "amount": nutrient["amount"],
                    "unit": nutrient["nutrient"]["unitName"].lower()
                })

        return {
            "description": detail_data.get("description", None),
            "nutrients": nutrients
        }


if __name__ == "__main__":
    # Start the server
    mcp.run()
