运行方式

```bash
nohup python3.12 main.py -k "_FPW*****" -b "https://api.poe.com/v1" -m "gpt-5.2-instant" --dir ./data/test --devmode 1 > test.log 2>&1 &

```

- `-k` or `--key`: Your API key for the language model service.
- `-b` or `--base_url`: The base URL for the API endpoint of the language model service.
- `-m` or `--model`: The specific model you want to use for processing the optimization problems.
- `--dir`: The directory where your input data is located. This should contain the files that the program will read and process.
- `--devmode`: A flag to indicate whether to run in development mode. Setting this to `1` enables development mode, which may include additional logging or debugging features.
- `nohup`: This command allows the process to continue running in the background even after you log out of the terminal.
- `> test.log 2>&1`: This redirects both the standard output and standard error to a file named `test.log`, allowing you to review the logs later.
- `&`: This symbol at the end of the command runs the process in the background, allowing you to continue using the terminal for other commands.