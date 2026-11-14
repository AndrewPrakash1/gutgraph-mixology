"""First-call smoke test (STARTER_GUIDE §4). Run from repo root or backend/."""
from foodoscope_client import Foodoscope


def main() -> None:
    fs = Foodoscope()
    data = fs.get("/recipe2-api/recipe/recipeofday")
    print("recipe of the day:", str(data)[:500])


if __name__ == "__main__":
    main()