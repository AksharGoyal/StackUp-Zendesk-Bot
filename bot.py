"""
Provides a Discord bot that uses the LlamaIndex library to provide a question-answering interface for users.
The bot has the following functionality:
- Connects to a Discord server using the discord.py library and the provided bot token.
- Handles events such as when a new member joins the server and sends them a welcome message.
- Provides a `!hello` command that allows users to greet other users.
- Provides a `/ask` slash command that allows users to ask questions,
    which the bot will attempt to answer using the LlamaIndex library and data stored in a MongoDB Atlas database.
    
The bot uses the LlamaIndex library to create a vector store index from data stored in a MongoDB Atlas database,
and uses this index to provide responses to user queries.
The bot also uses the discord.py library's pagination features to display long responses in a paginated format.
"""

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv, find_dotenv, dotenv_values
from discord.ext.pages import Paginator, Page, PaginatorButton
import warnings
warnings.filterwarnings(action='ignore')
from datetime import datetime

import pymongo
from llama_index.llms.llama_api import LlamaAPI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import ServiceContext, StorageContext, VectorStoreIndex
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch

config = dotenv_values(find_dotenv())

embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")
LLAMA_API = config.get('LLAMA_API')
llm = LlamaAPI(api_key=LLAMA_API)
service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm)

DB_NAME = 'stackup_ai'
COLLECTION_NAME = 'zendesk_data'
INDEX_NAME = 'index_embeddings'

ATLAS_URI = config.get('ATLAS_URI')
mongodb_client = pymongo.MongoClient(ATLAS_URI)

vector_store = MongoDBAtlasVectorSearch(mongodb_client = mongodb_client,
                                 db_name = DB_NAME, collection_name = COLLECTION_NAME,
                                 vector_index_name  = INDEX_NAME,
                                 )

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store, service_context=service_context)

TOKEN = config.get('TOKEN')

intents = discord.Intents.all()
intents.messages = True
intents.message_content = True 

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents, description="None for now")

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.event
async def on_member_join(member):
    await member.send(
        f'Welcome to the server, {member.mention}! Enjoy your stay here.'
    )
    
@bot.command(name="hello", aliases=["hi"], description="Say hello")
async def hello(ctx, user: str = None):
    if user:
        await ctx.reply(f"{ctx.author.mention} says hello to {user}!")
    else:
        await ctx.reply(f"{ctx.author.name}, you forgot to mention someone! Usage:`!hello @user`")
    
@bot.slash_command(name = "hello", description = "A command to greet someone")
async def hello(ctx, user: str = ''):
    if user:
        await ctx.respond(f"{ctx.author.mention} says hello to {user}!")
    else:
        await ctx.respond(f"{ctx.author.name}, you forgot to mention someone! Usage:`!hello @user`")

    
@bot.slash_command(name = "ask", description = "A command to ask the chatbot questions")
async def ask(ctx, user_query = ''):
    if not user_query:
        page = Page(embeds=[discord.Embed(title="Help Embed", timestamp = datetime.now(),
                                        description=f"Hey {ctx.author.mention}! Feel free to ask me anything about StackUp!\n I am still learning so will do my best to respond as accurate as possible!")])
        paginator = Paginator([page], use_default_buttons=False)
        await paginator.respond(ctx.interaction)
    else:
        await ctx.defer()
        response = index.as_query_engine().query(user_query)
        my_pages = []
        limit = 4000
        i = 0
        response_str = response.response[i*limit : (i+1)*limit]
        while len(response_str) > 0:
            my_pages.append(Page(embeds=[discord.Embed(title=user_query[:50], description=response_str)]))
            i += 1
            response_str = response.response[i*limit : (i+1)*limit]
            
        buttons = [
            PaginatorButton("first", label="<<-", style=discord.ButtonStyle.green),
            PaginatorButton("prev", label="<-", style=discord.ButtonStyle.green),
            PaginatorButton("page_indicator", style=discord.ButtonStyle.gray, disabled=True),
            PaginatorButton("next", label="->", style=discord.ButtonStyle.green),
            PaginatorButton("last", label="->>", style=discord.ButtonStyle.green),
        ]
        paginator = Paginator(my_pages, timeout=3000, use_default_buttons=False, custom_buttons=buttons)
        await paginator.respond(ctx.interaction)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command.")

bot.run(TOKEN)
