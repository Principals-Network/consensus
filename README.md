# University Board Consensus System

A multi-agent system for simulating and experimenting with consensus-finding in academic governance.

## Overview

This system implements an AI-powered consensus-building framework for university board decisions, featuring:

- Multiple specialized board member agents (Academic Affairs, Financial, Research & Innovation, etc.)
- Advanced consensus metrics and algorithms
- Real-time discussion analysis
- Compromise suggestion generation
- Visualization of consensus formation

## Key Features

- Asynchronous agent discussions
- Weighted voting mechanisms
- Delphi method implementation
- Network-based consensus visualization
- Comprehensive metrics for measuring agreement

## Installation

```bash
# Clone the repository
git clone https://github.com/Principals-Network/consensus.git

# Install dependencies
poetry install
```

## Usage

```bash
# Run the consensus system
poetry run streamlit run run_consensus.py
```

## Project Structure

```
consensus/
├── src/
│   ├── agents/           # Board member agents
│   ├── ai/              # AI integration
│   ├── consensus/       # Consensus algorithms
│   ├── visualization/   # Visualization tools
│   └── utils/          # Utility functions
├── tests/              # Test suite
└── poetry.toml         # Project configuration
```

## Configuration

Create a `.env` file with your configuration:

```env
ANTHROPIC_API_KEY=your-api-key
MAX_TOKENS=2000
TEMPERATURE=0.5
MODEL_NAME=claude-3-5-sonnet-20241022
CONSENSUS_THRESHOLD=0.7
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request 