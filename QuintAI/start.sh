#!/usr/bin/env bash

gunicorn api_server.wsgi:application