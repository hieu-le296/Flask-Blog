# TechTalks Blog

This blog is the CIS 245 Project at University of the Fraser Valley.

## Live Server
https://techtalks-blog.herokuapp.com/

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

Whenever running this project on the different system, please delete the previous virtual environment (venv) and create the new one.

### Prerequisites

What things you need to install the software and how to install them

```
Python 3.6 and later
Linux OS such as CentOS, Ubuntu, Linux Mint
Visual Studio Code (optional for editor)
```

### Installing
In terminal, create python3 virtual environment

```
$ python3 -m venv venv
```

And activate virtual environment

```
$ source venv/bin/activate
```

Once the virtual environment is activated, install all the modules and dependencies for this project


```
(venv) $ pip install -r requirments.txt
```

## Running the tests

There is no need to run database migration again. In order to run this program:
Export this app and make sure you are in the socialblog directory:

```
(venv) $ cd socialblog/
```
```
(venv) /socialblog $ export FLASK_APP=app.py
```
then type
```
(venv) /socialblog $ flask run
```


## Deployment

The Website can be deployed in Docker container for production. In order to run the container, please type
```
$ sudo docker-compose up
```

## Built With

* [Python 3](https://www.python.org/) - The programming language
* [PIP](https://pypi.org/project/pip/) - Dependency ManagementT
* [FLask](http://flask.pocoo.org/) - The web framework used
* [Boostrap](https://getbootstrap.com/) - Front end 

## Planned Technology

* Flask
* Flask WTForm
* Flask Login
* FLASK SQLAlchemy
* PILLOW - for uploading picture
* Flask Upload
* Flask Mail - for sending email
* FLASK Dance (Google Authentication)
* Stripe - for payment
* Database: SQLlite 
* Boostrap Temeplate

## Versioning

* Version 1.0

## Authors

* **Hieu Le**

## Donation Test
In order to test the donation, please use the testing visa card
* **Visa Card** - *4242 4242 4242 4242*
For more testing cards, please visit [Stripe Documentation](https://stripe.com/docs/testing)	

## Admin Page
In order to see the admin page, please login with this account:
* Email: admin@ourdrives.com
* Password: P@ssw0rd 
and then go to http://127.0.0.1:5000/admin

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments and References

Inspired by:
* **Miguel Grinberg** [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
* **Corey Schafer** [Flask Tutorials](https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH)
* Bootstrap theme from: https://startbootstrap.com
