import os
import sys
import durations_nlp
from datetime import datetime, timedelta
from github import Github, Project
import yaml


def clean(project: Project, rules):
    print(f"Processing {project.name}")
    for column in rules:
        target_col = None
        for projectColumn in project.get_columns():
            if column in projectColumn.name:
                target_col = projectColumn
                break

        if target_col is None:
            print(f"Couldn't match {column} to any column in {project.name}")
            return

        duration = durations_nlp.Duration(rules[column]['older_than'])
        if duration.to_days() < 3:
            print(f"Refusing to delete all cards older than {duration.to_hours()}h, duration is too short")
            return

        cards = target_col.get_cards()
        print(f"Found {cards.totalCount} cards in {target_col.name}")

        max_age = timedelta(seconds=duration.seconds)
        archived = 0
        for card in cards:
            if datetime.now() - card.updated_at > max_age:
                card.update(archived=True)
                archived += 1

        print(f"Archived {archived} cards in {project.name}/{target_col.name}")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <projects.yml>")
        sys.exit(1)

    try:
        config = yaml.safe_load(open(sys.argv[1], 'r'))
    except Exception as e:
        print(f"Could not load settings from {sys.argv[1]}")
        sys.exit(2)

    ghtoken = os.environ.get('GITHUB_TOKEN')
    if ghtoken is None or ghtoken == "":
        print("Could not read $GITHUB_TOKEN")
        sys.exit(3)

    gh = Github(ghtoken)

    for board in config:
        orgproject = board.split('/')
        try:
            org = gh.get_organization(orgproject[0])
        except Exception:
            try:
                org = gh.get_user(orgproject[0])
            except Exception:
                print(f"Couldn't find user or org '{orgproject[0]}'")
                return 1

        project = None
        for p in org.get_projects():
            if p.number == int(orgproject[1]):
                project = p
                break

        if project is None:
            print(f"Could not find project {orgproject[1]} in {orgproject[0]}")
            return

        clean(project, config[board])


if __name__ == '__main__':
    main()
