# Python Scheduler Application

This project is a Python-based scheduler application that utilizes the Model-View-Controller (MVC) design pattern along with various design patterns to enhance its functionality. The application is built using PyQt5 for the graphical user interface.

## Project Structure

The project is organized into the following directories and files:

```
python-scheduler
├── src
│   ├── models
│   │   ├── __init__.py
│   │   ├── task.py
│   │   └── scheduler_model.py
│   ├── views
│   │   ├── __init__.py
│   │   ├── abstract_factory.py
│   │   ├── builders
│   │   │   ├── __init__.py
│   │   │   └── view_builder.py
│   │   ├── components
│   │   │   ├── __init__.py
│   │   │   └── ui_components.py
│   │   ├── themes
│   │   │   ├── __init__.py
│   │   │   └── theme_factory.py
│   │   ├── main_window.py
│   │   ├── task_edit_view.py
│   │   └── schedule_edit_view.py
│   ├── controllers
│   │   ├── __init__.py
│   │   ├── main_controller.py
│   │   ├── task_controller.py
│   │   └── schedule_controller.py
│   ├── patterns
│   │   ├── __init__.py
│   │   ├── observer.py
│   │   ├── command.py
│   │   ├── state.py
│   │   └── strategy.py
│   └── utils
│       ├── __init__.py
│       └── config_manager.py
├── config
│   ├── task_lists.conf
│   └── work_time.conf
├── main.py
├── requirements.txt
└── README.md
```

## Features

- **Task Management**: Create, edit, and delete tasks with various attributes such as name, status, and estimated time.
- **Scheduler Management**: Manage a list of tasks and their states.
- **User Interface**: A user-friendly interface built with PyQt5, allowing for easy interaction with the application.
- **Design Patterns**: Utilizes several design patterns including Builder, Abstract Factory, Strategy, Observer, Command, and State to enhance flexibility and maintainability.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd python-scheduler
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python main.py
```

This will launch the main window of the scheduler application, where you can manage your tasks and schedules.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.