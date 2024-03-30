import os
from langchain_openai import ChatOpenAI
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from .tools.custom_tool import DocxReportGenerator
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv('SERPER_API_KEY')


@CrewBase
class MafComparatorCrew():
    """MafComparator crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        self.serper_dev_tool = SerperDevTool()
        self.scrape_website_tool = ScrapeWebsiteTool()
        self.docx_report_generator = DocxReportGenerator()

    @agent
    def criteria_developer(self) -> Agent:
        # No external tools required for criteria development
        return Agent(
            config=self.agents_config['criteria_developer'],
            tools=[self.serper_dev_tool, self.scrape_website_tool],
            verbose=True,
            max_iter=2
        )

    @agent
    def researcher(self) -> Agent:
        # Using SerperDevTool and ScrapeWebsiteTool for web searches and scraping
        return Agent(
            config=self.agents_config['researcher'],
            tools=[self.serper_dev_tool, self.scrape_website_tool],
            verbose=True,
            max_iter=3
        )

    @agent
    def analyzer(self) -> Agent:
        # Analysis may not require specific tools beyond internal logic
        return Agent(
            config=self.agents_config['analyzer'],
            verbose=True,
            max_iter=2
        )

    @agent
    def writer(self) -> Agent:
        # Configuring DocxReportGenerator for generating .docx reports
        return Agent(
            config=self.agents_config['writer'],
            tools=[self.docx_report_generator],
            verbose=True,
            max_iter=2
        )

    @agent
    def qa_agent(self) -> Agent:
        # QA process might be primarily manual; no specific tools added
        return Agent(
            config=self.agents_config['qa_agent'],
            verbose=True,
            max_iter=2
        )

    # Define tasks here using @task decorator

    @task
    def criteria_development_task(self) -> Task:
        return Task(
            config=self.tasks_config['criteria_development_task'],
            agent=self.criteria_developer()
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.researcher()
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task'],
            agent=self.analyzer()
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task'],
            agent=self.writer(),
            output_file='comparison_report.docx'
        )

    @task
    def quality_assurance_task(self) -> Task:
        return Task(
            config=self.tasks_config['quality_assurance_task'],
            agent=self.qa_agent()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MafComparator crew with a hierarchical process."""


        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            manager_llm=ChatOpenAI(temperature=0, model="gpt-4"),
            process=Process.hierarchical,
            verbose=2,
        )
