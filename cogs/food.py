import discord
from discord.ext import commands
import aiohttp
import random
import asyncio
import ujson

class Food(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["fp"])
    async def foodporn(self, ctx):
        """Get a random r/FoodPorn Image"""
        client_id = await self.bot.db.fetchval("SELECT imgur_id FROM keys")
        headers = {"Authorization" : "Client-ID "+ client_id}
        async with self.bot.session.get("https://api.imgur.com/3/gallery/r/foodporn/", headers=headers) as d:
            j = await d.json(loads=ujson.loads)
        x = random.choice(j["data"])
        url = x["link"]
        name = x["title"]
        blue = discord.Color.blue()
        e = discord.Embed(title = "Food Porn", description = name, url = url, color = blue)
        e.set_image(url=url)
        e.set_footer(text="Requested by "+ ctx.author.name, icon_url=ctx.author.avatar_url)
        message = await ctx.send(embed=e)
        emojis = ("\U000025b6","\U000023f9")
        def check(reaction,user):
            return user == ctx.author and str(reaction.emoji) in emojis and reaction.message.id == message.id
        for emoji in emojis:
            await message.add_reaction(emoji)
        while True:
            try:
                r, u = await self.bot.wait_for("reaction_add",check=check, timeout=60)
            except asyncio.TimeoutError:
                for emoji in emojis:
                    await message.remove_reaction(emoji, ctx.me)
                return
            else:
                try:
                    await message.remove_reaction(r,u)
                except:
                    pass
                if str(r.emoji) == "\U000023f9":
                    return await message.delete()
                else:
                    x = random.choice(j["data"])
            url = x["link"]
            name = x["title"]
            blue = discord.Color.blue()
            e = discord.Embed(title = "Food Porn", description = name, url = url, color = blue)
            e.set_image(url=url)
            e.set_footer(text="Requested by "+ ctx.author.name, icon_url=ctx.author.avatar_url)
            await message.edit(embed=e)

    @commands.command(aliases = ["sfp"])
    async def shittyfoodporn(self, ctx):
        """Get a random r/ShittyFoodPorn Image"""
        client_id = await self.bot.db.fetchval("SELECT imgur_id FROM keys")
        headers = {"Authorization" : "Client-ID "+ client_id}
        async with self.bot.session.get("https://api.imgur.com/3/gallery/r/shittyfoodporn/", headers=headers) as d:
            j = await d.json(loads=ujson.loads)
        x = random.choice(j["data"])
        url = x["link"]
        name = x["title"]
        blue = discord.Color.blue()
        e = discord.Embed(title = "Shitty Food Porn", description = name, url = url, color = blue)
        e.set_image(url=url)
        e.set_footer(text="Requested by "+ ctx.author.name, icon_url=ctx.author.avatar_url)
        message = await ctx.send(embed=e)
        emojis = ("\U000025b6","\U000023f9")
        def check(reaction,user):
            return user == ctx.author and str(reaction.emoji) in emojis and reaction.message.id == message.id
        for emoji in emojis:
            await message.add_reaction(emoji)
        while True:
            try:
                r, u = await self.bot.wait_for("reaction_add",check=check, timeout=60)
            except asyncio.TimeoutError:
                for emoji in emojis:
                    await message.remove_reaction(emoji, ctx.me)
                return
            else:
                try:
                    await message.remove_reaction(r,u)
                except:
                    pass
                if str(r.emoji) == "\U000023f9":
                    return await message.delete()
                else:
                    x = random.choice(j["data"])
            url = x["link"]
            name = x["title"]
            blue = discord.Color.blue()
            e = discord.Embed(title = "Shitty Food Porn", description = name, url = url, color = blue)
            e.set_image(url=url)
            e.set_footer(text="Requested by "+ ctx.author.name, icon_url=ctx.author.avatar_url)
            await message.edit(embed=e)

    @commands.command(aliases = ["fs","foodsearch","nutrition", "search"])
    async def food(self, ctx, *, search):
        """Gives nutritional value of the food you search foor (Make sure to include amount)"""
        data = await self.bot.db.fetchrow("SELECT * FROM keys")
        app_ids = data['food_ids']
        app_keys = data['food_keys']
        f = False
        c = 0
        while not f:
            try:
                app_id = app_ids[c]
                app_key = app_keys[c]
            except:
                return await ctx.send("Ratelimited, try again in one minute.")
            else:
                async with self.bot.session.get("https://api.edamam.com/api/nutrition-data?ingr="+search+"&app_id="+app_id+"&app_key="+app_key) as r:
                    try:
                        t = await r.json(loads=ujson.loads)
                    except:
                        c+=1
                    else:
                        f = True
        url = t.get("uri")
        diet = t.get("dietLabels")
        health = t.get("healthLabels")
        calories = t.get("calories")
        cautions = t.get("cautions")
        n = t.get("totalNutrients")
        nuts = list()
        for x in n:
            e = n.get(x)
            if int(e.get("quantity")):
                nuts.append(e.get("label") + " - " + str(int(e.get("quantity"))) + e.get("unit") + "\n")
        nutrients = " - " + " - ".join(nuts)
        d = ", ".join(health) + ", " + ", ".join(diet) if diet else ", ".join(health)
        c = ", ".join(cautions)
        blue = discord.Color.blue()
        e = discord.Embed(title="Nutrition Facts",description = search.title(), url = url, color = blue)
        if not calories or not nutrients:
            return await ctx.send("Please use a valid food and specify a valid amount. `Example: food!food 1 cup of peanut butter`")
        e.add_field(name= "Calories",value = calories)
        if d:
            e.add_field(name="Diet and Health Labels", value = d)
        if c:
            e.add_field(name="Cautions", value = c)
        e.add_field(name ="Nutrients",value = nutrients, inline = False)
        e.set_footer(text="Requested by "+ ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=e)

    @commands.command()
    async def cocktail(self, ctx, *, search=None):
        '''Sends Instructions on how to make the cocktail specified in the given search'''
        if search is None:
            async with self.bot.session.get('https://www.thecocktaildb.com/api/json/v1/1/random.php') as r:
                data = await r.json(loads=ujson.loads)
        else:
            search = search.replace(' ', '%20')
            async with self.bot.session.get('https://www.thecocktaildb.com/api/json/v1/1/search.php?s='+search) as r:
                data = await r.json(loads=ujson.loads)
        try:
            drink = data['drinks'][0]
            name = drink['strDrink']
            image = drink['strDrinkThumb']
            glass = drink['strGlass']
            instructions = drink['strInstructions']
            alcoholic = drink['strAlcoholic']
            ingredients = list()
            for i in range(1, 15):
                if drink['strMeasure'+str(i)] is not None:
                    if drink['strMeasure'+str(i)].strip():
                        ingredient = drink['strMeasure'+str(i)] + 'of ' + drink['strIngredient' + str(i)]
                        ingredients.append(ingredient)
                elif drink['strIngredient'+str(i)] is not None:
                    if drink['strIngredient'+str(i)].strip():
                        ingredient = drink['strIngredient' + str(i)]
                        ingredients.append(ingredient)
            ings = '-' + '\n-'.join(ingredients)
        except (ValueError, TypeError):
            return await ctx.send('This drink was not found.')
        green = discord.Color.green()
        em = discord.Embed(title=name, description=alcoholic, color=green)
        em.set_image(url=image)
        em.add_field(name='Glass to Use', value=glass, inline=False)
        em.add_field(name='Ingredients', value=ings, inline=False)
        em.add_field(name='Instructions', value=instructions, inline=False)
        await ctx.send(embed=em)

    @commands.command(aliases=["detect", "clarifai"])
    async def ai(self, ctx, url=None):
        '''Detects what food is in the image from the url or the first attachment'''
        if not url:
            try:
                url = ctx.message.attachments[0].proxy_url
            except:
                return await ctx.send("You didn't send an attachment or a url.")
        key = await self.bot.db.fetchval("SELECT clarifai FROM keys")
        headers = {"Content-Type": "application/json", "Authorization": "Key "+key}
        data = {
            "inputs": [
                {
                    "data": {
                        "image": {
                            "url": url
                        }
                    }
                }
            ]
        }
        async with self.bot.session.post("https://api.clarifai.com/v2/models/bd367be194cf45149e75f01d59f77ba7/outputs", json=data, headers=headers) as r:
            response = await r.json()
        try:
            concepts = " - " + "\n - ".join([concept["name"] + ": " + str(concept["value"])[:4] for concept in response["outputs"][0]["data"]["concepts"]])
        except:
            return await ctx.send("There was an error detecting food in your image.")
        await ctx.send("I think these are in your image:\n"+concepts)

def setup(bot):
    bot.add_cog(Food(bot))
