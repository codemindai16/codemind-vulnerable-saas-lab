# Demo Scenarios

This directory contains demo scenarios for showcasing CodeMind AI's capabilities.

## SSRF Detection Demo

The [ssrf-scenario.md](ssrf-scenario.md) walks through a complete flow:
- PR with SSRF vulnerability
- CodeMind AI detection and analysis
- Automatic fix generation
- Validation via security tests

## Running the Full Benchmark

```bash
chmod +x benchmark-runner.sh
./benchmark-runner.sh
```

This checks out each `vuln/*` branch, runs the failing security tests, then checks out the `fix/*` branch, and verifies the tests pass.
