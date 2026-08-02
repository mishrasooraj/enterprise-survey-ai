#!/bin/sh

set -e

echo "Waiting for Ollama..."

until ollama list >/dev/null 2>&1
do
    sleep 2
done

echo "Pulling model..."

ollama pull ${OLLAMA_MODEL}

echo "Model Ready."