# AoC 2024 Solution Generator 🎄

An AI-powered web application that generates and runs solutions for Advent of Code problems using OpenAI's GPT models. This app helps automate the process of solving Advent of Code challenges by generating specifications and implementing solutions using AI.

## Features 🌟

- Generate solution specifications from problem descriptions
- Create Python solutions based on specifications
- Run solutions with custom input files
- Real-time execution status updates
- Support for multiple GPT models (GPT-4 Turbo, GPT-4, GPT-3.5 Turbo)
- Download generated specs and solutions
- Cost tracking for API usage
- Advent of Code themed UI
- Secure API key handling

## Prerequisites 📋

- Python 3.9+
- Poetry (for local development)
- Docker and Docker Compose (for containerized deployment)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Local Setup 🛠️

1. Clone the repository:
```bash
git clone <repository-url>
cd adventofcode2024
```

2. Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your-api-key-here
FLASK_PORT=5001  # Optional, defaults to 5001
```

3. Install dependencies with Poetry:
```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

4. Run the application:
```bash
poetry run python run.py
```

The app will be available at `http://localhost:5001`

## Docker Setup 🐳

1. Clone the repository:
```bash
git clone <repository-url>
cd adventofcode2024
```

2. Create a `.env.docker` file:
```env
OPENAI_API_KEY=your-api-key-here
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The app will be available at `http://localhost:5001` (or the next available port if 5001 is in use)

## Usage Guide 💡

1. Start the application using either local or Docker setup
2. Open your browser and navigate to `http://localhost:5001`
3. If you haven't set an API key in the environment file:
   - You'll see a prompt to enter your OpenAI API key
   - Enter your key in the secure input field
   - The key will be stored only in memory
4. To generate a solution:
   - Select a GPT model from the dropdown
   - Enter your problem instructions in the text area
   - (Optional) Upload an input file if your problem requires one
   - Click "Generate Solution"
5. Monitor progress in the status log:
   - Watch real-time updates
   - See token usage and costs
   - View any errors or warnings
6. View results in three tabs:
   - Specification: The AI-generated problem analysis
   - Solution: The implemented Python code
   - Result: Output from running the solution
7. Download options:
   - Download the specification as a markdown file
   - Download the solution as a Python file

## Development Setup 🔧

### Project Structure
```
.
├── app/
│   ├── services/         # Core services
│   │   ├── llm_handler.py    # OpenAI integration
│   │   └── solution_runner.py # Code execution
│   ├── static/          # Frontend assets
│   │   ├── css/         # Styles
│   │   └── js/          # Client-side scripts
│   ├── templates/       # HTML templates
│   └── routes/          # API routes
├── docker-compose.yml   # Docker configuration
├── Dockerfile          # Container definition
├── pyproject.toml      # Poetry dependencies
└── run.py             # Application entry point
```

### Adding New Features
1. Backend changes:
   - Add routes in `app/routes/main.py`
   - Add services in `app/services/`
   - Update models in `app/models/`

2. Frontend changes:
   - Modify templates in `app/templates/`
   - Update styles in `app/static/css/`
   - Add scripts in `app/static/js/`

## Security Notes 🔒

- Never commit `.env` or `.env.docker` files
- The Docker container runs:
  - In read-only mode
  - With no-new-privileges security option
  - With limited CPU and memory resources
- API keys are stored only in memory
- Temporary files are automatically cleaned up
- Input validation is performed on all requests

## Troubleshooting 🔍

### Common Issues

1. Port conflicts:
   - The app tries ports 5001 and up if the default is taken
   - On macOS, disable AirPlay Receiver if using port 5000
   - Use `PORT=xxxx docker-compose up` to specify a port

2. API Key issues:
   - Ensure your key is valid and has sufficient credits
   - Check for spaces or newlines in your key
   - Verify the key is properly set in .env or .env.docker

3. Docker issues:
   - Run `docker-compose down` before rebuilding
   - Check logs with `docker-compose logs`
   - Clear containers with `docker container prune`

### Getting Help

- Check the status log in the UI for detailed error messages
- Look at Docker logs for container issues
- Review the OpenAI API documentation for API errors
- Open an issue on GitHub for bugs

## Acknowledgments 👏

- Advent of Code for the inspiration
- OpenAI for the GPT API
- Flask and Poetry communities
