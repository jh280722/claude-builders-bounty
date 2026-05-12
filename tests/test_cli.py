from claude_review.cli import parse_pr_url, validate_review, heuristic_review, PullRequestRef


def test_parse_full_github_pr_url():
    ref = parse_pr_url("https://github.com/owner-name/repo.name/pull/123")
    assert ref.owner == "owner-name"
    assert ref.repo == "repo.name"
    assert ref.number == 123
    assert ref.slug == "owner-name/repo.name"


def test_parse_owner_repo_shorthand():
    ref = parse_pr_url("octocat/Hello-World#42")
    assert ref == PullRequestRef("octocat", "Hello-World", 42)


def test_invalid_pr_url_is_rejected():
    try:
        parse_pr_url("https://example.com/not/github/pull/1")
    except ValueError as exc:
        assert "github.com" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_heuristic_review_has_required_sections():
    diff = """diff --git a/src/app.py b/src/app.py
--- a/src/app.py
+++ b/src/app.py
@@ -1 +1,2 @@
-print('old')
+print('new')
+print('token check')
"""
    review = heuristic_review(PullRequestRef("owner", "repo", 1), diff)
    assert validate_review(review) == []
    assert "## Summary" in review
    assert "## Identified risks" in review
    assert "## Improvement suggestions" in review
    assert "## Confidence" in review
    assert "credential" in review.lower() or "secret" in review.lower()
