# autogen_multi_agent_marketing_team

> Still work in progress ...

## 📖 Overview
A multi-agent autonomous AI Marketing team that can work collaboratively &amp; autonomously to accomplish multiple tasks.

## 🕵🏽 Agents

The agents involved in the collaboration include:

- ***Content Team***
    - **Head of Content**: Oversees content creation and ensures alignment with marketing strategies.
    - **Content Creator**: Develops innovative content ideas and writes engaging blog posts, articles, and social media posts.
    - **Editor**: Edits written content for grammar, style, accuracy, and clarity.
    - **Designer**: Creates visually stunning posts, graphics and multimedia elements for marketing campaigns.
    - **Email Marketer**: Strategizes, designs, and executes effective email marketing campaigns.

- ***Market Research Team***
    - **Head of Market Research**: Leads the market research team in gathering insights into customer behavior, preferences, and industry trends.
    - **Market Researcher**: Conducts surveys, interviews, focus groups, and data analysis to uncover valuable information about target markets and competitors.
    - **SEO Specialist**:  Optimizes website content and meta tags to improve search engine rankings and online visibility.

## 🛠️ Tools Used

1. `Serper` for realtime web search
2. `Google ADs` for SEO-related information

## ⚙️ Setup & Configuration

1. Ensure required libraries are installed:
    ```
    pip install pyautogen
    ```

2. Set up the OpenAI configuration list by either providing an environment variable `OAI_CONFIG_LIST` or specifying a file path.
    ```
    [
        {
            "model": "gpt-3.5-turbo", #or whatever model you prefer
            "api_key": "INSERT_HERE"
        }
    ]
    ```

3. Setup api keys in .env:
```
OPENAI_API_KEY="XXX"
SERPAPI_API_KEY="XXX"
SERPER_API_KEY="XXX"
```

4. Launch in CLI:
```
streamlit run Home.py
```