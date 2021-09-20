# Winter 2022 - Shopify Developer Intern Challenge

Image repository built on [Django](https://www.djangoproject.com/) for 
[Shopify Developer Intern Challenge](https://docs.google.com/document/d/1eg3sJTOwtyFhDopKedRD6142CFkDfWp1QvRKXNTPIOc/edit#).

REST API is implemented with [Django REST Framework](https://www.django-rest-framework.org/). 

Database is [sqlite3](https://www.sqlite.org/index.html).

Supported image formats: .jpeg, .png 

**Functionality:**
* Upload one image or multiple images
    * Secure uploading: only authorized users can add images
    * Permissions: when a new image is added, the user sets its private or public access 
    (`public` attribute in `Image` model) 
        * `GET` API method was not a part of the Developer Intern Challenge requirements 
            and therefore was not implemented. 
            To implement `GET` please use `Image: public` value for access permissions.  
    
* Delete one image or multiple images
    * Secure deletion: only authorized users can delete images
    * Access control: user cannot delete other user's images
    * All images cannot be deleted at ones because no user owns all images, 
    and a user can delete only their own images

 

## Quick start

* Make sure you have `virtualenv` installed (usually installed by `pip3 install virtualenv`)
* Clone the repository
* Create a virtualenv in the project directory
```
$ virtualenv env -p `which python3`
```
* Activate the virtualenv from the project dir for working in terminal
```
$ source env/bin/activate
```
(Also, setup the project interpreter in PyCharm or other IDE)

* Install the project requirements by running
```
$ pip3 install -r requirements.txt
```
* Run migration from `/repoapp` dir
```
$ cd repoapp
$ python manage.py migrate
```
This will generate sqlite3 database with the relevant structure.

* Run Django server from `/repoapp` dir
```
$ python manage.py runserver
```

## REST API

**IMPORTANT:** Only authorized users can use the REST API. Before using the API please log in.

```
Username: user1 
Password: 1111

Username: user2 
Password: 1111
```
If you decide to use [Postman](https://www.postman.com/) to call the API: 
1. Select `Basic Auth` type in the `Authorization` tab 
2. Enter username & password

Otherwise, please check how to login via your API platform of choice before using this API.

* **Add one image to the repo**
    - Request Method: POST
    - Request URL: http://127.0.0.1:8000/images/
    - Request JSON format:
        ```
        {
          "public": <true / false>,
          "image": <base64-encoded image string>
        }
        ```
    - Response Status: 
        * Success - Image added: 201
        * Failure - Unauthorized: 403
        * Failure - Bad Request: 400
        
* **Add multiple images to the repo**
    - Request Method: POST
    - Request URL: http://127.0.0.1:8000/images/create_multiple/
    - Request JSON format:
        ```
      [
            {
              "public": <true / false>,
              "image": <base64-encoded image string>
            },
            {
              "public": <true / false>,
              "image": <base64-encoded image string>
            }
      ]
        ```
    - Response Status: 
        * Success: 201
        * Failure - Unauthorized: 403
    - Response JSON format: 
        ```
      {
            "created": [<image data>],
            "failed": [<image data>]
      }
        ```
* **Delete one image from the repo**
    - Request Method: DELETE
    - Request URL: http://127.0.0.1:8000/images/<IMAGE-ID>/
    - No Request Body
    - Response Status: 
        * Success - Image deleted: 204
        * Failure - Unauthorized: 403
        * Failure - Not Found: 404
              
* **Delete multiple images from the repo**
    - Request Method: DELETE
    - Request URL: http://127.0.0.1:8000/images/delete_multiple/?ids=<COMMA-SEPARATED-IMAGE-IDS>
    - No Request Body
    - Response Status: 
        * Success: 200
        * Failure - Unauthorized: 403
    - Response JSON format: 
        ```
      {
            "deleted": [<image IDs>],
            "not_deleted": [<image IDs>]
      }
        ```
        
## Create a new superuser (for django admin access)
Call the following command from the `/repoapp` dir
```
$ python manage.py createsuperuser
```
      
    
           
