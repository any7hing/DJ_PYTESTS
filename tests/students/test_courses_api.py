import pytest
from students.models import Student, Course
from rest_framework.test import APIClient
from model_bakery import baker

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    #Arrange
    courses = course_factory(_quantity=1)
    #Act
    response = client.get('/api/v1/courses/1/')
    data = response.json()
    #Assert
    assert response.status_code == 200
    assert courses[0].id == data['id']
    assert courses[0].name == data['name']
    
@pytest.mark.django_db
def test_get_all_courses(client, course_factory):
    #Arrange
    courses = course_factory(_quantity=10)
    #Act
    response = client.get('/api/v1/courses/')
    data = response.json()
    #Assert
    assert response.status_code == 200
    for i,c in enumerate(data):
        assert c['id'] == courses[i].id
        
@pytest.mark.django_db
def test_filter_course_by_id(client, course_factory):
    #Arrange
    courses = course_factory(_quantity=10)
    #Act
    response = client.get('/api/v1/courses/', {'id':courses[0].id})
    data = response.json()
    #Assert
    assert response.status_code == 200
    assert data[0]['id'] == courses[0].id
    
@pytest.mark.django_db
def test_filter_course_name(client, course_factory):
    #Arrange
    courses = course_factory(_quantity=10)
    #Act
    response = client.get(f'/api/v1/courses/?name={courses[0].name}')
    data = response.json()
    #Assert
    assert response.status_code == 200
    assert data[0]['name'] == courses[0].name

@pytest.mark.django_db
def test_create_course(client):
    #Arrange
    count = Course.objects.count()
    #Act
    response = client.post('/api/v1/courses/', data = {'name':'demo_test'})
    #Assert
    assert response.status_code == 201
    assert Course.objects.count() == count + 1
    
@pytest.mark.django_db
def test_update_course(client, course_factory):
    #Arrange
    courses = course_factory(_quantity=10)
    #Act
    response = client.patch(f'/api/v1/courses/{courses[0].id}/', data ={'name':'test_update'})
    #Assert
    assert response.status_code == 200
    assert response.data['name'] == 'test_update'
    
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    #Arrange
    courses = course_factory(_quantity=10)
    count = Course.objects.count()
    #Act
    response = client.delete(f'/api/v1/courses/{courses[0].id}/')
    #Assert
    assert response.status_code == 204
    assert Course.objects.count() == count - 1
    
@pytest.mark.django_db
def test_max_stunedts_at_course(client, students_factory):
    #Arrange
    students_test = students_factory(_quantity=21)
    x = Course.objects.create(name='test1')
    x.save()
    # y = Student.objects.create(name='123')
    # x.students.add(y)
    for s in students_test:
        # Course.objects.update_or_create(name='test1', students = s)
        x.students.add(s)
        x.save()
    # assert Course.objects.get(name='test1').students.count() < 20
    