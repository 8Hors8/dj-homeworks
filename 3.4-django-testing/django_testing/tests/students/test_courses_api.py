import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student():
    return Student.objects.create(name='st1')


@pytest.fixture
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_first_courses(client, courses_factory):
    course = courses_factory(_quantity=1)[0]

    response = client.get(f'/api/v1/courses/{course.id}/')
    data = response.json()
    student_ids = list(course.students.values_list('id', flat=True))

    assert response.status_code == 200
    assert data['id'] == course.id
    assert data['name'] == course.name
    assert sorted(data['students']) == sorted(student_ids)


@pytest.mark.django_db
def test_get_courses(client, courses_factory, students_factory):
    courses = courses_factory(_quantity=10)
    for course in courses:
        students = students_factory(_quantity=2)
        course.students.set(students)

    response = client.get('/api/v1/courses/')
    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(courses)
    for i, c in enumerate(data):
        student_ids = list(courses[i].students.values_list('id', flat=True))
        assert c['name'] == courses[i].name
        assert sorted(c['students']) == sorted(student_ids)


@pytest.mark.django_db
def test_filter_courses_by_id(client, courses_factory):
    courses = courses_factory(_quantity=5)
    course_to_filter = courses[2]

    response = client.get(f'/api/v1/courses/?id={course_to_filter.id}')
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['id'] == course_to_filter.id
    assert data[0]['name'] == course_to_filter.name


@pytest.mark.django_db
def test_filter_courses_by_name(client, courses_factory):
    courses = courses_factory(_quantity=5)
    course_to_filter = courses[2]

    response = client.get(f'/api/v1/courses/?name={course_to_filter.name}')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['id'] == course_to_filter.id
    assert data[0]['name'] == course_to_filter.name


@pytest.mark.django_db
def test_create_course(client):
    course_data = {
        'name': 'Python'
    }

    response = client.post('/api/v1/courses/', data=course_data)
    created_course = Course.objects.first()
    assert response.status_code == 201
    assert Course.objects.count() == 1
    assert created_course.name == course_data['name']


@pytest.mark.django_db
def test_update_course(client, courses_factory):
    courses = courses_factory(_quantity=5)
    course_update = {
        'name': 'Python'
    }
    course_id = courses[2]

    response = client.patch(f'/api/v1/courses/{course_id.id}/', data=course_update)
    updated_course = Course.objects.get(id=course_id.id)

    assert response.status_code == 200
    assert updated_course.name == course_update['name']


@pytest.mark.django_db
def test_delete_course(client, courses_factory):
    courses = courses_factory(_quantity=5)
    course_to_delete = courses[2]

    response = client.delete(f'/api/v1/courses/{course_to_delete.id}/')

    assert response.status_code == 204
    assert Course.objects.filter(id=course_to_delete.id).count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize("num_students, expected_exception", [
    (19, None),
    (20, None),
    (21, ValidationError),
])
def test_student_limit_on_course(settings, num_students, expected_exception,
                                 client, courses_factory, students_factory):
    settings.MAX_STUDENTS_PER_COURSE = 20
    course = courses_factory(_quantity=1)[0]
    students = students_factory(_quantity=num_students)

    if expected_exception:
        with pytest.raises(expected_exception):
            course.students.set(students)
            course.clean()
    else:
        course.students.set(students)
        course.clean()