# gh-project-cleanup

A script and GH action to cleanup old cards sitting in Done-like columns in Github Projects.

## Example

```yaml
  cleanup-project:
    name: Cleanup old cards in Done column
    runs-on: ubuntu-latest
    steps:
      - uses: roobre/gh-project-cleanup@v1
        with:
          github_token: ${{ secrets.ACTUAL_TOKEN }}
          config: |
            # Location and ID of project
            roobre/1:
              Done: # Column name to cleanup, matches partially (i.e. contains)
                older_than: 2 months # Format must be understandable by https://pypi.org/project/durations-nlp/
```
