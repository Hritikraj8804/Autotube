# Contributing to AutoTube

First off, thank you for considering contributing to AutoTube! It's people like you that make AutoTube such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Standards

- **Be respectful**: Treat everyone with respect. We're all here to learn and improve.
- **Be constructive**: Provide helpful feedback and constructive criticism.
- **Be collaborative**: Work together towards common goals.
- **Be inclusive**: Welcome newcomers and help them get started.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include as many details as possible:

**Bug Report Template:**
```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g. Windows 11, Ubuntu 22.04]
 - Docker version: [e.g. 24.0.5]
 - n8n version: [from docker logs]

**Additional context**
Add any other context about the problem.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful** to most AutoTube users
- **List some other projects** where this enhancement exists, if applicable

### Pull Requests

**Process:**

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/my-awesome-feature
   ```

2. **Make your changes** following our coding standards

3. **Test your changes thoroughly**
   - Ensure all existing functionality still works
   - Test new features with various inputs
   - Check Docker containers restart properly

4. **Commit your changes** with clear, descriptive messages
   ```bash
   git commit -m "Add awesome feature: brief description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/my-awesome-feature
   ```

6. **Open a Pull Request** with a clear title and description

**Pull Request Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have tested my changes
- [ ] I have updated the documentation
- [ ] My changes don't break existing functionality
- [ ] I have added comments to complex code
```

## Development Setup

### Prerequisites

- Docker Desktop or Docker Engine
- Git
- Python 3.11+ (for local testing)
- Basic knowledge of n8n workflows

### Setting Up Development Environment

1. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Autotube.git
   cd Autotube
   ```

2. **Set up environment**
   ```bash
   cd short_automation
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

4. **View logs**
   ```bash
   docker-compose logs -f
   ```

### Running Tests

```bash
# Test Python scripts
docker exec youtube-python python /scripts/ai_generator.py
docker exec youtube-python python /scripts/create_video.py

# Test API
curl http://localhost:5001/health

# Test n8n workflow
# Open http://localhost:5678 and run the workflow manually
```

### Local Python Development

```bash
# Enter Python container
docker exec -it youtube-python bash

# Install dependencies
pip install -r /scripts/requirements.txt

# Test scripts
python /scripts/ai_generator.py
```

## Coding Standards

### Python

- **PEP 8**: Follow Python's PEP 8 style guide
- **Docstrings**: Use Google-style docstrings for all functions
- **Type hints**: Use type hints where appropriate
- **Comments**: Comment complex logic, not obvious code

**Example:**
```python
def generate_image(prompt: str, output_path: str = None) -> str:
    """
    Generate an AI image from text prompt.
    
    Args:
        prompt: Text description for image generation
        output_path: Optional path to save image
        
    Returns:
        Path to generated image file
        
    Raises:
        ValueError: If prompt is empty
        IOError: If image cannot be saved
    """
    # Implementation here
    pass
```

### Docker

- Keep Dockerfiles minimal and efficient
- Use specific version tags, not `latest` in production
- Document all environment variables
- Clean up temporary files in build steps

### n8n Workflows

- Add descriptive names to all nodes
- Use comments in Code nodes
- Handle errors gracefully
- Test thoroughly before committing

### Documentation

- Update README.md if you change functionality
- Keep documentation in sync with code
- Use clear, concise language
- Include code examples where helpful

## Project Structure

```
Autotube/
├── short_automation/
│   ├── docker-compose.yml      # Service orchestration
│   ├── .env.example            # Environment template
│   ├── workflows/              # n8n workflow JSON files
│   ├── scripts/                # Python automation scripts
│   │   ├── ai_generator.py     # AI image generation
│   │   ├── create_video.py     # Video creation logic
│   │   └── video_api.py        # Flask API server
│   └── data/                   # Persistent data (gitignored)
├── docs/                       # Documentation
├── START-ROBOT.bat             # Windows start script
└── README.md                   # Main documentation
```

## Areas for Contribution

We welcome contributions in these areas:

### 🎨 Features
- Additional AI providers (GPT-4, Claude, Gemini)
- Advanced video effects and transitions
- Thumbnail generation
- Multi-language support
- Scheduled posting
- Analytics dashboard

### 🐛 Bug Fixes
- Video generation errors
- API timeout issues
- Docker networking problems
- Workflow edge cases

### 📚 Documentation
- Improve existing docs
- Add tutorials
- Create video guides
- Translate documentation

### 🧪 Testing
- Unit tests for Python scripts
- Integration tests for workflows
- Performance testing
- Error handling tests

### 🎨 UI/UX
- Custom n8n nodes
- Workflow templates
- Dashboard improvements

## Git Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests

**Examples:**
```
Add AI image fallback mechanism
Fix video generation timeout issue
Update documentation for Python API
Improve error handling in create_video.py
```

## Release Process

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create release branch
4. Test thoroughly
5. Merge to main
6. Tag release
7. Create GitHub release with notes

## Community

- **GitHub Discussions**: For questions and general discussion
- **Issues**: For bugs and feature requests
- **Pull Requests**: For code contributions

## Need Help?

- Check the [documentation](docs/)
- Search existing [issues](https://github.com/Hritikraj8804/Autotube/issues)
- Ask in [GitHub Discussions](https://github.com/Hritikraj8804/Autotube/discussions)

## Recognition

Contributors will be recognized in:
- README.md acknowledgments
- Release notes
- Project documentation

Thank you for contributing to AutoTube! 🎉
