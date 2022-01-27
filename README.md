# UserCommitCount
<p>This simple fastAPI web application interacts with GitHub's REST API's and Teradici's public repository for Cloud Access Manager: https://github.com/teradici/deploy</p>

<h2>Unit Tests</h2>
<p>docker-compose run core_api pytest</p>

<h2>Building</h2>
<p>docker-compose build</p>

<h2>Running the application</h2>
<p>docker-compose up</p>

<h3>Usage</h3>
/users
<p>Returns the users for everyone that has committed code to https://github.com/teradici/deploy</p>

/most-frequent
<p>Count the number of commits which occurred from June 1, 2019 - May 31, 2020</p>

/most-frequent?start=2019-09-07&end=2020-09-02
<p>Count the number of commits which occurred since start until end with the format of the start and end being YYYY-MM-DD</p>