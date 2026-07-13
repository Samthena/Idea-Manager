from Omnilinx import Idea

def test_home_page_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200

def test_new_idea_is_rendered_after_post(client):
    response = client.post(
        '/', 
        data={
            "title": "New Idea",
            "description": "This is a test idea.",
            "client": "OpenAI",
            "meeting_date": "2026-07-13T12:00",
            "owner": "Sam",
            "priority": "Няма",
            "status": "Нова",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"New Idea" in response.data

def test_empty_title_not_saved(client):
    response = client.post(
        "/",
        data={
            "title": "",
            "description": "Testing",
            "client": "OpenAI",
            "meeting_date": "2026-07-13T12:00",
            "owner": "Sam",
        },
    )

    assert response.status_code == 400

def test_nonexistent_idea_returns_404(client):
    response = client.get('/idea/9999')
    assert response.status_code == 404

def test_delete_removes_idea(client):
    client.post(
        "/",
        data={
            "title": "Delete Me",
            "description": "Testing",
            "client": "OpenAI",
            "meeting_date": "2026-07-13T12:00",
            "owner": "Sam",
        },
    )

    response = client.get("/delete/1", follow_redirects=True)

    assert b"Delete Me" not in response.data


def test_search_finds_matching_idea(client):
    client.post(
        "/",
        data={
            "title": "Python Project",
            "description": "Testing",
            "client": "OpenAI",
            "meeting_date": "2026-07-13T12:00",
            "owner": "Sam",
        },
    )

    response = client.get("/search?q=Python")

    assert b"Python Project" in response.data


def test_filter_by_priority(client):
    client.post(
        "/",
        data={
            "title": "High Priority",
            "description": "Testing",
            "client": "OpenAI",
            "meeting_date": "2026-07-13T12:00",
            "owner": "Sam",
            "priority": "Висок",
        },
    )

    client.post(
        "/",
        data={
            "title": "Low Priority",
            "description": "Testing",
            "client": "OpenAI",
            "meeting_date": "2026-07-13T12:00",
            "owner": "Sam",
            "priority": "Нисък",
        },
    )

    response = client.get("/filter?priority=Висок")

    assert b"High Priority" in response.data
    assert b"Low Priority" not in response.data

def test_update_priority(client):
    client.post(
        "/",
        data={
            "title": "Priority Test",
            "description": "Testing",
            "client": "OpenAI",
            "meeting_date": "2026-07-13T12:00",
            "owner": "Sam",
        },
    )

    idea = Idea.query.first()

    response = client.post(
        f"/update-priority/{idea.id}",
        data={"priority": "Висок"},
        follow_redirects=True,
    )

    assert response.status_code == 200

    updated = Idea.query.get(idea.id)
    assert updated.priority == "Висок"