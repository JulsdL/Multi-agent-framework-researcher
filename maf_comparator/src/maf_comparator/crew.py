from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from maf_comparator.tools.custom_tool import MyCustomTool
# from maf_comparator.tools.docx_report_generator import DocxReportGenerator

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool, BaseTool

@CrewBase
class MafComparatorCrew():
    """MafComparator crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def criteria_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['criteria_developer'],
            verbose=True
        )

    @agent
    def researcher(self) -> Agent:
        # Example of using a custom search tool, like SerperDevTool for web searches
        # tools=[SerperDevTool()],
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True
        )

    @agent
    def analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['analyzer'],
            verbose=True
        )

    @agent
    def writer(self) -> Agent:
        # Assuming DocxReportGenerator is a custom tool for generating .docx reports
        # tools=[DocxReportGenerator()],
        return Agent(
            config=self.agents_config['writer'],
            verbose=True
        )

    @agent
    def qa_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_agent'],
            verbose=True
        )

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
        """Creates the MafComparator crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=2,
        )
