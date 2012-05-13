<?php

$con = mysql_connect("localhost","root","Fuc5de3@wr");
	
mysql_select_db("wordpress", $con);

$result = mysql_query("SELECT * FROM fbmongousers");

$arr = array();

while($row = mysql_fetch_array($result)) {

  $arr[] = $row["id"];
  
  }
  
echo json_encode($arr);

?>
