# NBA-Player-Comparator
Summary:

This program takes two current NBA players and compares them based on stats the user chooses from a list. The program uses the requests and beautifulsoup modules from python to parse data from the Basketball Reference website. The data is then sifted and only the select statstics are taken and displayed. The program then shows the user which player is leading each stat.

Limitations: 

-cannot parse data for players that are retired

-cannot parse data if user spells the name of the player wrong in any way, the name must be spelled perfectly

-cannot finish gathering statsics if the user enters which statistics they want incorrectly


Below is a sample of the running program:

Step 1 : We are prompted to list the names of two current NBA players by entering the first then the last name for each.

<img width="311" alt="screen shot 2017-06-19 at 4 21 50 pm" src="https://user-images.githubusercontent.com/13561051/27309897-7d06ae66-550b-11e7-8093-f8a7982d3c42.png">

Step 2: We are then prompted to choose the list of stats we want to compare and enter them as a space separated list spelled the way they are given in any order we want. 

<img width="995" alt="screen shot 2017-06-19 at 4 24 28 pm" src="https://user-images.githubusercontent.com/13561051/27309973-d5d45868-550b-11e7-8c32-229473e1c1f2.png">

Step 3: We will list all of the stats so we can compare the two players, Kevin Durant and LeBron James, based on all of the stats available to the program.

<img width="1335" alt="screen shot 2017-06-19 at 4 34 01 pm" src="https://user-images.githubusercontent.com/13561051/27310159-24ded586-550d-11e7-9c8a-3036d61f9319.png">


Step 4: Now the program will compare the two players and list their stats as well as an arrow pointing to who is leading in that particular stat. The results are then shown in a table format.

<img width="1338" alt="screen shot 2017-06-19 at 3 40 13 pm" src="https://user-images.githubusercontent.com/13561051/27310123-e6dd505a-550c-11e7-9697-1815dabbc15c.png">

We can see here that Durant leads in 6 stat categories whereas James leads in 4 of the stat categories.
