from agents import build_reader_agent , build_search_agent , writer_chain , critic_chain

def run_research_pipeline(topic : str, ui_callback=None) -> dict:
    state = {}

    #search agent working
    if ui_callback: ui_callback("search", "Search Agent is finding recent and reliable sources...")
    print("\n"+" ="*50)
    print("step 1 - Search Agent is working ....")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user" , f"Search for recent, reliable sources on : {topic}")
        ]
    })
    state["search_result"] = search_result['messages'][-1].content
    print("\n search result ",state['search_result'])

    #reader agent working
    if ui_callback: ui_callback("reader", "Reader Agent is scraping and reading the top resources...")
    print("\n"+ " ="*50)
    print("step 2 - Reader Agent is scrapung top resources .... ")
    print(" ="*50)
    
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages" : [("user",
        f"""
        Read and understand the following search results and provide:
        1. Cleaned raw notes and search results about '{topic}' strictly related to the topic and avoid unnecessary information.
        2. Bullet points of key insights and scrape it for deeper content.
        3. List of unique URLs to read

        Search Results:\n
        {state['search_result'][:800]}
        """)]
    })
    state["scraped_content"] = reader_result['messages'][-1].content
    print("\n scraped content ",state['scraped_content'])

    #writer agent working
    if ui_callback: ui_callback("writer", "Writer Agent is structuring and writing the comprehensive report...")
    print("\n"+ " ="*50)
    print("step 3 - Writer Agent is writing the article .... ")
    print(" ="*50)


    research_combined = (
        f"Search Results : \n {state['search_result']} \n\n"
        f"Detailed Scraped Content : \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })
    print("\n Final Report \n",state['report'])

    #critic report
    if ui_callback: ui_callback("critic", "Critic Agent is reviewing the report for quality and accuracy...")
    print("\n" + " ="*50)
    print("step 4 - Critic Agent is reviewing the report")
    print(" ="*50)

    state["feedback"] = critic_chain.invoke({
        "report" : state['report']
    })
    print("\n critic result \n",state["feedback"])

    if ui_callback: ui_callback("done", "Research pipeline completed successfully!")
    return state

    
if __name__ == "__main__":
    topic = input("\n Enter a research topic")
    run_research_pipeline(topic)

    
