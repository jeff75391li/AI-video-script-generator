from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper


def generate_video_script(subject, video_duration, creativity, api_key):
    """Generates a video script based on the subject and duration by calling OpenAI Chat model.

            Parameters
            ----------
            subject : str
                The video subject
            video_duration : float
                The video duration
            creativity : float
                How creative the model will be
            api_key : str
                OpenAI API key
    """

    # prompt template for generating video titles
    title_template = ChatPromptTemplate.from_messages(
        [
            ("human", "Please generate an engaging video title related to '{subject}'")
        ]
    )

    # prompt template for generating video scripts
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """You are a content creator and make the best videos.
             Please write a great video script based on the following information:
             Video title: {title}; video length: {duration} minutes. Length of the script
             should match the provided video length. The script intro should be
             captivating enough to draw readers attention. The main body of the script should
             provide useful details of the subject. The script outro should surprise
             the readers. The format of the script is in the form of [intro, main body, outro].
             The script should be fun and easy to understand for most people.
             You may refer to the following information from Wikipedia search. It is just for your reference
             so please ignore any unrelated contents:
             ```{wikipedia_search}```""")
        ]
    )

    model = ChatOpenAI(openai_api_key=api_key, temperature=creativity)
    title_chain = title_template | model
    script_chain = script_template | model

    # Get a good title from the model
    title = title_chain.invoke({"subject": subject}).content

    # Set up Wikipedia API to search for the topic
    wikipedia = WikipediaAPIWrapper()
    search_result = wikipedia.run(subject)

    # Get a video script based on the generated title and the search result from Wikipedia.
    script = script_chain.invoke({"title": title, "duration": video_duration,
                                  "wikipedia_search": search_result}).content

    return title, script, search_result
