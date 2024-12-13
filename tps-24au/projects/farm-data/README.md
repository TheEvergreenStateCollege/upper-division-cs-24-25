# Farm data processing script
Script that read through hours.json to print the number of hours each crop has been put into harvesting and how long it takes into processing how long each worker has worked and all the crops they worked on broken down for harvesting and processing. what are people doing? and what crops are getting the most attention? harvesting product and finished products. 

to run type `python3 hoursData.py` then follow the commands printed to the terminal

### What to expect
you can
- see person and what they are clocked in as doing
- search for an individual person by name or by their id and see what they are working on and for how long
    - barcode scanning will need to be implimented in the future
- search for a specific crop and see who is working on it and for how long and see how much effort is requiered to be put into it with its overall time spent

### Ideas of what would be implimented in a future project
Once the database is actually collecting real data these scripts can be used to see the time spent on the farm. Ideally the script would be changed to send data to a website front end for admins to look at and manage the information in a far more readable way than just command line output. 