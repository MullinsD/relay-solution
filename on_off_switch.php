 <?php
 //Connect to database
 $dbconn = mysql_connect("mysql.eecs.ku.edu","drmullin", "skl00ker") or
		    die('Could not connect: ' . mysql_error());
		    mysql_select_db('drmullin') or die('Could not select database');

	//Execute query that gets the values currently held in the fields Water and Light
	$query = "SELECT Water, Light FROM GPIO_Pins WHERE Pi = 1;";
    $result = mysql_query($query) or die('Query failed: ' . mysql_error());
    if(mysql_num_rows ($result)){
	  //print the values either "on" or "off" to the page
      $row = mysql_fetch_row($result);
	  echo $row[0] . "\n"; //water
	  echo $row[1]; //light
	  //send value of water to Pi here.
	  
	}

?>	