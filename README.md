# Airflow Teams Notifier

A Python-based notification system that automatically sends Microsoft Teams alerts for Airflow DAG failures with associated ServiceNow ticket information. This project provides a modular and configurable solution for integrating Airflow monitoring with Teams notifications.

## Features

- 🚀 Automated Teams notifications for Airflow DAG failures
- 🎯 Integration with ServiceNow ticket information
- 🔧 Modular and object-oriented design
- 🛡️ Built-in error handling
- ⚙️ Configurable notification templates
- 🔄 Easy to extend and customize

## Project Structure

airflow_teams_notifier/
│
| ├── src/
│ ├── init.py
│ ├── models/
│ │ ├── init.py
│ │ ├── servicenow_ticket.py
│ │ └── airflow_failure.py
│ ├── notifiers/
│ │ ├── init.py
│ │ ├── teams_notifier.py
│ │ └── notification_manager.py
│ └── config.py
│
├── requirements.txt
├── README.md
└── main.py

## Configuration

The application can be configured through `src/config.py`. Key configurations include:
- Teams webhook URL
- Message templates
- Notification settings

## Requirements

- Python 3.7+
- requests>=2.25.1
- Microsoft Teams access
- ServiceNow instance (optional)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is not yet license but trying make it copywrite.

## Acknowledgments

- Microsoft Teams API Documentation
- Apache Airflow Documentation
- ServiceNow API Documentation

## Contact

Naval Hatode - [@navalhatode](https://twitter.com/navalhatode) - navalhatode@gmail.com
Akshay Prabhu - [@akshayprabhu](https://www.linkedin.com/in/akshay-prabhu-0a757484/)

Project Link: [https://github.com/navalhatode/airflow_teams_notifier](https://github.com/navalhatode/airflow_teams_notifier)
