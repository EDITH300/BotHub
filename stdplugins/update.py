"""Update UserBot code
Syntax: .update"""

from os import remove
from os import execl
import sys

import git
from git import Repo
from git.exc import GitCommandError
from git.exc import InvalidGitRepositoryError
from git.exc import NoSuchPathError

# from uniborg import CMD_HELP, bot
# from uniborg.events import register


import asyncio
import random
import re
import time

from collections import deque

import requests

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon import events

from uniborg.util import admin_cmd

# import git
from contextlib import suppress
import os
import sys
import asyncio

async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += f"•[{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n"
    return ch_log


async def is_off_br(br):
    off_br = ["master"]
    for k in off_br:
        if k == br:
            return 1
    return


@borg.on(admin_cmd("update ?(.*)", outgoing=True, allow_sudo=True))
async def upstream(ups):
    "For .update command, check if the bot is up to date, update if specified"
    await ups.edit("`Checking for updates, please wait....`")
    conf = ups.pattern_match.group(1)
    off_repo = "https://www.github.com/mkaraniya/bothub.got"

    try:
        txt = "`Oops.. Updater cannot continue due to some problems occured`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await ups.edit(f"{txt}\n`directory {error} is not found`")
        return
    except InvalidGitRepositoryError as error:
        await ups.edit(
            f"{txt}\n`directory {error} does not seems to be a git repository`"
        )
        return
    except GitCommandError as error:
        await ups.edit(f"{txt}\n`Early failure! {error}`")
        return

    ac_br = repo.active_branch.name
    if not await is_off_br(ac_br):
        await ups.edit(
            f"**[UPDATER]:**` Looks like you are using your own custom branch ({ac_br}). \
            in that case, Updater is unable to identify which branch is to be merged. \
            please checkout to any official branch`")
        return

    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")

    if not changelog:
        await ups.edit(f"\n`Your BOT is` **up-to-date** `with` **{ac_br}**\n")
        return

    if conf != "now":
        changelog_str = f"**New UPDATE available for [{ac_br}]:\n\nCHANGELOG:**\n`{changelog}`"
        if len(changelog_str) > 4096:
            await ups.edit("`Changelog is too big, sending it as a file.`")
            file = open("output.txt", "w+")
            file.write(changelog_str)
            file.close()
            await ups.client.send_file(
                ups.chat_id,
                "output.txt",
                reply_to=ups.id,
            )
            remove("output.txt")
        else:
            await ups.edit(changelog_str)
        await ups.respond(
            "`do \".update now\" to update\nDon't if using Heroku`")
        return

    await ups.edit("`New update found, updating...`")
    ups_rem.fetch(ac_br)
    repo.git.reset("--hard', 'FETCH_HEAD")
    await ups.edit("`Successfully Updated!\n"
                   "Bot is restarting... Wait for a second!`")
    await bot.disconnect()
    # Spin a new instance of bot
    execl(sys.executable, sys.executable, *sys.argv)
    # Shut the existing one down
    exit()




"""CMD_HELP.update({
    'update':
    ".update\
\nUsage: Checks if the main userbot repository has any updates and shows a changelog if so.\
\n\n.update now\
\nUsage: Updates your userbot, if there are any updates in the main userbot repository."
})
"""
