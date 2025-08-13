@echo off
title AutoMidjourney-400

cd /d E:\Dropbox\Dev\Projects\Python\automidjourney
uv run auto_midjourney.py --get_prompts --prompt_file --count 400 
