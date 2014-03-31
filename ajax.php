<?php
//connect to the database
$query=mysql_connect("mysql.eecs.ku.edu","drmullin", "skl00ker");
mysql_select_db('drmullin');
// gets the post value from the button.php script
if(isset($_POST['value']))
{
   //updates the value in the database with value of the button from button.php
  $value=$_POST['value'];
	mysql_query("update GPIO_Pins set Water='$value' where Pi='1'");
	echo "<h2>The sprinkler is: " .$value."</h2>";
}

?>