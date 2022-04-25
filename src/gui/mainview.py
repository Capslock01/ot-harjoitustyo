import tkinter as tk
from tkinter import ttk, constants, Grid

from services.project_service import project_service


class MainView:
    """Class for main window."""

    def __init__(self, root) -> None:
        self._root = root
        self._frame = None
        self._widgets = []  # storing text widgets for update function
        self._controllers = []
        self._start()

    def pack(self) -> None:
        """Pack self._frame."""

        self._frame.pack(fill = constants.BOTH)

    def update(self, width) -> None:

        size = int(width*0.01)
        # style = ttk.Style()
        # style.theme_use('default')
        # style.map('TreeView')
        # style.configure('Treeview.Heading', font = ('Arial', size))
        # style.configure('Label', font = ('Arial', size))
        for widget in self._widgets:
            widget.config(font = ('Arial', size))

    def _start(self) -> None:
        """Initialize view layout."""

        self._frame = tk.Frame(
            master = self._root,
            background = 'black'
        )
        Grid.rowconfigure(self._root, 0, weight = 1)
        Grid.columnconfigure(self._root, 1, weight = 2, minsize = 200)
        Grid.columnconfigure(self._root, 0, weight = 5)

        left_frame = tk.Frame(self._root, bg='white')
        right_frame = tk.Frame(self._root, bg='white')
        left_frame.grid(row = 0, column = 0, sticky = 'nsew')
        right_frame.grid(row = 0, column = 1, sticky = 'nsew')

        # make custom class instead of Treeview


        # New project creation area
        new_project_label = ttk.Label(right_frame, text = 'Luo uusi projekti', font = ('Arial', 18))
        new_project_label.grid(row = 0, column = 0, pady = 20, padx = 20, sticky = 'n')

        project_name_label = ttk.Label(right_frame, text = 'Projektin nimi:', font = ('Arial', 12))
        project_name = ttk.Entry(right_frame)
        project_name_label.grid(row = 1, column = 0, pady = 10, padx = 10, sticky = 'nsew')
        project_name.grid(row = 2, column = 0, pady = 10, padx = 10, sticky = 'nsew')

        create_project = ttk.Button(
            right_frame,
            command = lambda:[project_service.add_project(project_name.get()),
            project_name.delete(0, 'end'),
            project_service.print_data()],
            text = 'Lisää projekti'
        )
        create_project.grid(row = 3, column = 0, pady = 10, padx = 10, sticky =' new')

        Grid.columnconfigure(right_frame, 0, weight = 1)

    def _create_project_controllers(self) -> None:
        """Get projects from repo and create ProjectControllers for them."""

        for i, project in enumerate(project_service.default_repo):
            controller = ProjectController(self._frame, project)
            controller.grid(i)

    def destroy(self) -> None:
        self._frame.destroy()


class ProjectController:
    """GUI class to control project timers."""

    def __init__(self, root, project) -> None:
        self._root = root
        self._project = project
        self._frame = tk.Frame(
            master = self._root,
            background = 'grey'
        )
        self.name = tk.Label(self._frame, text = self._project.name, font = ('Arial', 12))
        self.time = tk.Label(self._frame, text = self._project.timer, font = ('Arial', 12))
        self.play = tk.Button(self._frame, text = 'Play')

    def grid(self, row) -> None:
        """Place ProjectController on screen."""

        self._frame.grid(row = row, pady = 5, padx = 5, sticky = 'new')
        self.name.grid(row = 0, column = 0, padx = 10, pady = 2, sticky = 'w')
        self.time.grid(row = 0, column = 1, padx = 10, pady = 2, sticky = 'e')
        self.play.grid(row = 0, column = 0, padx = 10, pady = 2, sticky = 'e')
