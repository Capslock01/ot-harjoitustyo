from datetime import timedelta
import re

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from entities.project import Project
from database.database import Base, ENGINE, Projects, ProjectData


class ProjectRepository:
    """Class that handles creating and saving new projects."""

    def __init__(self) -> None:
        """Class constructor."""

        self._projects = []

        # Create database if it doesn't exist
        Base.metadata.create_all(ENGINE)

        # Get active projects from database
        with Session(ENGINE) as session:
            selection = select(Projects).\
                where(Projects.active == 1)
            for project in session.scalars(selection):
                self._projects.append(Project(project.name, project.id))
            session.commit()

    def valid_name(self, name: str) -> bool:
        """Check for project with given name.

        Args:
            name: Name to validate.

        Returns:
            True if name is valid, else False.
        """

        sieve = re.compile('^[a-öA-Ö0-9]+$') # Match any single word
        if sieve.match(name) is None:
            return False
        for project in self._projects:
            if project.name.lower() == name.lower():
                return False
        return True

    def get_projects(self) -> list:
        """Method to aquire self._projects from outside the class.

        Returns:
            self._projects: List of all active projects
        """

        return self._projects

    def _query_all_projects(self) -> list:
        """Query all active and not active projects from database.

        Returns:
            all_projects: All projects in database
        """

        all_projects = []
        with Session(ENGINE) as session:
            selection = select(Projects)
            for project in session.scalars(selection):
                all_projects.append(Project(project.name, project.id))
            session.commit()
        return all_projects

    def add_project(self, name: str) -> bool:
        """Add new project.

        Args:
            name: Name of the project to be added.

        Returns:
            True if adding successful, else False.
        """

        if not self.valid_name(name):
            return 0

        # Check if same name project is in active projects
        for project in self.get_projects():
            if name.lower() == project.name.lower():
                return 0

        # Check if same name project is deactivated
        all_projects = self._query_all_projects()
        for project in all_projects:
            # Check for deactivated (deleted) projects to reactivate
            if project.name.lower() == name.lower():
                # Set active column to True
                with Session(ENGINE) as session:
                    re_activate = update(Projects).\
                        where(Projects.name == project.name).\
                        values(active = True).\
                        execution_options(synchronize_session = 'fetch')
                    session.execute(re_activate)

                    # Get reactivated project to projectrepo
                    selection = select(Projects).\
                        where(Projects.name.in_([name]))
                    for result in session.scalars(selection):
                        self._projects.append(Project(result.name, result.id))
                    session.commit()
                return 1

        # Create new project
        with Session(ENGINE) as session:
            session.add_all([Projects(name = name, active = True)])
            session.commit()
            selection = select(Projects).where(Projects.name.in_([name]))
            for project in session.scalars(selection):
                self._projects.append(Project(project.name, project.id))
            session.commit()
        return 2

    def delete_project(self, name: str) -> bool:
        """Delete project with given name from repo.

        Does not delete from database, sets the project inactive.

        Args:
            name: name of the project to be deleted.

        Returns:
            True if project is successfully deleted, else False.
        """

        for project in self._projects:
            if project.name == name:
                self._projects.remove(project)
                with Session(ENGINE) as session:
                    deactivate = update(Projects).\
                        where(Projects.name == name).\
                        values(active = False).\
                        execution_options(synchronize_session = 'fetch')
                    session.execute(deactivate)
                    session.commit()
                return True
        return False

    def get_stats(self, timestr: str) -> str:
        """Return stats for given timestr as a string.

        Args:
            timestr: time string to filter query results.

        Returns:
            text: string to be displayed in GUI.
        """

        projects_with_times = {}    # Save name and total time here
        all_projects = self._query_all_projects()

        with Session(ENGINE) as session:
            for project in all_projects:
                selection = select(func.sum(ProjectData.time)).\
                    where(ProjectData.project_id == project.id_).\
                    where(ProjectData.date.startswith(timestr))
                # Must iterate to get data as an integer
                for data in session.scalars(selection):
                    if data is None:
                        data = 0
                    if data > 0:
                        projects_with_times[project.name] = str(timedelta(seconds = data))
            session.commit()
        if timestr == '':
            text = ' Projektien kokonaisajat kaikista\n tallennetuista ajoista:\n\n'
        else:
            text = f' Projektien kokonaisajat ajanjaksolta {timestr}:\n\n'

        for key, value in projects_with_times.items():
            key = key + ':'
            text += f' {key:<18}{value}\n'
        return text

    def print_projects(self) -> None:
        for project in self._projects:
            print(project.name, project.timer)


projectrepo = ProjectRepository()
