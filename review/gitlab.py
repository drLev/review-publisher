import requests
import datetime


def get_commits_url(gitlab_url, project_id):
    return gitlab_url \
           + '/api/v4/projects/' \
           + str(project_id) \
           + '/repository/commits'


def api_request_creator(private_token):
    headers = {
        'private-token': private_token
    }

    def gitlab_api_request(method, url, params):
        return requests.request(
            method=method,
            headers=headers,
            url=url,
            params=params
        )
    return gitlab_api_request


def get_query_params(ref_name):
    since_date = datetime.datetime.now()
    return {
        "ref_name": ref_name,
        "since": since_date.strftime("%Y-%m-%d 00:00:00")
    }


def get_commits(url, branches, request):
    commits = {}
    for branch in branches:
        response = request(
            method="GET",
            url=url,
            params=get_query_params(branch)
        )
        for commit in response.json():
            commits[commit['id']] = {
                "author_name": commit['author_name'],
                "title": commit["title"],
                "branch": "master"
            }
    return commits


def commit_url(gitlab_url, project_path, commit_id):
    return gitlab_url + '/' + project_path + '/commit/' + commit_id


def set_url_to_commits(commits, gitlab_url, project_path):
    for commit_id in commits:
        commits[commit_id]['commit_url'] = commit_url(
            gitlab_url,
            project_path,
            commit_id
        )
    return commits


def commits_by(gitlab_url, private_token):
    request = api_request_creator(private_token)

    def func_get_commits_by(project_id, project_path, branches):
        return set_url_to_commits(
            get_commits(
                get_commits_url(
                    gitlab_url,
                    project_id
                ),
                branches,
                request
            ),
            gitlab_url,
            project_path
        )
    return func_get_commits_by