# GitHub repository listing helper

Use `list_github_repos.py` to export a full repository list as CSV.

## Public repositories for any username

```bash
python3 list_github_repos.py <github-username> --output repos.csv
```

## Your own public + private repositories

```bash
export GITHUB_TOKEN="<your-token>"
python3 list_github_repos.py --private --output repos.csv
```

The token needs `repo` scope to include private repositories.
