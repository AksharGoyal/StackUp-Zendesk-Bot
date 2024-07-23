# StackUp Zendesk Bot  

## Acknowledgement
Firstly, I would like to thank the StackUp team for choosing me as a Beta Tester for their upcoming Hackathon App. This opportunity allowed me to give back to the community which has always encouraged me to step out of my comfort zone and view learning as a rewarding experience.

## Introduction

I found the motivation to build this bot when I saw discord user crackie_0000's [chatbot](https://github.com/dsa012/StackUpChatBot/blob/main/README.md) that feeds on Zendesk articles and responds to users' queries. As someone who enjoys using Discord and has participated in the campaign [Innovating with MongoDB Atlas Vector Search](https://earn.stackup.dev/campaigns/innovating-with-mongodb-atlas-vector-search), I decided to build a Discord bot version of his chatbot. Special thanks to "Kradian" for helping in building and testing the bot.

The repo contains code for building a discord chatbot that uses StackUp's Zendesk articles to retrieve information and answer a user's query. The bot uses LLMs (Llama AI) and vector embeddings stored in Atlas MongoDB to search for the closest information relevant to the query and responds through Discord's Embeds.  

At the moment, the bot isn't hosted unfortunately so you may have to test it locally. I will try to explain the steps in as much detail as needed to run on your side.

## Requirements
- Python 3.9 or higher
- Anaconda for virtual environment
- Bot Token (https://discord.com/developers/applications)
- Llama API (https://www.llama-api.com/)

## Instructions
1. Clone the repo
