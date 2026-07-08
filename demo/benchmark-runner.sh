#!/bin/bash
# CodeMind AI Security Benchmark Runner
# Runs all security tests across every vuln/fix branch pair

set -e

BRANCHES=(
  "vuln/sql-injection:fix/sql-injection"
  "vuln/idor:fix/idor"
  "vuln/ssrf:fix/ssrf"
  "vuln/path-traversal:fix/path-traversal"
  "vuln/mass-assignment:fix/mass-assignment"
  "vuln/command-injection:fix/command-injection"
)

echo "============================================"
echo " CodeMind AI Security Benchmark"
echo "============================================"
echo ""

for pair in "${BRANCHES[@]}"; do
  VULN_BRANCH="${pair%%:*}"
  FIX_BRANCH="${pair##*:}"

  echo "--------------------------------------------"
  echo " Scenario: $VULN_BRANCH"
  echo "--------------------------------------------"

  # Checkout vulnerable branch
  git checkout "$VULN_BRANCH" 2>/dev/null
  echo " [VULN] Running security tests..."
  cd backend
  VULN_RESULT=$(pytest tests/security/ -v --tb=line 2>&1 | tail -5)
  cd ..
  echo "$VULN_RESULT"

  # Checkout fix branch
  git checkout "$FIX_BRANCH" 2>/dev/null
  echo " [FIX] Running security tests..."
  cd backend
  FIX_RESULT=$(pytest tests/security/ -v --tb=line 2>&1 | tail -5)
  cd ..
  echo "$FIX_RESULT"

  echo ""
done

git checkout main 2>/dev/null
echo "============================================"
echo " Benchmark complete!"
echo "============================================"
