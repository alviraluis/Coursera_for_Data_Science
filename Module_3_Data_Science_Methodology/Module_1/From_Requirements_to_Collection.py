try:
    from pyodide.http import pyfetch
except ImportError:
    raise RuntimeError("This script must be run in a Pyodide environment.")

import pandas as pd  # Ensure pandas is installed in your environment
pd.set_option('display.max_columns', None)

async def main():
    async def download(url, filename):
        response = await pyfetch(url)
        if response.status == 200:
            with open(filename, "wb") as f:
                f.write(await response.bytes())

    path = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0103EN-SkillsNetwork/labs/Module%202/recipes.csv"
    # Download the dataset
    await download(path, "recipes.csv")

    # Load the dataset
    recipes = pd.read_csv("recipes.csv")
    print(recipes.head())

# Run the async function
import asyncio
asyncio.run(main())