<?php
  $config = parse_ini_file('/etc/archangel/archangel.conf');
  $blockpage=$config["blockpageip"] . ':' . $config['blockpageport'];
?>
<html>
<title>Archangel - Block Page</title>
<body bgcolor="#0B0B3B">
  <table bgcolor="black" width="98%" style="border:3px solid black" cellpadding="3px">
    <tr>
      <td colspan="2" style="border:3px solid black" bgcolor="white" height="90px">
	<font size="8" face="verdana"><center><b>Archangel</b></center></font>
      </td>
    </tr>
    <tr>
      <td width=400 style="border:3px solid black">
	<img src="http://<?php echo $blockpage; ?>/images/archangel.jpg">
      </td>
      <td style="border:3px solid black" bgcolor="white" valign="top">
	<center>
	  <font size=6 face="verdana">
	    <h3>Block Page</h3>
	  </font>
	  <font size=5 face="verdana">
	    Block category: <b><?php echo $_GET['category'] ?></b>
	  </font>
	  <br>
	  <br>
	  <font size=4 face="verdana">
	    <p align="left" style="width: 80%">
	      You are seeing this page because the page you have requested has been 
	      restricted. It may contain inappropriate content or security threats.
	      If you believe this page is a false positive and should not be filtered, 
	      please contact your network administrator and report any potential false 
	      positives.
	    </p>
	  </font>
	  <br>
	</center>
      </td>
    </tr>
    <tr>
      <td colspan="2" style="border:3px solid black" bgcolor="grey">
	<center>Archangel content filter - released July 2014</center>
      </td>
    </tr>
  </table>
</body>
</html>
