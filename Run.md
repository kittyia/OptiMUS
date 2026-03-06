main.py运行命令：

```bash
python .\main.py --api_key "*********" --base_url "https://1yvxf19722895.vicp.fun/v1" --model "Qwen/Qwen3-8B" --dir .\data\nlp4lp\1
```

batch_run.py运行命令：

```bash
nohup python.exe .\batch_run.py --api_key "*****" --base_url "https://1yvxf19722895.vicp.fun/v1" --model "Qwen/Qwen3-8B" --base_dir "./data/nlp4lp" > batch_run.log 2>&1 &
```