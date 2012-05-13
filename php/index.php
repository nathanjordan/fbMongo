<?php

$secret = "9e283992e0ba5892ddf42ad548176472";
$signed_request = $_POST["signed_request"];

function parse_signed_request($signed_request, $secret) {
  list($encoded_sig, $payload) = explode('.', $signed_request, 2); 

  // decode the data
  $sig = base64_url_decode($encoded_sig);
  $data = json_decode(base64_url_decode($payload), true);

  if (strtoupper($data['algorithm']) !== 'HMAC-SHA256') {
    error_log('Unknown algorithm. Expected HMAC-SHA256');
    return null;
  }

  // check sig
  $expected_sig = hash_hmac('sha256', $payload, $secret, $raw = true);
  if ($sig !== $expected_sig) {
    error_log('Bad Signed JSON signature!');
    return null;
  }

  return $data;
}

function base64_url_decode($input) {
  return base64_decode(strtr($input, '-_', '+/'));
}

$json = parse_signed_request($signed_request, $secret);

$userid = $json["user_id"];

if($userid.length == 0) {
	
	echo "<h3>Looks like you're not authenticated :(</h3>";
	
	}

else {
	
	$con = mysql_connect("localhost","root","Fuc5de3@wr");
	
	mysql_select_db("wordpress", $con);
	
	$query = sprintf("REPLACE INTO fbmongousers ( id ) VALUES ( '%s' )",
            mysql_real_escape_string($userid)
            );
     
     //print $query;
     
     mysql_query($query);
	
	}
	
echo "<h3>I have access to your likes and your friends likes, theres nothing else for you to do! have a nice day!</h3>";

?>
