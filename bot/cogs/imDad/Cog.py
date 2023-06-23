"""
This Cog contains a feature which allows the bot to respond with I'm Dad when someone says "I'm"
"""

import json
import os

import discord
import requests
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

PROGRAM_PATH = "/".join(__file__.split("/")[:-1]) + "/"
DOTENV_PATH = "/".join(__file__.split("/")[:-3]) + "/.env"
load_dotenv(DOTENV_PATH)
GUILD_ID = os.getenv("GUILD_ID")
GUILD = discord.Object(GUILD_ID)
OWNER_ID = int(os.getenv("OWNER_ID"))

blacklisted_users_str: str = os.getenv("BLACKLISTED_USERS")
BLACKLISTED_USERS = json.loads(blacklisted_users_str)

imdad_spam_users_str: str = os.getenv("IMDAD_SPAM_USERS")
IMDAD_SPAM_USERS = json.loads(imdad_spam_users_str)

imdad_excluded_channels_str: str = os.getenv("IMDAD_EXCLUDED_CHANNELS")
IMDAD_EXCLUDED_CHANNELS = json.loads(imdad_excluded_channels_str)


class ImDadCog(commands.Cog):
    """
    This Cog contains a feature which allows the bot to respond with I'm Dad when someone says "I'm"
    """

    def __init__(self, client: commands.Bot):
        self.bot = client
        self._opt_outs = []
        # load the opt-outs from the file
        with open(PROGRAM_PATH + "opt_outs.json", "r") as file:
            self._opt_outs = json.load(file)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        This function is called whenever a message is sent in a channel that the bot can see
        :param message: the message that was sent
        :return: None
        """
        # code hashed out as it is for testing purposes
        # TESTING_CHANNEL_ID = 42
        # if message.channel.id != TESTING_CHANNEL_ID:
        #     return
        # if message.author.id != OWNER_ID:
        #     return

        # conditions to ignore the message
        if message.author == self.bot.user:
            return
        if message.author.bot:
            return
        if message.author.id in self._opt_outs:
            return
        if message.author.id in BLACKLISTED_USERS:
            return
        if message.channel.id in IMDAD_EXCLUDED_CHANNELS:
            return

        # gets the content of the message
        message_content = message.content
        # filters out profanity
        url = 'http://profanityfilter:6969/service'
        data = {'data': message_content}
        response = requests.post(url, json=data)

        if response.status_code != 200:
            return
        message_content = response.text
        # condition is put in place to ignore messages that are too long otherwise it could be abused
        if len(message_content) > 250:
            return

        # this is to prevent the bot from pinging everyone
        message_content = message_content.replace("@", "\\@")
        message_content = message_content.replace("everyone", "eVeRyOnE")
        message_content = message_content.replace("here", "hErE")

        # code hashed out as it is for testing purposes
        # print("========================================\n"
        #       f"Message from: {message.author.name}#{message.author.discriminator} ({message.author.id})\n"
        #       f"Message content: {message.content}\n"
        #       f"Message content after filtering: {message_content}\n"
        #       f"Message content length: {len(message.content)}")

        # used to simplify the code
        message_content_lower = message_content.lower()
        # if the message contains the word "I'm" or "Im" or "i'm" or "im"
        sent_message_count = 0
        max_sent_message_count = 1 if message.author.id in IMDAD_SPAM_USERS else 4
        if "i'm " in message_content_lower or "im " in message_content_lower:
            message_content_split = message_content.split(" ")
            # find the index of the word "I'm" or "Im" or "i'm" or "im"
            for index, word in enumerate(message_content_split):
                # if the word is "I'm" or "Im" or "i'm" or "im" and it is not the last word in the message
                if word.lower() in ["i'm", "im"] and index != len(message_content_split) - 1:
                    # get the next words in the message
                    next_words = message_content_split[index + 1:]
                    # send a message to the channel that the message was sent in
                    if sent_message_count < max_sent_message_count:
                        await message.channel.send(f"Hi {' '.join(next_words)}, I'm Dad!")
                        sent_message_count += 1
                    else:
                        return

    @app_commands.command(name="imdadoptout", description="Opt out of the \"Hi I'm Dad\" feature")
    async def opt_out(self, interaction: discord.InteractionMessage):
        """
        This function is called whenever someone uses the slash command to opt out of the "hi im dad" feature
        :param interaction: the interaction that was made
        :return: None
        """
        # if the user is not in the opt-outs list
        if interaction.user.id not in self._opt_outs:
            # add the user to the opt-outs list
            self._opt_outs.append(interaction.user.id)
            # send a message to the user
            await interaction.response.send_message("You have opted out of the \"Hi I'm Dad\" feature", ephemeral=True)
        else:
            # send a message to the user
            await interaction.response.send_message("You have already opted out of the \"Hi I'm Dad\" feature",
                                                    ephemeral=True)

        # save the opt-outs list to the file
        with open(PROGRAM_PATH + "opt_outs.json", "w") as file:
            json.dump(self._opt_outs, file)

    @app_commands.command(name="imdadoptin", description="Opt in to the \"Hi I'm Dad\" feature")
    async def opt_in(self, interaction: discord.InteractionMessage):
        """
        This function is called whenever someone uses the slash command to opt in to the "hi im dad" feature
        :param interaction: the interaction that was made
        :return: None        
        """
        # if the user is in the opt-outs list
        if interaction.user.id in self._opt_outs:
            # remove the user from the opt-outs list
            self._opt_outs.remove(interaction.user.id)
            # send a message to the user
            await interaction.response.send_message("You have opted in to the \"Hi I'm Dad\" feature", ephemeral=True)
        else:
            # send a message to the user
            await interaction.response.send_message("You have already opted in to the \"Hi I'm Dad\" feature",
                                                    ephemeral=True)

        # save the opt-outs list to the file
        with open(PROGRAM_PATH + "opt_outs.json", "w") as file:
            json.dump(self._opt_outs, file)

    @app_commands.command(name="imdadoptstatus",
                          description="Tells you if you have opted out of the \"Hi I'm Dad\" feature")
    async def status(self, interaction: discord.InteractionMessage):
        """
        This function is called whenever someone uses the slash command to check if they have opted out of the "hi im dad" feature
        :param interaction: the interaction that was made
        :return: None
        """
        # if the user is in the opt-outs list
        if interaction.user.id in self._opt_outs:
            # send a message to the user
            await interaction.response.send_message("You have opted out of the \"Hi I'm Dad\" feature", ephemeral=True)
        else:
            # send a message to the user
            await interaction.response.send_message("You have not opted out of the \"Hi I'm Dad\" feature",
                                                    ephemeral=True)

    @app_commands.command(name="imdadoptouts",
                          description="Get a list of the users who have opted out of the \"Hi I'm Dad\" feature")
    async def opt_outs(self, interaction: discord.InteractionMessage):
        """
        This function is called whenever someone uses the slash command to get a list of the users who have opted out of
        the "hi im dad" feature. This command can only be used by the owner of the bot
        :param interaction: 
        :return: 
        """
        # if the user is the owner of the bot
        if interaction.user.id == OWNER_ID:
            # send a message to the user
            embed = discord.Embed(title="Opt Outs",
                                  description="Users who have opted out of the \"Hi I'm Dad\" feature")
            for user_id in self._opt_outs:
                user = self.bot.get_user(user_id)
                embed.add_field(name=user.name, value=user_id)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            # send a message to the user
            await interaction.response.send_message("You do not have permission to use this command", ephemeral=True)


async def setup(client: commands.Bot) -> None:
    """ Set up the cog """
    await client.add_cog(ImDadCog(client), guild=GUILD)
