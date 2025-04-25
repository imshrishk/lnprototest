<div align="center">
  <h1>lnprototest</h1>

  <p>
    <strong>a Testsuite for the Lightning Network Protocol</strong>
  </p>

  <h4>
    <a href="https://github.com/rustyrussell/lnprototest">Project Homepage</a>
  </h4>
 
  <a href="https://github.com/rustyrussell/lnprototest/actions">
    <img alt="GitHub Workflow Status (branch)" src="https://img.shields.io/github/workflow/status/rustyrussell/lnprototest/Integration%20testing/master?style=flat-square"/>
  </a>
  
  <a href="https://github.com/vincenzopalazzo/lnprototest/blob/vincenzopalazzo/styles/HACKING.md">
    <img src="https://img.shields.io/badge/doc-hacking-orange?style=flat-square" />
  </a>

</div>

lnprototest is a set of test helpers written in Python3, designed to
make it easy to write new tests when you propose changes to the
lightning network protocol, as well as test existing implementations.

## Install requirements

To install the necessary dependences

```bash
pip3 install poetry
poetry shell
poetry install
```

Well, now we can run the test

## Running test

The simplest way to run is with the "dummy" runner:

	make check

Here are some other useful pytest options:

1. `-n8` to run 8-way parallel.
2. `-x` to stop on the first failure.
3. `--pdb` to enter the debugger on first failure.
4. `--trace` to enter the debugger on every test.
5. `-k foo` to only run tests with 'foo' in their name.
6. `tests/test_bolt1-01-init.py` to only run tests in that file.
7. `tests/test_bolt1-01-init.py::test_init` to only run that test.
8. `--log-cli-level={LEVEL_NAME}` to enable the logging during the test execution.

### Running Against A Real Node.

The more useful way to run is to use an existing implementation. So
far, core-lightning is supported.  You will need:

1. `bitcoind` installed, and in your path.
2. [`lightningd`](https://github.com/ElementsProject/lightning/) compiled with
   `--enable-developer`. By default the source directory should be
   `../lightning` relative to this directory, otherwise use
   `export LIGHTNING_SRC=dirname`.
3. Install any python requirements by
   `pip3 install -r lnprototest/clightning/requirements.txt`.

Then you can run

	make check PYTEST_ARGS='--runner=lnprototest.clightning.Runner'

or directly:

    pytest --runner=lnprototest.clightning.Runner

# Further Work

If you want to write new tests or new backends, see [HACKING.md](HACKING.md).

Let's keep the sats flowing!

Rusty.

# LNPrototest Message Flow Visualizer

A web application for visualizing and interacting with Lightning Network protocol message flows using lnprototest.

This tool allows developers to:
- Connect to different Lightning Network implementations (LDK, c-lightning, etc.)
- Visualize message flows between nodes
- Test protocol compliance with predefined test sequences
- Send custom messages and observe responses

## Project Structure

```
├── api/                      # Backend Flask API
│   ├── app.py                # Main API implementation
│   └── requirements.txt      # Python dependencies
│
├── webapp/                   # Frontend React application
│   ├── public/               # Static assets
│   ├── src/                  # Source code
│   │   ├── api/              # API client
│   │   ├── components/       # React components
│   │   └── types/            # TypeScript type definitions
│   ├── package.json          # Node.js dependencies
│   └── tsconfig.json         # TypeScript configuration
│
└── README.md                 # This file
```

## Prerequisites

- Node.js 16+ and npm
- Python 3.7+
- Lightning Network implementation (LDK is supported by default)

## Setup Instructions

### Backend API

1. From the project root, set up a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the lnprototest and Flask API dependencies:

```bash
pip install -e .
cd api
pip install -r requirements.txt
```

3. Start the Flask API:

```bash
python app.py
```

The API will run on http://localhost:5000.

### Frontend Web App

1. Navigate to the webapp directory:

```bash
cd webapp
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm start
```

The web app will run on http://localhost:3000.

## Usage Guide

1. **Connect to a Node**: 
   - Select an implementation from the dropdown
   - Click "Connect" and provide connection details

2. **Run a Test Sequence**:
   - Select a predefined test sequence
   - Click "Run Test Sequence"
   - View the message flow results

3. **Send Custom Messages**:
   - Use the "Send Message" dropdown to select a message type
   - Set message parameters if needed
   - View the response in the message flow

## BOLT Specifications Implementation

This visualizer currently implements the following BOLT specifications:

- BOLT #1: Base Protocol (Messaging)
  - Init Messages
  - Ping/Pong Messages

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The Lightning Network Developers
- lnprototest project maintainers
