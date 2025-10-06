#!/bin/bash
# Quick test runner for course exercises
# Usage: ./check_exercise.sh 1   (for exercise 1)
#        ./check_exercise.sh     (for all exercises)

EXERCISE_NUM=$1

if [ -z "$EXERCISE_NUM" ]; then
    echo "🧪 Running ALL exercise tests..."
    python -m pytest tests/ -v --no-cov
else
    echo "🧪 Running tests for Exercise $EXERCISE_NUM..."
    python -m pytest tests/test_ex${EXERCISE_NUM}_*.py -v --no-cov
fi
