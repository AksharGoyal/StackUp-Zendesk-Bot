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
- MongoDB Atlas Account
- Bot Token (https://discord.com/developers/applications)
- Llama API (https://www.llama-api.com/)

When inviting the bot to your server you admin, make sure the invite URL looks similar to below. You can find the Client ID in the OAuth2 section of your [Application's Homepage](https://discord.com/developers/applications/).
```
https://discord.com/oauth2/authorize?client_id=<CLIENT_ID>&permissions=551903300608&integration_type=0&scope=applications.commands+bot
```
<img width="500" alt="image" src="https://github.com/user-attachments/assets/d2d5c262-9da6-4730-8386-4709ddf63f8a">

## Instructions
1. Clone the repo
```sh
git clone https://github.com/AksharGoyal/StackUp-Zendesk-Bot.git
cd StackUp-Zendesk-Bot
```
2. Create a virtual environment using conda. You can give any name to your environment; I have used "bot" here that will run on Python version 3.9.
```sh
conda create --env bot python=3.9
```
3. Install the necessary libraries.
```sh
pip install -r requirements.txt
```
4. Populate the .env file (make sure the .env.template is changed to .env)  
<img width="650" alt="image" src="https://github.com/user-attachments/assets/bbbe3c16-8bde-4884-9e81-63fc5273bf8a">

5. To generate the necessary inputs for our LLM, run the following command:
```sh
python data_scraper.py
```

6. Run all the cells in `generate_embeddings.ipynb` to store the vector embeddings of the data in MongoDB. The Demonstration part is optional but make sure to create the search index as the bot will need it.
7. Finally, run the following command:
```
python bot.py
```  
While the bot is running in your terminal, go to your discord server and type `/ask`. You will observe that the `ask` command pops up as part of your application's command.  

<img width="600" alt="image" src="https://github.com/user-attachments/assets/2316cc37-f6af-4160-8e72-83bf76f1fc65">  

The command takes a user query as input. Note that it's important the user query is related to StackUp, especially based on its Zendesk's articles. Here are some examples of how the bot would work with user queries:  

<img width="350" alt="image" src="https://github.com/user-attachments/assets/1f51262c-5f5e-4faa-b710-ec21083ef6b4">  

