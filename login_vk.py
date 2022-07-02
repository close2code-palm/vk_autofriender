import asyncio
from typing import List

from environs import Env
from playwright.async_api import async_playwright, Locator

env = Env()
env.read_env()

friend_limit = 50


async def add_friends_with_acc():
    """Enter VK page with creds from .env file
    and extends friendlist by sending up to limit"""
    # context dependence, so here we use single function
    # solution 1 pass the context
    # solution 2 grab once and then reuse cookies
    async with async_playwright() as a_p:
        browser = await a_p.firefox.launch(headless=True)
        page = await browser.new_page()
        # login
        await page.goto('https://vk.com')
        await page.locator('button.VkIdForm__signInButton').click()

        async def submit():
            """Presses the submit button when data entered"""
            await page.locator('button.vkc__Button__primary').click()

        login_name = env.str('VK_LOGIN')
        await page.locator('input.vkc__TextField__input').fill(login_name)
        await submit()
        password = env.str('VK_PASS')
        await page.locator('input[name="password"]').fill(password)
        await submit()
        await asyncio.sleep(5)
        # add friends
        await page.goto('https://vk.com/friends?act=find')
        friend_link_sel = 'a.friends_find_user_add'
        while await page.locator(friend_link_sel).count() < friend_limit:
            await page.locator(friend_link_sel).last.scroll_into_view_if_needed()
        for l_i in range(friend_limit):
            await page.locator(friend_link_sel).nth(l_i).click()
            print(f'User`s {l_i + 1} friendship requested.')
            await asyncio.sleep(7)

# creates the loop and executes the function
asyncio.run(add_friends_with_acc())
